from __future__ import annotations

from models import Patient, TrainingSample


DISEASES = [
    "Cảm cúm",
    "Viêm họng",
    "Viêm phổi",
    "COVID-19",
    "Dạ dày",
    "Dị ứng",
    "Sốt xuất huyết",
    "Viêm gan",
]

SYMPTOMS = [
    "Sốt",
    "Ho",
    "Đau họng",
    "Sổ mũi",
    "Nhức đầu",
    "Mệt mỏi",
    "Buồn nôn",
    "Chóng mặt",
    "Khó thở",
    "Đau ngực",
    "Đau bụng",
    "Tiêu chảy",
    "Phát ban",
]

TRAINING_DATA = [
    TrainingSample(Patient(["Sốt", "Ho", "Đau họng", "Sổ mũi", "Nhức đầu", "Mệt mỏi"], 170, 65), "Cảm cúm"),
    TrainingSample(Patient(["Sốt", "Ho", "Sổ mũi", "Mệt mỏi"], 165, 58), "Cảm cúm"),
    TrainingSample(Patient(["Đau họng", "Sổ mũi", "Nhức đầu", "Mệt mỏi"], 175, 70), "Cảm cúm"),
    TrainingSample(Patient(["Sốt", "Ho", "Nhức đầu"], 160, 55), "Cảm cúm"),
    TrainingSample(Patient(["Sốt", "Đau họng", "Mệt mỏi"], 180, 75), "Cảm cúm"),

    TrainingSample(Patient(["Đau họng", "Sốt", "Khó nuốt", "Ho khan"], 168, 62), "Viêm họng"),
    TrainingSample(Patient(["Đau họng dữ dội", "Sốt cao", "Nhức đầu"], 172, 68), "Viêm họng"),
    TrainingSample(Patient(["Đau họng", "Khàn giọng", "Ho"], 158, 52), "Viêm họng"),
    TrainingSample(Patient(["Sốt", "Đau họng", "Sưng hạch"], 185, 80), "Viêm họng"),
    TrainingSample(Patient(["Đau họng", "Nhức đầu", "Mệt mỏi"], 162, 57), "Viêm họng"),

    TrainingSample(Patient(["Sốt cao", "Ho có đờm", "Khó thở", "Đau ngực"], 175, 72), "Viêm phổi"),
    TrainingSample(Patient(["Khó thở", "Sốt", "Mệt mỏi nặng", "Đau ngực khi thở"], 169, 64), "Viêm phổi"),
    TrainingSample(Patient(["Ho liên tục", "Sốt", "Ớn lạnh", "Khó thở"], 182, 78), "Viêm phổi"),
    TrainingSample(Patient(["Đau ngực", "Ho có đờm vàng", "Sốt"], 166, 60), "Viêm phổi"),
    TrainingSample(Patient(["Khó thở khi vận động", "Ho", "Mệt mỏi"], 178, 74), "Viêm phổi"),

    TrainingSample(Patient(["Sốt", "Ho khan", "Mất vị giác", "Mất khứu giác"], 171, 66), "COVID-19"),
    TrainingSample(Patient(["Sốt", "Khó thở", "Đau cơ", "Mệt mỏi"], 164, 59), "COVID-19"),
    TrainingSample(Patient(["Ho", "Sốt nhẹ", "Mất vị giác", "Đau họng"], 176, 71), "COVID-19"),
    TrainingSample(Patient(["Mệt mỏi", "Đau đầu", "Mất khứu giác", "Sổ mũi"], 163, 58), "COVID-19"),
    TrainingSample(Patient(["Sốt", "Ho", "Khó thở nhẹ", "Đau cơ"], 179, 76), "COVID-19"),

    TrainingSample(Patient(["Đau bụng", "Buồn nôn", "Ợ chua", "Chán ăn"], 167, 63), "Dạ dày"),
    TrainingSample(Patient(["Đau thượng vị", "Buồn nôn", "Ợ nóng"], 173, 69), "Dạ dày"),
    TrainingSample(Patient(["Đau bụng sau ăn", "Buồn nôn", "Đầy bụng"], 159, 54), "Dạ dày"),
    TrainingSample(Patient(["Ợ chua", "Đau bụng", "Khó tiêu"], 181, 77), "Dạ dày"),
    TrainingSample(Patient(["Buồn nôn", "Đau bụng", "Chán ăn"], 161, 56), "Dạ dày"),

    TrainingSample(Patient(["Phát ban", "Ngứa", "Sổ mũi", "Hắt hơi"], 174, 67), "Dị ứng"),
    TrainingSample(Patient(["Ngứa mắt", "Hắt hơi", "Sổ mũi"], 168, 61), "Dị ứng"),
    TrainingSample(Patient(["Phát ban", "Khó thở", "Sưng mặt"], 177, 73), "Dị ứng"),
    TrainingSample(Patient(["Hắt hơi liên tục", "Ngứa mũi", "Chảy nước mắt"], 155, 50), "Dị ứng"),
    TrainingSample(Patient(["Phát ban", "Ngứa", "Sổ mũi"], 170, 65), "Dị ứng"),

    TrainingSample(Patient(["Sốt cao đột ngột", "Đau đầu dữ dội", "Xuất huyết", "Đau cơ"], 172, 68), "Sốt xuất huyết"),
    TrainingSample(Patient(["Sốt", "Xuất huyết dưới da", "Buồn nôn"], 166, 60), "Sốt xuất huyết"),
    TrainingSample(Patient(["Sốt cao", "Đau sau hốc mắt", "Đau cơ khớp"], 180, 75), "Sốt xuất huyết"),
    TrainingSample(Patient(["Sốt", "Xuất huyết", "Mệt mỏi"], 164, 59), "Sốt xuất huyết"),
    TrainingSample(Patient(["Sốt cao", "Đau đầu", "Buồn nôn", "Xuất huyết nhẹ"], 178, 74), "Sốt xuất huyết"),

    TrainingSample(Patient(["Mệt mỏi", "Vàng da", "Vàng mắt", "Đau hạ sườn phải"], 175, 70), "Viêm gan"),
    TrainingSample(Patient(["Chán ăn", "Buồn nôn", "Mệt mỏi", "Vàng da"], 169, 64), "Viêm gan"),
    TrainingSample(Patient(["Đau bụng", "Sốt nhẹ", "Vàng mắt"], 182, 78), "Viêm gan"),
    TrainingSample(Patient(["Mệt mỏi kéo dài", "Chán ăn", "Đau hạ sườn"], 167, 62), "Viêm gan"),
    TrainingSample(Patient(["Vàng da", "Buồn nôn", "Ngứa"], 173, 69), "Viêm gan"),
]
