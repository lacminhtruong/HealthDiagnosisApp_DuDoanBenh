from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import unicodedata

import torch

from models import DiagnosisResult, Patient


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "trained_models" / "health_diagnosis_model.pt"
DEFAULT_ASSOCIATION_RULES_PATH = PROJECT_ROOT / "trained_models" / "association_rules_meta.json"
SYMPTOM_PREFIX = "symptom__"


def normalize_text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFC", str(value or "")).strip().split()).casefold()


class SymptomSuggestionService:
    def __init__(
        self,
        available_symptoms: list[str],
        rules_path: Path = DEFAULT_ASSOCIATION_RULES_PATH,
    ) -> None:
        self.symptom_lookup = {
            normalize_text(symptom): symptom
            for symptom in available_symptoms
        }
        self.algorithm = "Apriori / Association Rules"
        self.parameters: dict[str, object] = {}
        self.metrics: dict[str, object] = {}
        self.rules: list[dict[str, object]] = []

        if not rules_path.exists():
            return

        try:
            artifact = json.loads(rules_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        self.algorithm = str(artifact.get("algorithm", self.algorithm))
        self.parameters = dict(artifact.get("parameters", {}))
        self.metrics = dict(artifact.get("metrics", {}))

        for rule in artifact.get("rules", []):
            antecedents = self._clean_symptoms(rule.get("antecedents"))
            consequents = self._clean_symptoms(rule.get("consequents"))
            if not antecedents or not consequents:
                continue

            antecedent_keys = {normalize_text(symptom) for symptom in antecedents}
            consequent_keys = {
                normalize_text(symptom)
                for symptom in consequents
                if normalize_text(symptom) in self.symptom_lookup
            }
            if consequent_keys:
                self.rules.append(
                    {
                        "antecedent_keys": antecedent_keys,
                        "consequent_keys": consequent_keys,
                        "confidence_percent": float(rule.get("confidence_percent", 0)),
                        "support_percent": float(rule.get("support_percent", 0)),
                        "lift": float(rule.get("lift", 0)),
                    }
                )

    @property
    def mining_summary(self) -> dict[str, object]:
        required_metrics = {"total_frequent", "total_closed", "total_maximal"}
        return {
            "available": required_metrics.issubset(self.metrics),
            "algorithm": self.algorithm,
            "parameters": self.parameters,
            "metrics": self.metrics,
        }

    @staticmethod
    def _clean_symptoms(values: object) -> list[str]:
        if not isinstance(values, list):
            return []
        return [
            " ".join(unicodedata.normalize("NFC", str(value)).strip().split())
            for value in values
            if str(value).strip()
        ]

    def suggest(self, selected_symptoms: list[str], limit: int = 6) -> list[dict[str, object]]:
        selected_keys = {
            normalize_text(symptom)
            for symptom in selected_symptoms
            if normalize_text(symptom) in self.symptom_lookup
        }
        if not selected_keys:
            return []

        best_by_symptom: dict[str, dict[str, object]] = {}
        for rule in self.rules:
            antecedent_keys = rule["antecedent_keys"]
            if not antecedent_keys.issubset(selected_keys):
                continue

            for symptom_key in rule["consequent_keys"] - selected_keys:
                suggestion = {
                    "symptom": self.symptom_lookup[symptom_key],
                    "confidence_percent": round(float(rule["confidence_percent"]), 2),
                    "support_percent": round(float(rule["support_percent"]), 2),
                    "lift": round(float(rule["lift"]), 3),
                    "matched_symptom_count": len(antecedent_keys),
                }
                current = best_by_symptom.get(symptom_key)
                if current is None or self._sort_key(suggestion) > self._sort_key(current):
                    best_by_symptom[symptom_key] = suggestion

        return sorted(best_by_symptom.values(), key=self._sort_key, reverse=True)[:limit]

    @staticmethod
    def _sort_key(suggestion: dict[str, object]) -> tuple[int, float, float, float]:
        return (
            int(suggestion["matched_symptom_count"]),
            float(suggestion["confidence_percent"]),
            float(suggestion["lift"]),
            float(suggestion["support_percent"]),
        )


class TrainedModelDiagnosisService:
    def __init__(self, model_path: Path = DEFAULT_MODEL_PATH) -> None:
        if not model_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy model đã train: {model_path}. "
                "Hãy chạy: uv run python scripts/train_model.py"
            )

        self.model_path = model_path
        self.artifact = torch.load(model_path, map_location="cpu")
        if self.artifact.get("model_type") != "knn":
            raise ValueError("Model artifact hiện tại không phải KNN. Hãy train lại bằng scripts/train_model.py.")

        self.k: int = int(self.artifact["k"])
        self.train_features: torch.Tensor = self.artifact["train_features"]
        self.train_labels: torch.Tensor = self.artifact["train_labels"]
        self.feature_columns: list[str] = self.artifact["feature_columns"]
        self.label_to_disease: dict[str, str] = self.artifact["label_to_disease"]
        self.normalization: dict[str, float] = self.artifact["normalization"]
        self.metrics: dict = self.artifact.get("metrics", {})
        self.symptom_feature_names = [
            column.replace(SYMPTOM_PREFIX, "", 1)
            for column in self.feature_columns
            if column.startswith(SYMPTOM_PREFIX)
        ]
        self.symptom_lookup = {
            normalize_text(symptom): symptom
            for symptom in self.symptom_feature_names
        }

    @property
    def available_symptoms(self) -> list[str]:
        return self.symptom_feature_names

    def predict(self, patient: Patient) -> DiagnosisResult:
        features = self._build_feature_vector(patient)
        distances = torch.cdist(features, self.train_features)[0]
        effective_k = min(self.k, self.train_features.shape[0])
        neighbor_distances, neighbor_indices = torch.topk(
            distances,
            k=effective_k,
            largest=False,
        )
        neighbor_labels = self.train_labels[neighbor_indices]

        predicted_label = self._choose_label(neighbor_labels, neighbor_distances)
        predicted_disease = self.label_to_disease[str(predicted_label)]
        disease_percentages = self._build_vote_percentages(neighbor_labels, effective_k)
        confidence_percent = disease_percentages[predicted_disease]
        nearest_neighbors = [
            {
                "rank": index,
                "disease": self.label_to_disease[str(label.item())],
                "distance": round(distance.item(), 4),
            }
            for index, (label, distance) in enumerate(zip(neighbor_labels, neighbor_distances), start=1)
        ]

        explanation = "\n".join(
            [
                "Web đang sử dụng KNN từ file model .pt.",
                f"Model: {self.model_path.relative_to(PROJECT_ROOT)}",
                f"K: {effective_k}",
                "Tập dữ liệu đã chia theo tỉ lệ 70% train / 20% test / 10% valid.",
                f"Số mẫu train: {self.metrics.get('training_rows', 'N/A')}",
                f"Số mẫu test: {self.metrics.get('test_rows', 'N/A')}",
                f"Số mẫu valid: {self.metrics.get('valid_rows', 'N/A')}",
                f"Test accuracy: {self.metrics.get('test_accuracy', 'N/A')}",
                f"Valid accuracy: {self.metrics.get('valid_accuracy', 'N/A')}",
                f"BMI đầu vào: {patient.bmi:.2f}",
                "",
                "Các hàng xóm gần nhất:",
                *[
                    f"- {neighbor['disease']}: khoảng cách = {neighbor['distance']:.4f}"
                    for neighbor in nearest_neighbors
                ],
            ]
        )

        return DiagnosisResult(
            predicted_disease=predicted_disease,
            disease_percentages=disease_percentages,
            confidence_percent=confidence_percent,
            explanation=explanation,
            model_path=str(self.model_path.relative_to(PROJECT_ROOT)),
            feature_count=len(self.feature_columns),
            k=effective_k,
            metrics=self.metrics,
            nearest_neighbors=nearest_neighbors,
        )

    def _build_feature_vector(self, patient: Patient) -> torch.Tensor:
        symptom_set = {
            normalize_text(symptom)
            for symptom in patient.symptoms
        }
        values: list[float] = []

        for column in self.feature_columns:
            if column == "age_scaled":
                values.append(self._min_max_scale("age", patient.age))
            elif column == "gender_encoded":
                values.append(self._encode_gender(patient.gender))
            elif column == "height_cm_scaled":
                values.append(self._min_max_scale("height_cm", patient.height_cm))
            elif column == "weight_kg_scaled":
                values.append(self._min_max_scale("weight_kg", patient.weight_kg))
            elif column == "bmi_scaled":
                values.append(self._min_max_scale("bmi", patient.bmi))
            elif column == "height_scaled":
                values.append(patient.height_cm / self.normalization["height_cm_divisor"])
            elif column == "weight_scaled":
                values.append(patient.weight_kg / self.normalization["weight_kg_divisor"])
            elif column == "bmi_scaled":
                values.append(patient.bmi / self.normalization["bmi_divisor"])
            elif column.startswith(SYMPTOM_PREFIX):
                symptom = column.replace(SYMPTOM_PREFIX, "", 1)
                values.append(1.0 if normalize_text(symptom) in symptom_set else 0.0)
            else:
                values.append(0.0)

        return torch.tensor([values], dtype=torch.float32)

    def _min_max_scale(self, field_name: str, value: float) -> float:
        minimum = self.normalization[f"{field_name}_min"]
        maximum = self.normalization[f"{field_name}_max"]
        if value <= 0:
            value = self.normalization.get(f"{field_name}_default", (minimum + maximum) / 2)
        if maximum == minimum:
            return 0.0
        scaled = (value - minimum) / (maximum - minimum)
        return min(max(scaled, 0.0), 1.0)

    @staticmethod
    def _encode_gender(gender: str) -> float:
        normalized = normalize_text(gender)
        if normalized in {"nữ", "nu", "female", "f", "1"}:
            return 1.0
        if normalized in {"nam", "male", "m", "0"}:
            return 0.0
        return 0.5

    def _choose_label(self, neighbor_labels: torch.Tensor, neighbor_distances: torch.Tensor) -> int:
        label_votes = Counter(neighbor_labels.tolist())
        best_vote_count = max(label_votes.values())
        candidates = [
            label
            for label, vote_count in label_votes.items()
            if vote_count == best_vote_count
        ]
        if len(candidates) == 1:
            return int(candidates[0])

        return int(
            min(
                candidates,
                key=lambda label: self._average_distance_for_label(
                    neighbor_labels,
                    neighbor_distances,
                    label,
                ),
            )
        )

    @staticmethod
    def _average_distance_for_label(labels: torch.Tensor, distances: torch.Tensor, label: int) -> float:
        matching_distances = [
            distance
            for current_label, distance in zip(labels.tolist(), distances.tolist())
            if current_label == label
        ]
        return sum(matching_distances) / len(matching_distances)

    def _build_vote_percentages(self, neighbor_labels: torch.Tensor, effective_k: int) -> dict[str, float]:
        label_votes = Counter(neighbor_labels.tolist())
        pairs = []

        for label, vote_count in label_votes.items():
            disease = self.label_to_disease[str(label)]
            pairs.append((disease, round(vote_count / effective_k * 100, 2)))

        return dict(sorted(pairs, key=lambda item: item[1], reverse=True))
