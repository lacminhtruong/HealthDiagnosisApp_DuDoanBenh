# HealthDiagnosisApp Python

Đồ án chẩn đoán bệnh bằng Python Flask. Web sử dụng thuật toán KNN từ file `trained_models/health_diagnosis_model.pt` để nhận diện bệnh từ triệu chứng, chiều cao và cân nặng.

## Chạy project

Chạy nhanh bằng `uv`:

```powershell
uv run python app.py
```

Sau đó mở:

```text
http://127.0.0.1:5000
```

## Luồng hoạt động

Web hiện tại chạy theo luồng:

```text
form nhập liệu -> services.py -> KNN trong trained_models/health_diagnosis_model.pt -> kết quả chẩn đoán
```

`data.py` không còn được web dùng để dự đoán trực tiếp. File này chỉ dùng khi cần xuất lại dữ liệu Excel hoặc tạo lại dataset ban đầu.

## Chia dữ liệu

Script train chia dữ liệu theo từng bệnh để giữ tỷ lệ lớp:

```text
70% train / 20% test / 10% valid
```

Với KNN, bước "train" là lưu các vector của tập train vào file `.pt`. Khi dự đoán, web tính khoảng cách từ bệnh nhân mới tới các mẫu train và lấy K hàng xóm gần nhất để bỏ phiếu.

## Cấu trúc

- `app.py`: route Flask và xử lý form.
- `models.py`: các lớp dữ liệu dùng `dataclass`.
- `services.py`: load artifact `.pt` và dự đoán bằng KNN.
- `data.py`: dữ liệu mẫu để xuất Excel nếu cần.
- `datasets/health_training_data.xlsx`: file Excel nhỏ được xuất từ `data.py`.
- `datasets/massive_health_training_data.xlsx`: file Excel lớn đang dùng để train.
- `trained_models/health_diagnosis_model.pt`: artifact KNN đang được web sử dụng.
- `trained_models/health_diagnosis_model_meta.json`: metadata, split và metric của model.
- `scripts/export_dataset.py`: xuất `data.py` sang Excel.
- `scripts/train_model.py`: chia train/test/valid và lưu KNN artifact `.pt`.
- `scripts/predict_with_trained_model.py`: chạy thử predict bằng artifact `.pt`.
- `templates/`: giao diện Jinja.
- `static/`: CSS và JavaScript.

## Xuất Excel Và Train Lại Model

Xuất dữ liệu trong `data.py` sang Excel:

```powershell
uv run python scripts/export_dataset.py
```

Train KNN bằng file dữ liệu lớn:

```powershell
uv run python scripts/train_model.py --dataset datasets/massive_health_training_data.xlsx --k 5
```

Chạy thử nhận diện bằng KNN artifact:

```powershell
uv run python scripts/predict_with_trained_model.py --height-cm 153 --weight-kg 56 --symptoms "Khó thở mãn tính" "Thở khò khè" "Tức ngực"
```
