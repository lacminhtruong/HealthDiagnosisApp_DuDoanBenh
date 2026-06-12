import unittest

from models import Patient
from services import TrainedModelDiagnosisService


class TrainedModelDiagnosisServiceTest(unittest.TestCase):
    def test_predicts_with_knn_pt_model(self):
        service = TrainedModelDiagnosisService()
        patient = Patient(
            symptoms=["  Khó thở mãn tính  ", "Thở khò khè", "Tức ngực"],
            height_cm=153,
            weight_kg=56,
        )

        features = service._build_feature_vector(patient)
        result = service.predict(patient)

        self.assertGreater(features[0, 3:].sum().item(), 0)
        self.assertIn("COPD", result.predicted_disease)
        self.assertGreaterEqual(result.confidence_percent, 60)
        self.assertEqual(result.model_path, "trained_models\\health_diagnosis_model.pt")
        self.assertTrue(service.available_symptoms)


if __name__ == "__main__":
    unittest.main()
