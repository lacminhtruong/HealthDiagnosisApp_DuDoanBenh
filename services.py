from __future__ import annotations

from collections import Counter
from pathlib import Path
import unicodedata

import torch

from models import DiagnosisResult, Patient


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "trained_models" / "health_diagnosis_model.pt"
SYMPTOM_PREFIX = "symptom__"


def normalize_text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFC", str(value or "")).strip().split()).casefold()


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
            if column == "height_scaled":
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
