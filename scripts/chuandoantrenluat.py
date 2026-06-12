import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpmax
from pathlib import Path
import sys

# Cấu hình đường dẫn
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "datasets" / "massive_health_training_data_v2.xlsx"
OUTPUT_JSON_PATH = PROJECT_ROOT / "trained_models" / "association_rules_meta.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_closed_frequent_itemsets(
    frequent_itemsets: pd.DataFrame,
    transaction_count: int,
) -> pd.DataFrame:
    """Return itemsets that have no proper superset with the same support."""
    if frequent_itemsets.empty:
        return frequent_itemsets.copy()

    candidates = frequent_itemsets.copy()
    candidates["support_count"] = (
        candidates["support"] * transaction_count
    ).round().astype(int)
    candidates["itemset_length"] = candidates["itemsets"].map(len)
    closed_indices: list[int] = []

    for _, support_group in candidates.groupby("support_count", sort=False):
        larger_itemsets: list[frozenset[str]] = []
        ordered_group = support_group.sort_values("itemset_length", ascending=False)

        for index, row in ordered_group.iterrows():
            itemset = frozenset(row["itemsets"])
            if not any(itemset < superset for superset in larger_itemsets):
                closed_indices.append(index)
            larger_itemsets.append(itemset)

    return candidates.loc[closed_indices].drop(
        columns=["support_count", "itemset_length"]
    ).reset_index(drop=True)


def run_association_rules():
    print("--- BẮT ĐẦU TÌM LUẬT KẾT HỢP TRIỆU CHỨNG ---")
    
    # 1. Đọc dữ liệu
    df = pd.read_excel(DATASET_PATH, engine='openpyxl')
    
    # 2. Tiền xử lý
    symptom_cols = [col for col in df.columns if str(col).startswith('symptom__')]
    df_symptoms = df[symptom_cols].copy()
    df_symptoms.columns = [col.replace('symptom__', '') for col in df_symptoms.columns]
    df_symptoms = df_symptoms.astype(bool)
    
    # 3. Chạy thuật toán Apriori
    min_support = 0.0085
    print(f"\n[1/3] Đang quét tập dữ liệu (min_support = {min_support})...")
    frequent_itemsets = apriori(df_symptoms, min_support=min_support, use_colnames=True)

    # 4. Trích xuất tập phổ biến đóng và tối đại
    print("[2/3] Đang trích xuất tập phổ biến đóng và tối đại...")
    closed_itemsets = find_closed_frequent_itemsets(frequent_itemsets, len(df_symptoms))
    maximal_itemsets = fpmax(df_symptoms, min_support=min_support, use_colnames=True)

    # 5. Sinh luật kết hợp
    min_confidence = 0.5
    print(f"[3/3] Đang sinh luật kết hợp (min_confidence = {min_confidence})...\n")
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    
    # Sắp xếp luật theo độ tin cậy từ cao xuống thấp
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    
    print(f"THÀNH CÔNG! Đã tìm ra {len(rules)} luật kết hợp đạt ngưỡng đã chọn.")
    print(
        "Tập phổ biến: "
        f"{len(frequent_itemsets)} | Đóng: {len(closed_itemsets)} | "
        f"Tối đại: {len(maximal_itemsets)}"
    )

    # 6. Đóng gói dữ liệu ra dạng JSON để hệ thống Web tái sử dụng
    rules_list = []
    for _, row in rules.iterrows():
        rules_list.append({
            "antecedents": sorted(row['antecedents']),
            "consequents": sorted(row['consequents']),
            "confidence_percent": round(float(row['confidence']) * 100, 2),
            "support_percent": round(float(row['support']) * 100, 2),
            "lift": round(float(row['lift']), 3),
        })

    # Tạo object meta data giống như file của KNN
    meta_data = {
        "algorithm": "Apriori / Association Rules",
        "dataset_path": str(DATASET_PATH),
        "parameters": {
            "min_support": min_support,
            "min_confidence": min_confidence
        },
        "metrics": {
            "total_transactions": len(df_symptoms),
            "total_symptoms": len(symptom_cols),
            "total_frequent": len(frequent_itemsets),
            "total_closed": len(closed_itemsets),
            "total_maximal": len(maximal_itemsets),
            "total_rules_found": len(rules_list),
        },
        "rules": rules_list
    }

    # 7. Ghi ra file JSON vào thư mục trained_models
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(
        json.dumps(meta_data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    print("-" * 80)
    print(f"Đã xuất cấu trúc luật kết hợp thành công tại:")
    print(OUTPUT_JSON_PATH.relative_to(PROJECT_ROOT))
    print("-" * 80)

if __name__ == "__main__":
    run_association_rules()
