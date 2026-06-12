import unittest

from app import app


class AppRoutesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_contains_age_and_gender_fields(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('name="age"', html)
        self.assertIn('name="gender"', html)
        self.assertIn("data-submit-dock", html)
        self.assertIn("dock-selected-count", html)
        self.assertIn('id="suggestion-box"', html)
        self.assertIn("/api/symptom-suggestions", html)
        self.assertIn("data-suggestion-toggle", html)

    def test_suggestion_api_returns_clickable_symptom_candidates(self):
        response = self.client.post(
            "/api/symptom-suggestions",
            json={"symptoms": ["Chảy nước mắt", "Đổ ghèn"]},
        )
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cộm mắt", payload["suggestions"])
        self.assertGreater(payload["details"][0]["confidence_percent"], 0)

    def test_suggestion_api_rejects_non_list_symptoms(self):
        response = self.client.post(
            "/api/symptom-suggestions",
            json={"symptoms": "Sốt"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["suggestions"], [])

    def test_suggestion_api_rejects_non_object_json(self):
        response = self.client.post(
            "/api/symptom-suggestions",
            json=["Sốt"],
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["suggestions"], [])

    def test_diagnosis_requires_age(self):
        response = self.client.post(
            "/ket-qua",
            data={
                "gender": "Nam",
                "height_cm": "153",
                "weight_kg": "56",
                "symptoms": ["Khó thở mãn tính"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tuổi phải nằm trong khoảng từ 1 đến 100.", response.get_data(as_text=True))

    def test_diagnosis_renders_result_with_age(self):
        response = self.client.post(
            "/ket-qua",
            data={
                "age": "65",
                "gender": "Nam",
                "height_cm": "153",
                "weight_kg": "56",
                "symptoms": ["Khó thở mãn tính", "Thở khò khè", "Tức ngực"],
            },
        )
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("COPD", html)
        self.assertIn("<b>65</b> tuổi", html)
        self.assertIn("data-count-up", html)
        self.assertIn("--target-width", html)
        self.assertIn("Tập phổ biến đóng", html)
        self.assertIn("Tập phổ biến tối đại", html)
        self.assertIn("Mạng lưới triệu chứng liên quan", html)
        self.assertIn("Confidence, support và lift", html)
        self.assertIn("association-network-frame", html)


if __name__ == "__main__":
    unittest.main()
