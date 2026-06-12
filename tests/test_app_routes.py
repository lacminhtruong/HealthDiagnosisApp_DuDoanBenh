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


if __name__ == "__main__":
    unittest.main()
