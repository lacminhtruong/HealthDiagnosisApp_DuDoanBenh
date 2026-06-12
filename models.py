from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Patient:
    symptoms: list[str] = field(default_factory=list)
    age: int = 0         # <-- THÊM DÒNG NÀY
    gender: str = ""     # <-- THÊM DÒNG NÀY
    height_cm: float = 0.0
    weight_kg: float = 0.0

    @property
    def bmi(self) -> float:
        if self.height_cm <= 0:
            return 0.0
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m * height_m)


@dataclass
class TrainingSample:
    patient: Patient
    disease_name: str


@dataclass
class DiagnosisResult:
    predicted_disease: str
    disease_percentages: dict[str, float]
    confidence_percent: float
    explanation: str
    model_path: str
    feature_count: int
    k: int
    metrics: dict[str, object]
    nearest_neighbors: list[dict[str, object]]
