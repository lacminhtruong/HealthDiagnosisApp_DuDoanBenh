import unittest

from models import Patient
from services import TrainedModelDiagnosisService


class TrainedModelDiagnosisServiceTest(unittest.TestCase):
    def test_predicts_with_knn_pt_model(self):
        service = TrainedModelDiagnosisService()
        patient = Patient(
            symptoms=["  Khó thở mãn tính  ", "Thở khò khè", "Tức ngực"],
            age=65,
            gender="Nam",
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

    def test_encodes_gender_from_patient(self):
        service = TrainedModelDiagnosisService()
        male_features = service._build_feature_vector(Patient(gender="Nam"))
        female_features = service._build_feature_vector(Patient(gender="Nữ"))
        gender_index = service.feature_columns.index("gender_encoded")

        self.assertEqual(male_features[0, gender_index].item(), 0.0)
        self.assertEqual(female_features[0, gender_index].item(), 1.0)

    def test_encodes_age_from_patient(self):
        service = TrainedModelDiagnosisService()
        young_features = service._build_feature_vector(Patient(age=18))
        older_features = service._build_feature_vector(Patient(age=70))
        age_index = service.feature_columns.index("age_scaled")

        self.assertLess(young_features[0, age_index].item(), older_features[0, age_index].item())


if __name__ == "__main__":
    unittest.main()
