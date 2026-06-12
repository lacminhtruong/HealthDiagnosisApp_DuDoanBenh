from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from models import Patient  # noqa: E402
from services import TrainedModelDiagnosisService  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--gender", choices=["Nam", "Nữ"], required=True)
    parser.add_argument("--height-cm", type=float, required=True)
    parser.add_argument("--weight-kg", type=float, required=True)
    parser.add_argument("--symptoms", nargs="+", required=True)
    args = parser.parse_args()

    service = TrainedModelDiagnosisService()
    result = service.predict(
        Patient(
            symptoms=args.symptoms,
            age=args.age,
            gender=args.gender,
            height_cm=args.height_cm,
            weight_kg=args.weight_kg,
        )
    )

    print(f"Prediction: {result.predicted_disease}")
    print(f"KNN vote confidence: {result.confidence_percent}%")
    print("Vote distribution:")
    for disease, percentage in result.disease_percentages.items():
        print(f"- {disease}: {percentage}%")


if __name__ == "__main__":
    main()
