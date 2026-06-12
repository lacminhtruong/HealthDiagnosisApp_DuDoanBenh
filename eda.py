import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Đường dẫn tới file dataset
PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_PATH = PROJECT_ROOT / "datasets" / "health_training_data.xlsx"

def run_eda():
    print("--- BẮT ĐẦU PHÂN TÍCH DỮ LIỆU (EDA) ---")
    df = pd.read_excel(DATASET_PATH, engine='openpyxl')
    
    # 1. Kiểm tra dữ liệu khuyết thiếu (Missing Values)
    print("\n[1] Kiểm tra giá trị khuyết thiếu:")
    missing_data = df.isnull().sum()
    print(missing_data[missing_data > 0] if missing_data.any() else "Tuyệt vời! Không có dữ liệu bị thiếu.")

    # 2. Thống kê sinh hiệu cơ bản
    print("\n[2] Thống kê mô tả (Chiều cao, Cân nặng, BMI):")
    print(df[['height_cm', 'weight_kg', 'bmi']].describe())

    # 3. Vẽ biểu đồ phân bố Bệnh lý (Class Distribution)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='disease', order=df['disease'].value_counts().index, palette='viridis')
    plt.title('Phân bố số lượng mẫu dữ liệu theo Bệnh lý', fontsize=14)
    plt.xlabel('Số lượng mẫu', fontsize=12)
    plt.ylabel('Tên Bệnh', fontsize=12)
    plt.tight_layout()
    
    # Lưu ảnh để lát dán vào báo cáo
    plt.savefig('disease_distribution.png')
    print("\n[3] Đã lưu biểu đồ phân bố bệnh tại 'disease_distribution.png'.")
    plt.show()

if __name__ == "__main__":
    run_eda()