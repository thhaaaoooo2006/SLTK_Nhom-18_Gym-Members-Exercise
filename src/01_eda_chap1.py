"""
Chương 1 — Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)
===========================================================
Tác giả : Nguyễn Thị Thảo (Owner) — Reviewer: Khánh
Mô-đun  : src/01_eda_chap1.py
Outputs :
    - outputs/tables/01_summary_stats.csv

─────────────────────────────────────────────────────────────
LÝ THUYẾT – Khái niệm nền tảng
─────────────────────────────────────────────────────────────
1. Mẫu ngẫu nhiên (Random Sample)
   Cho X là biến ngẫu nhiên có hàm phân phối F(x) chưa biết.
   Bộ n quan sát X₁, X₂, …, Xₙ được gọi là MẪU NGẪU NHIÊN
   kích thước n nếu chúng là n biến ngẫu nhiên ĐỘC LẬP và
   có CÙNG PHÂN PHỐI với X.

2. Hàm thống kê (Statistic)
   Mọi hàm T = g(X₁, …, Xₙ) KHÔNG chứa tham số chưa biết
   được gọi là hàm thống kê. Khi thay X₁, …, Xₙ bằng mẫu
   quan sát x₁, …, xₙ ta được giá trị thống kê (statistic value).

3. Trung bình mẫu (Sample Mean)
        x̄ = (1/n) Σᵢ₌₁ⁿ xᵢ
   x̄ là ước lượng không chệch, vững và hiệu quả cho kỳ vọng μ.

4. Phương sai mẫu hiệu chỉnh (Sample Variance, ddof = 1)
        S² = [1/(n − 1)] Σᵢ₌₁ⁿ (xᵢ − x̄)²
   Chia cho (n − 1) thay vì n để S² là ước lượng không chệch
   cho σ². Đại lượng (n − 1) gọi là bậc tự do (degrees of freedom).

5. Độ lệch chuẩn mẫu hiệu chỉnh
        S = √S²

6. Tần suất mẫu (Sample Proportion)
        p̂ = k / n
   trong đó k là số phần tử thỏa một sự kiện A nào đó.
─────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Thêm thư mục gốc vào sys.path để import stats_utils
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.stats_utils import (
    load_data,
    sample_mean,
    sample_var,
    sample_std,
    sample_prop,
    sample_median,
    sample_quantile,
    detect_outliers_iqr,
    describe_series,
    TABLES_DIR,
)

# ============================================================================
# 1. ĐỌC DỮ LIỆU
# ============================================================================
print("=" * 70)
print("CHƯƠNG 1 — TIỀN XỬ LÝ & THỐNG KÊ MÔ TẢ (MẪU NGẪU NHIÊN)")
print("=" * 70)

df = load_data()
print(f"\n[INFO] Đã tải dữ liệu: {df.shape[0]} quan sát × {df.shape[1]} biến")

# ============================================================================
# 2. MÔ TẢ BỐI CẢNH & PHÂN LOẠI BIẾN
# ============================================================================
print("\n" + "-" * 70)
print("2. MÔ TẢ BỐI CẢNH & PHÂN LOẠI BIẾN")
print("-" * 70)

BOI_CANH = """
Bộ dữ liệu "Gym Members Exercise Tracking" ghi lại thông tin tập luyện
của 973 thành viên phòng gym, bao gồm các chỉ số thể chất, sinh lý
(nhịp tim, lượng calo đốt cháy), thói quen tập luyện (loại bài tập,
tần suất, thời lượng) và trình độ kinh nghiệm. Mục tiêu nghiên cứu là
áp dụng các phương pháp suy luận thống kê (ước lượng, kiểm định, hồi quy)
để phân tích mối quan hệ giữa thời lượng tập (Session_Duration) và lượng
calo tiêu thụ (Calories_Burned), cũng như so sánh sự khác biệt theo
giới tính (Gender), loại bài tập (Workout_Type) và trình độ kinh nghiệm
(Experience_Level).
"""
print(BOI_CANH)

# Phân loại biến
NUMERICAL_COLS = [
    "Age", "Weight (kg)", "Height (m)", "Max_BPM", "Avg_BPM",
    "Resting_BPM", "Session_Duration", "Calories_Burned",
    "Fat_Percentage", "Water_Intake (liters)", "Workout_Frequency",
    "BMI",
]
CATEGORICAL_COLS = ["Gender", "Workout_Type", "Experience_Level"]

print("BIẾN ĐỊNH LƯỢNG (Numerical / Quantitative):")
for col in NUMERICAL_COLS:
    if col in df.columns:
        dtype_label = "Liên tục" if col not in ("Age", "Max_BPM", "Avg_BPM",
                                                  "Resting_BPM", "Workout_Frequency",
                                                  "Experience_Level") else "Rời rạc"
        print(f"   • {col:30s}  —  {dtype_label}")

print("\nBIẾN PHÂN LOẠI (Categorical / Qualitative):")
for col in CATEGORICAL_COLS:
    if col in df.columns:
        nuniq = df[col].nunique()
        vals = ", ".join(map(str, sorted(df[col].unique())))
        cat_type = "Danh nghĩa (Nominal)" if col != "Experience_Level" else "Thứ bậc (Ordinal)"
        print(f"   • {col:30s}  —  {cat_type}  |  {nuniq} giá trị: {vals}")

# ============================================================================
# 3. KIỂM TRA DỮ LIỆU: MISSING / DUPLICATE / OUTLIER
# ============================================================================
print("\n" + "-" * 70)
print("3. KIỂM TRA CHẤT LƯỢNG DỮ LIỆU")
print("-" * 70)

# 3.1. Missing values
print("\n3.1. GIÁ TRỊ THIẾU (Missing Values)")
missing = df.isnull().sum()
total_missing = missing.sum()
if total_missing == 0:
    print("   ✅ Không phát hiện giá trị thiếu (missing) trong toàn bộ dữ liệu.")
else:
    print(f"   ⚠ Tổng số missing: {total_missing}")
    for col in missing[missing > 0].index:
        pct = missing[col] / len(df) * 100
        print(f"      • {col}: {missing[col]} ({pct:.2f}%)")

# 3.2. Duplicate rows
print("\n3.2. QUAN SÁT TRÙNG LẶP (Duplicates)")
n_dup = df.duplicated().sum()
if n_dup == 0:
    print("   ✅ Không có hàng dữ liệu trùng lặp.")
else:
    print(f"   ⚠ Phát hiện {n_dup} hàng trùng lặp.")
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"   → Đã loại bỏ. Còn lại {len(df)} quan sát.")

# 3.3. Outlier detection (IQR method) — dùng hàm tự cài đặt từ stats_utils
print("\n3.3. PHÁT HIỆN NGOẠI LAI (Outlier Detection — Phương pháp IQR)")
print("   Quy tắc: Ngoại lai nếu xᵢ < Q₁ − 1.5·IQR  hoặc  xᵢ > Q₃ + 1.5·IQR")

continuous_cols = [c for c in NUMERICAL_COLS if c in df.columns]

for col in continuous_cols:
    result = detect_outliers_iqr(df[col].dropna().values)
    n_out = result["n_outliers"]
    if n_out > 0:
        pct_out = n_out / len(df) * 100
        print(f"   • {col:30s}  —  {n_out:3d} ngoại lai ({pct_out:.2f}%)")

print("\n   → Quyết định: GIỮ NGUYÊN dữ liệu gốc (không loại bỏ), vì đây là")
print("     các giá trị sinh lý thực tế hợp lệ (cân nặng, BMI,…) và mẫu đủ lớn")
print("     (n = 973) nên ngoại lai nhẹ không ảnh hưởng đáng kể đến ước lượng.")

# ============================================================================
# 4. THỐNG KÊ MÔ TẢ — DÙNG HÀM TỰ CÀI ĐẶT TỪ stats_utils
# ============================================================================
print("\n" + "-" * 70)
print("4. BẢNG THỐNG KÊ MÔ TẢ (tự cài đặt bằng stats_utils)")
print("-" * 70)

# 4a. Biến định lượng — dùng describe_series() từ stats_utils
desc_rows = []
for col in continuous_cols:
    s = df[col].dropna().values
    info = describe_series(s)
    desc_rows.append({
        "Biến": col,
        "n": info["n"],
        "x_bar": info["x_bar"],
        "S2": info["S2"],
        "S": info["S"],
        "Min": info["min"],
        "Q1": info["Q1"],
        "Median": info["median"],
        "Q3": info["Q3"],
        "Max": info["max"],
    })

df_desc = pd.DataFrame(desc_rows)
print("\n--- Biến định lượng ---")
print(df_desc.to_string(index=False))

# 4b. Tần suất mẫu (p̂) cho biến phân loại — dùng sample_prop() từ stats_utils
print("\n--- Tần suất mẫu (biến phân loại) ---")
freq_rows = []
for col in CATEGORICAL_COLS:
    for val in sorted(df[col].unique(), key=str):
        indicator = (df[col] == val).astype(int).values
        p_hat = sample_prop(indicator)
        count = int(np.sum(indicator))
        freq_rows.append({
            "Biến": col,
            "Giá trị": val,
            "Số lượng (k)": count,
            "p_hat": p_hat,
        })

df_freq = pd.DataFrame(freq_rows)
print(df_freq.to_string(index=False))

# ============================================================================
# 5. XUẤT KẾT QUẢ — DUY NHẤT 1 FILE: outputs/tables/01_summary_stats.csv
# ============================================================================
print("\n" + "-" * 70)
print("5. XUẤT KẾT QUẢ RA FILE")
print("-" * 70)

# Gộp bảng mô tả biến liên tục + bảng tần suất biến phân loại vào cùng 1 CSV
# Phần 1: Thống kê mô tả biến định lượng
# Phần 2: Tần suất mẫu biến phân loại (đánh dấu bằng cột "section")
df_desc_out = df_desc.copy()
df_desc_out.insert(0, "section", "descriptive_statistics")

df_freq_out = df_freq.copy()
df_freq_out = df_freq_out.rename(columns={"Giá trị": "value", "Số lượng (k)": "count"})
df_freq_out.insert(0, "section", "sample_proportion")

out_csv = TABLES_DIR / "01_summary_stats.csv"
with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
    f.write("# Phần 1: Thống kê mô tả biến định lượng (x_bar, S2, S dùng hàm tự cài đặt stats_utils)\n")
    df_desc.to_csv(f, index=False)
    f.write("\n# Phần 2: Tần suất mẫu (p_hat) biến phân loại\n")
    df_freq.to_csv(f, index=False)

print(f"   ✅ {out_csv}")

print("\n" + "=" * 70)
print("HOÀN THÀNH CHƯƠNG 1")
print("=" * 70)
