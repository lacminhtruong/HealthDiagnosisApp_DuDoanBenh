from __future__ import annotations

import os
import unicodedata

from flask import Flask, render_template, request

from models import Patient
from services import TrainedModelDiagnosisService


app = Flask(__name__)
diagnosis_service = TrainedModelDiagnosisService()


BODY_SYSTEM_RULES = [
    ("Hô hấp", ["ho", "thở", "phổi", "phế", "đờm", "ngực", "mũi", "xoang", "họng", "amidan"]),
    ("Mắt - tai - mũi - miệng", ["mắt", "tai", "miệng", "khứu giác", "vị giác", "nước mắt", "cộm"]),
    ("Tiêu hóa", ["bụng", "nôn", "tiêu", "đại tiện", "dạ dày", "ợ", "ăn", "gan", "vàng da", "vàng mắt", "mật"]),
    ("Tiết niệu", ["tiểu", "nước tiểu", "thận", "bàng quang"]),
    ("Tim mạch", ["tim", "huyết áp", "mạch", "hồi hộp", "phù", "đau thắt"]),
    ("Thần kinh - tâm lý", ["đầu", "chóng mặt", "choáng", "co giật", "mất ngủ", "lo âu", "trầm cảm", "tê", "yếu", "vô dụng", "buồn bã"]),
    ("Cơ - xương - khớp", ["xương", "khớp", "cơ", "lưng", "gối", "cứng", "đĩa đệm", "gout"]),
    ("Da - dị ứng", ["da", "ngứa", "ban", "mẩn", "mề đay", "sưng", "dị ứng"]),
    ("Nội tiết - chuyển hóa", ["giáp", "đường", "mỡ", "khát", "cân", "run tay"]),
]


def parse_float(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value or default)
    except ValueError:
        return default


def normalize_for_grouping(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def group_symptoms_by_body_system(symptoms: list[str]) -> list[dict[str, object]]:
    groups = {name: [] for name, _keywords in BODY_SYSTEM_RULES}
    groups["Toàn thân - khác"] = []

    for symptom in symptoms:
        normalized_symptom = normalize_for_grouping(symptom)
        matched_group = "Toàn thân - khác"
        for group_name, keywords in BODY_SYSTEM_RULES:
            if any(keyword in normalized_symptom for keyword in keywords):
                matched_group = group_name
                break
        groups[matched_group].append(symptom)

    return [
        {"name": name, "symptoms": group_symptoms}
        for name, group_symptoms in groups.items()
        if group_symptoms
    ]


def build_index_context(
    selected_symptoms: list[str] | None = None,
    height_cm: str = "",
    weight_kg: str = "",
    errors: list[str] | None = None,
) -> dict[str, object]:
    symptoms = diagnosis_service.available_symptoms
    return {
        "symptoms": symptoms,
        "symptom_groups": group_symptoms_by_body_system(symptoms),
        "selected_symptoms": selected_symptoms or [],
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "errors": errors or [],
    }


@app.get("/")
def index():
    return render_template("index.html", **build_index_context())


@app.post("/ket-qua")
def ket_qua():
    selected_symptoms = request.form.getlist("symptoms")
    height_cm = parse_float(request.form.get("height_cm"))
    weight_kg = parse_float(request.form.get("weight_kg"))

    errors: list[str] = []
    if not selected_symptoms:
        errors.append("Vui lòng chọn ít nhất một triệu chứng.")
    if height_cm <= 0:
        errors.append("Chiều cao phải lớn hơn 0 cm.")
    if weight_kg <= 0:
        errors.append("Cân nặng phải lớn hơn 0 kg.")

    if errors:
        return render_template(
            "index.html",
            **build_index_context(
                selected_symptoms=selected_symptoms,
                height_cm=request.form.get("height_cm", ""),
                weight_kg=request.form.get("weight_kg", ""),
                errors=errors,
            ),
        )

    patient = Patient(
        symptoms=selected_symptoms,
        height_cm=height_cm,
        weight_kg=weight_kg,
    )
    result = diagnosis_service.predict(patient)

    return render_template("result.html", result=result, patient=patient)


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", message="Không tìm thấy trang."), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", message="Có lỗi khi xử lý yêu cầu."), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
