import json
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report
import sys

# Thêm đường dẫn project để import các module của bạn
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Import các hàm cần thiết từ file train_model của bạn
from scripts.train_model import read_excel_dataset, predict_knn

DATASET_PATH = PROJECT_ROOT / "datasets" / "massive_health_training_data_v2.xlsx"
MODEL_PATH = PROJECT_ROOT / "trained_models" / "health_diagnosis_model.pt"
META_PATH = PROJECT_ROOT / "trained_models" / "health_diagnosis_model_meta.json"
OUTPUT_IMG = PROJECT_ROOT / "confusion_matrix.png"

def evaluate_and_plot():
    print("="*80)
    print(" ĐÁNH GIÁ MÔ HÌNH CHUYÊN SÂU (PRECISION, RECALL, CONFUSION MATRIX) ")
    print("="*80)

    # 1. Đọc dữ liệu và mô hình
    print("Đang nạp dữ liệu và mô hình đã huấn luyện...")
    matrix = read_excel_dataset(DATASET_PATH)
    artifact = torch.load(MODEL_PATH)
    
    # Lấy các thông số cần thiết từ artifact
    k = artifact["k"]
    train_features = artifact["train_features"]
    train_labels = artifact["train_labels"]
    test_features = artifact["test_features"]
    test_labels = artifact["test_labels"]
    disease_to_label = artifact["disease_to_label"]
    
    # Tạo map ngược từ label -> disease
    label_to_disease = {v: k for k, v in disease_to_label.items()}
    
    # Lấy top 15 bệnh phổ biến nhất trong tập test để vẽ (vì 50 bệnh vẽ lên hình sẽ bị nát)
    unique_labels, counts = np.unique(test_labels.numpy(), return_counts=True)
    top_15_labels = [label for _, label in sorted(zip(counts, unique_labels), reverse=True)[:15]]
    top_15_disease_names = [label_to_disease[label] for label in top_15_labels]

    # Lọc tập test chỉ lấy 15 bệnh phổ biến này để đánh giá chi tiết
    mask = torch.isin(test_labels, torch.tensor(top_15_labels))
    filtered_test_features = test_features[mask]
    filtered_test_labels = test_labels[mask]

    # 2. Chạy dự đoán
    print(f"Đang chạy thuật toán K-NN (K={k}) dự đoán cho tập Test...")
    predictions = predict_knn(filtered_test_features, train_features, train_labels, k)

    # Chuyển đổi tensor sang numpy array
    y_true = filtered_test_labels.numpy()
    y_pred = predictions.numpy()

    # 3. In Báo cáo phân loại (Classification Report)
    print("\n" + "-"*80)
    print(" BÁO CÁO PHÂN LOẠI CHI TIẾT (PRECISION, RECALL, F1-SCORE) ")
    print("-"*80)
    report = classification_report(y_true, y_pred, target_names=top_15_disease_names, digits=4)
    print(report)

    # 4. Vẽ Ma trận nhầm lẫn (Confusion Matrix)
    print("\nĐang vẽ biểu đồ Ma trận nhầm lẫn...")
    cm = confusion_matrix(y_true, y_pred, labels=top_15_labels)
    
    plt.figure(figsize=(14, 10))
    sns.set_theme(font='Calibri', style='white')
    
    # Vẽ heatmap
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                     xticklabels=top_15_disease_names, 
                     yticklabels=top_15_disease_names,
                     cbar_kws={'label': 'Số lượng mẫu'})
    
    plt.title('Ma Trận Nhầm Lẫn (Confusion Matrix) - Top 15 Bệnh Phổ Biến', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Bệnh được dự đoán (Predicted Label)', fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel('Bệnh thực tế (True Label)', fontsize=12, fontweight='bold', labelpad=10)
    
    # Xoay chữ ở trục X để dễ đọc
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300, bbox_inches='tight')
    
    print(f"-> [THÀNH CÔNG] Đã lưu hình ảnh Ma trận nhầm lẫn tại: {OUTPUT_IMG.name}")
    print("="*80)

if __name__ == "__main__":
    evaluate_and_plot()