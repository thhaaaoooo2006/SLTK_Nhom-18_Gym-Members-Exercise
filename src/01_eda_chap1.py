"""
Chương 1 — Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)
===========================================================
Tác giả : Nguyễn Thị Thảo (Owner) — Reviewer: Khánh
Mô-đun  : src/01_eda_chap1.py
Outputs :
    - outputs/tables/01_summary_stats.csv
    - report/sections/01_chap1.md

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
    fmt,
    md_table,
    TABLES_DIR,
    SECTIONS_DIR,
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

# Rename lại Water_Intake nếu chưa rename (giữ nguyên tên gốc từ CSV)
rename_map = {
    "Weight (kg)": "Weight_kg",
    "Height (m)": "Height_m",
    "Water_Intake (liters)": "Water_Intake",
}
# Lưu ý: stats_utils.load_data() đã rename Session_Duration và Workout_Frequency

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

# 3.3. Outlier detection (IQR method)
print("\n3.3. PHÁT HIỆN NGOẠI LAI (Outlier Detection — Phương pháp IQR)")
print("   Quy tắc: Ngoại lai nếu xᵢ < Q₁ − 1.5·IQR  hoặc  xᵢ > Q₃ + 1.5·IQR")

# Chỉ kiểm tra biến liên tục
continuous_cols = [c for c in NUMERICAL_COLS if c in df.columns]
outlier_summary_rows = []

for col in continuous_cols:
    s = df[col].dropna()
    q1 = float(np.percentile(s, 25))
    q3 = float(np.percentile(s, 75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    n_out = int(((s < lower) | (s > upper)).sum())
    pct_out = n_out / len(s) * 100
    outlier_summary_rows.append({
        "Biến": col,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Cận dưới": lower,
        "Cận trên": upper,
        "Số ngoại lai": n_out,
        "% ngoại lai": pct_out,
    })
    if n_out > 0:
        print(f"   • {col:30s}  —  {n_out:3d} ngoại lai ({pct_out:.2f}%)")

df_outlier = pd.DataFrame(outlier_summary_rows)

total_outlier = df_outlier["Số ngoại lai"].sum()
if total_outlier == 0:
    print("   ✅ Không phát hiện ngoại lai đáng kể theo phương pháp IQR.")
else:
    print(f"\n   Tổng cộng {int(total_outlier)} giá trị ngoại lai được phát hiện.")
    print("   → Quyết định: GIỮ NGUYÊN dữ liệu gốc (không loại bỏ), vì đây là")
    print("     các giá trị sinh lý thực tế hợp lệ (cân nặng, BMI,…) và mẫu đủ lớn")
    print("     (n = 973) nên ngoại lai nhẹ không ảnh hưởng đáng kể đến ước lượng.")

# ============================================================================
# 4. THỐNG KÊ MÔ TẢ — DÙNG HÀM TỰ CÀI ĐẶT
# ============================================================================
print("\n" + "-" * 70)
print("4. BẢNG THỐNG KÊ MÔ TẢ (tự cài đặt bằng stats_utils)")
print("-" * 70)

desc_rows = []
for col in continuous_cols:
    s = df[col].dropna().values
    desc_rows.append({
        "Biến": col,
        "n": len(s),
        "x̄ (trung bình)": sample_mean(s),
        "S² (phương sai HC)": sample_var(s, ddof=1),
        "S (độ lệch chuẩn)": sample_std(s, ddof=1),
        "Min": float(np.min(s)),
        "Q1": float(np.percentile(s, 25)),
        "Median": float(np.median(s)),
        "Q3": float(np.percentile(s, 75)),
        "Max": float(np.max(s)),
    })

df_desc = pd.DataFrame(desc_rows)
print(df_desc.to_string(index=False))

# ============================================================================
# 5. TẦN SUẤT MẪU (p̂) CHO CÁC BIẾN PHÂN LOẠI
# ============================================================================
print("\n" + "-" * 70)
print("5. TẦN SUẤT MẪU (p̂) — BIẾN PHÂN LOẠI")
print("-" * 70)

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
            "p̂ = k/n": p_hat,
        })

df_freq = pd.DataFrame(freq_rows)
print(df_freq.to_string(index=False))

# ============================================================================
# 6. XUẤT KẾT QUẢ
# ============================================================================
print("\n" + "-" * 70)
print("6. XUẤT KẾT QUẢ RA FILE")
print("-" * 70)

# 6a. CSV — Bảng thống kê mô tả
out_csv = TABLES_DIR / "01_summary_stats.csv"
# Gộp bảng mô tả biến liên tục + tần suất biến phân loại
df_desc.to_csv(out_csv, index=False, encoding="utf-8-sig")
print(f"   ✅ {out_csv}")

out_freq_csv = TABLES_DIR / "01_frequency_table.csv"
df_freq.to_csv(out_freq_csv, index=False, encoding="utf-8-sig")
print(f"   ✅ {out_freq_csv}")

out_outlier_csv = TABLES_DIR / "01_outlier_check.csv"
df_outlier.to_csv(out_outlier_csv, index=False, encoding="utf-8-sig")
print(f"   ✅ {out_outlier_csv}")

# 6b. Markdown report
md_lines = []
md_lines.append("# Chương 1 — Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)\n")

md_lines.append("## 1. Cơ sở lý thuyết\n")
md_lines.append("""### 1.1. Mẫu ngẫu nhiên (Random Sample)

