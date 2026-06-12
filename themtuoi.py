import pandas as pd
import numpy as np
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_PATH = PROJECT_ROOT / "datasets" / "massive_health_training_data.xlsx"
OUTPUT_PATH = PROJECT_ROOT / "datasets" / "massive_health_training_data_v2.xlsx"

def add_demographics_to_dataset():
    print("="*75)
    print(" BỔ SUNG TUỔI & GIỚI TÍNH THEO LOGIC Y KHOA ")
    print("="*75)

    df = pd.read_excel(DATASET_PATH, engine='openpyxl')
    
    ages = []
    genders = []
    
    # Thiết lập seed để lần nào chạy cũng ra kết quả giống nhau
    np.random.seed(42)
    random.seed(42)

    for index, row in df.iterrows():
        disease = str(row['disease']).lower()
        
        # ----------------------------------------------------
        # 1. LOGIC GÁN TUỔI (Theo phân bố dịch tễ học)
        # ----------------------------------------------------
        if any(d in disease for d in ["tay chân miệng", "sởi", "thủy đậu"]):
            age = np.random.randint(1, 12)  # Trẻ em
        elif any(d in disease for d in ["thoái hóa khớp", "loãng xương", "suy tim", "copd"]):
            age = np.random.randint(45, 85) # Người lớn tuổi
        elif any(d in disease for d in ["rối loạn mỡ máu", "trĩ", "viêm đại tràng", "đau nửa đầu"]):
            age = np.random.randint(25, 60) # Người trưởng thành/Trung niên
        else:
            age = np.random.randint(15, 75) # Bệnh chung (Cảm cúm, viêm họng...)

        # ----------------------------------------------------
        # 2. LOGIC GÁN GIỚI TÍNH (Nam/Nữ)
        # ----------------------------------------------------
        # Đau nửa đầu, Loãng xương, Viêm tiết niệu -> Nữ mắc nhiều hơn (70% Nữ)
        if any(d in disease for d in ["đau nửa đầu", "loãng xương", "tiết niệu"]):
            gender = np.random.choice(["Nam", "Nữ"], p=[0.3, 0.7])
        # COPD, Trĩ, Gout -> Nam mắc nhiều hơn (70% Nam)
        elif any(d in disease for d in ["copd", "trĩ", "gout", "lao phổi"]):
            gender = np.random.choice(["Nam", "Nữ"], p=[0.7, 0.3])
        else:
            gender = np.random.choice(["Nam", "Nữ"], p=[0.5, 0.5]) # Tỷ lệ 50-50

        ages.append(age)
        genders.append(gender)

    # Chèn vào dataframe (Sau cột disease)
    df.insert(1, 'age', ages)
    df.insert(2, 'gender', genders)

    # Xuất ra file Excel mới
    df.to_excel(OUTPUT_PATH, index=False, engine='openpyxl')
    print(f"-> Đã sinh thành công {len(df)} bản ghi.")
    print(f"-> File mới đã được lưu tại: {OUTPUT_PATH.name}")
    print("-> Sẵn sàng để đưa vào huấn luyện mô hình!")

if __name__ == "__main__":
    add_demographics_to_dataset()