Cho $X$ là biến ngẫu nhiên có hàm phân phối $F(x)$ chưa biết.
Bộ $n$ quan sát $X_1, X_2, \\ldots, X_n$ được gọi là **mẫu ngẫu nhiên** kích thước $n$
nếu chúng là $n$ biến ngẫu nhiên **độc lập** và có **cùng phân phối** với $X$ (i.i.d.).

### 1.2. Hàm thống kê (Statistic)

Mọi hàm $T = g(X_1, \\ldots, X_n)$ **không chứa tham số chưa biết** được gọi là hàm thống kê.

### 1.3. Trung bình mẫu (Sample Mean)

$$\\bar{x} = \\frac{1}{n} \\sum_{i=1}^{n} x_i$$

$\\bar{x}$ là ước lượng không chệch, vững và hiệu quả cho kỳ vọng $\\mu$.

### 1.4. Phương sai mẫu hiệu chỉnh (Sample Variance, ddof = 1)

$$S^2 = \\frac{1}{n-1} \\sum_{i=1}^{n} (x_i - \\bar{x})^2$$

Chia cho $(n - 1)$ thay vì $n$ để $S^2$ là ước lượng **không chệch** cho $\\sigma^2$.
Đại lượng $(n - 1)$ gọi là **bậc tự do** (degrees of freedom).

### 1.5. Độ lệch chuẩn mẫu hiệu chỉnh

$$S = \\sqrt{S^2}$$

### 1.6. Tần suất mẫu (Sample Proportion)

$$\\hat{p} = \\frac{k}{n}$$

trong đó $k$ là số phần tử trong mẫu thỏa sự kiện $A$.
""")

md_lines.append("## 2. Mô tả bối cảnh\n")
md_lines.append(BOI_CANH.strip())
md_lines.append("")

md_lines.append("## 3. Phân loại biến\n")
md_lines.append("### Biến định lượng (Numerical)\n")
md_lines.append("| Tên biến | Kiểu | Mô tả |")
md_lines.append("|---|---|---|")
var_desc_map = {
    "Age": ("Rời rạc", "Tuổi (năm)"),
    "Weight (kg)": ("Liên tục", "Cân nặng (kg)"),
    "Height (m)": ("Liên tục", "Chiều cao (m)"),
    "Max_BPM": ("Rời rạc", "Nhịp tim tối đa (bpm)"),
    "Avg_BPM": ("Rời rạc", "Nhịp tim trung bình (bpm)"),
    "Resting_BPM": ("Rời rạc", "Nhịp tim khi nghỉ (bpm)"),
    "Session_Duration": ("Liên tục", "Thời lượng buổi tập (giờ)"),
    "Calories_Burned": ("Liên tục", "Lượng calo tiêu thụ (kcal)"),
    "Fat_Percentage": ("Liên tục", "Tỷ lệ mỡ cơ thể (%)"),
    "Water_Intake (liters)": ("Liên tục", "Lượng nước uống (lít/ngày)"),
    "Workout_Frequency": ("Rời rạc", "Tần suất tập (ngày/tuần)"),
    "BMI": ("Liên tục", "Chỉ số BMI"),
}
for col in NUMERICAL_COLS:
    if col in var_desc_map:
        t, d = var_desc_map[col]
        md_lines.append(f"| `{col}` | {t} | {d} |")

md_lines.append("\n### Biến phân loại (Categorical)\n")
md_lines.append("| Tên biến | Kiểu | Các giá trị |")
md_lines.append("|---|---|---|")
cat_desc_map = {
    "Gender": ("Danh nghĩa", "Male, Female"),
    "Workout_Type": ("Danh nghĩa", "Cardio, HIIT, Strength, Yoga"),
    "Experience_Level": ("Thứ bậc", "1 (Beginner), 2 (Intermediate), 3 (Advanced)"),
}
for col in CATEGORICAL_COLS:
    if col in cat_desc_map:
        t, d = cat_desc_map[col]
        md_lines.append(f"| `{col}` | {t} | {d} |")

md_lines.append("\n## 4. Kiểm tra chất lượng dữ liệu\n")
md_lines.append(f"- **Kích thước mẫu**: n = {len(df)} quan sát, {df.shape[1]} biến")
md_lines.append(f"- **Giá trị thiếu**: {total_missing} (không có)")
md_lines.append(f"- **Hàng trùng lặp**: {n_dup}")

md_lines.append("\n### Kiểm tra ngoại lai (IQR)\n")
md_lines.append(md_table(df_outlier, nd=2))

md_lines.append("\n**Quyết định**: Giữ nguyên dữ liệu gốc — các ngoại lai đều là giá trị "
                "sinh lý thực tế hợp lệ và mẫu đủ lớn (n = 973).\n")

md_lines.append("## 5. Bảng thống kê mô tả\n")
md_lines.append("*Các giá trị được tính bằng hàm tự cài đặt trong `src/stats_utils.py`*\n")
md_lines.append(md_table(df_desc, nd=4))

md_lines.append("\n## 6. Tần suất mẫu (biến phân loại)\n")
md_lines.append(md_table(df_freq, nd=4))
md_lines.append("")

report_path = SECTIONS_DIR / "01_chap1.md"
report_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"   ✅ {report_path}")

print("\n" + "=" * 70)
print("HOÀN THÀNH CHƯƠNG 1")
print("=" * 70)
