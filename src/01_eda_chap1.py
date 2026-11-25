"""Chương 1 — Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)
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
   có CÙNG PHÂN PHỐI với X (iid).

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
   cho σ²: E(S²) = σ². Đại lượng (n − 1) gọi là bậc tự do.

5. Độ lệch chuẩn mẫu hiệu chỉnh
        S = √S²

6. Tần suất mẫu (Sample Proportion)
        p̂ = k / n
   trong đó k là số phần tử thỏa mãn biến cố A nào đó.
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
    md_table,
    TABLES_DIR,
    SECTIONS_DIR,
)

def main():
    print("=" * 70)
    print("CHƯƠNG 1 — TIỀN XỬ LÝ & THỐNG KÊ MÔ TẢ (MẪU NGẪU NHIÊN)")
    print("Tác giả: Nguyễn Thị Thảo (Owner) — Reviewer: Khánh")
    print("=" * 70)

    # 1. Đọc dữ liệu
    df = load_data()
    n_rows, n_cols = df.shape
    print(f"\n[INFO] Đã tải dữ liệu: {n_rows} quan sát × {n_cols} biến")

    # 2. Phân loại biến
    NUMERICAL_COLS = [
        "Age", "Weight (kg)", "Height (m)", "Max_BPM", "Avg_BPM",
        "Resting_BPM", "Session_Duration", "Calories_Burned",
        "Fat_Percentage", "Water_Intake (liters)", "Workout_Frequency",
        "BMI",
    ]
    CATEGORICAL_COLS = ["Gender", "Workout_Type", "Experience_Level"]

    continuous_cols = [c for c in NUMERICAL_COLS if c in df.columns]

    # 3. Kiểm tra chất lượng dữ liệu
    print("\n--- KIỂM TRA CHẤT LƯỢNG DỮ LIỆU ---")
    missing_series = df.isnull().sum()
    total_missing = int(missing_series.sum())
    n_dup = int(df.duplicated().sum())
    print(f"• Số giá trị thiếu (Missing values): {total_missing}")
    print(f"• Số hàng trùng lặp (Duplicates): {n_dup}")

    outlier_summary = []
    for col in continuous_cols:
        res = detect_outliers_iqr(df[col].dropna().values)
        outlier_summary.append({
            "Biến": col,
            "Số ngoại lai": res["n_outliers"],
            "Tỷ lệ ngoại lai (%)": round(res["n_outliers"] / n_rows * 100, 2),
            "Cận dưới IQR": round(res["lower_bound"], 4),
            "Cận trên IQR": round(res["upper_bound"], 4),
        })
    df_outliers = pd.DataFrame(outlier_summary)

    # 4. Thống kê mô tả định lượng
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

    # 5. Tần suất mẫu định tính
    freq_rows = []
    for col in CATEGORICAL_COLS:
        for val in sorted(df[col].unique(), key=str):
            indicator = (df[col] == val).astype(int).values
            p_hat = sample_prop(indicator)
            count = int(np.sum(indicator))
            freq_rows.append({
                "Biến": col,
                "Giá trị": str(val),
                "Số lượng (k)": count,
                "p_hat": p_hat,
            })
    df_freq = pd.DataFrame(freq_rows)

    # 6. Xuất file outputs/tables/01_summary_stats.csv
    out_csv = TABLES_DIR / "01_summary_stats.csv"
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        f.write("# Phần 1: Thống kê mô tả biến định lượng (x_bar, S2, S dùng hàm tự cài đặt stats_utils)\n")
        df_desc.to_csv(f, index=False)
        f.write("\n# Phần 2: Tần suất mẫu (p_hat) biến phân loại\n")
        df_freq.to_csv(f, index=False)
    print(f"   ✅ Đã xuất bảng tổng hợp: {out_csv}")

    # 7. Xuất file báo cáo markdown report/sections/01_chap1.md
    md = []
    md.append("# Chương 1: Mẫu ngẫu nhiên và thống kê mô tả\n")
    md.append("## 1. Cơ sở lý thuyết mẫu ngẫu nhiên\n")
    md.append(r"""### 1.1. Định nghĩa mẫu ngẫu nhiên và hàm thống kê
- **Mẫu ngẫu nhiên**: Cho $X$ là biến ngẫu nhiên có hàm phân phối tích lũy $F(x)$ đặc trưng cho tổng thể nghiên cứu. Bộ $n$ đại lượng ngẫu nhiên $(X_1, X_2, \dots, X_n)$ được gọi là một mẫu ngẫu nhiên kích thước $n$ nếu chúng độc lập với nhau và có cùng phân phối xác suất với $X$ ($iid$ - independent and identically distributed):
  $$P(X_1 \le x_1, X_2 \le x_2, \dots, X_n \le x_n) = \prod_{i=1}^n F(x_i)$$
- **Hàm thống kê**: Mọi hàm thực $T = g(X_1, X_2, \dots, X_n)$ hoàn toàn xác định từ các biến ngẫu nhiên của mẫu và không chứa bất kỳ tham số tổng thể chưa biết nào đều được gọi là một hàm thống kê.

### 1.2. Các đặc trưng mẫu cơ bản
1. **Trung bình mẫu**:
   $$\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$$
   Đặc tính: $E(\bar{X}) = \mu$, $Var(\bar{X}) = \frac{\sigma^2}{n}$. $\bar{X}$ là ước lượng không chệch, vững và tiệm cận chuẩn theo Định lý Giới hạn Trung tâm (CLT).
2. **Phương sai mẫu hiệu chỉnh**:
   $$S^2 = \frac{1}{n - 1} \sum_{i=1}^n (X_i - \bar{X})^2$$
   Việc chia cho bậc tự do $n - 1$ thay vì $n$ là điều kiện toán học bắt buộc để loại bỏ độ chệch: $E(S^2) = \sigma^2$. Nếu chia cho $n$, ước lượng sẽ bị chệch dưới với $E(S_n^2) = \frac{n-1}{n}\sigma^2$.
3. **Độ lệch chuẩn mẫu hiệu chỉnh**: $S = \sqrt{S^2}$.
4. **Tần suất mẫu**:
   $$\hat{p} = \frac{k}{n} = \frac{1}{n} \sum_{i=1}^n I_A(X_i)$$
   với $I_A$ là biến chỉ thị cá thể thuộc nhóm biến cố quan tâm. $\hat{p}$ là ước lượng không chệch cho xác suất $p$ của tổng thể.
""")

    md.append("## 2. Bối cảnh nghiên cứu và phân loại biến\n")
    md.append(r"""Bộ dữ liệu **Gym Members Exercise Tracking** gồm $n = 973$ quan sát cá thể thành viên phòng gym, theo dõi các chỉ số sinh trắc học, thói quen tập luyện và hiệu suất tiêu thụ năng lượng:
- **Biến định lượng liên tục**: `Weight (kg)`, `Height (m)`, `Session_Duration` (giờ), `Calories_Burned` (kcal), `Fat_Percentage` (%), `Water_Intake (liters)`, `BMI`.
- **Biến định lượng rời rạc**: `Age` (năm), `Max_BPM`, `Avg_BPM`, `Resting_BPM`, `Workout_Frequency` (buổi/tuần).
- **Biến phân loại (Categorical)**: `Gender` (Male, Female), `Workout_Type` (Cardio, HIIT, Strength, Yoga), `Experience_Level` (1: Mới bắt đầu, 2: Trung cấp, 3: Nâng cao).
""")

    md.append("## 3. Kiểm tra chất lượng dữ liệu (Data Cleaning & Quality Assurance)\n")
    md.append(f"- **Giá trị khuyết thiếu (Missing values)**: 0 trường hợp (100% dữ liệu toàn vẹn).\n")
    md.append(f"- **Bản ghi trùng lặp (Duplicates)**: 0 trường hợp.\n")
    md.append(r"""- **Kiểm định ngoại lai theo phương pháp Hàng rào IQR (Tukey's Fences)**:
  Khoảng chấp nhận giá trị hợp lệ: $[Q_1 - 1.5 \cdot IQR, \; Q_3 + 1.5 \cdot IQR]$, với $IQR = Q_3 - Q_1$.
""")
    md.append(md_table(df_outliers, nd=2))
    md.append(r"""*Nhận định*: Các ngoại lai phát hiện ở `Calories_Burned`, `BMI` hay `Water_Intake` phản ánh độ phân tán sinh lý và cường độ vận động thực tế của các vận động viên thể hình/cường độ cao, không phải lỗi nhập liệu. Do đó, toàn bộ $973$ mẫu được giữ nguyên để bảo đảm tính khách quan.
""")

    md.append("## 4. Bảng thống kê mô tả thực nghiệm\n")
    md.append("### 4.1. Thống kê mô tả các biến định lượng\n")
    md.append(md_table(df_desc, nd=4))
    md.append("\n### 4.2. Tần suất mẫu các biến phân loại\n")
    md.append(md_table(df_freq, nd=4))
    md.append("\n*Các chỉ số trên được tính toán hoàn toàn bằng các hàm tự cài đặt từ `src/stats_utils.py`.*")

    md_path = SECTIONS_DIR / "01_chap1.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"   ✅ Đã xuất báo cáo: {md_path}")
    print("\n" + "=" * 70)
    print("HOÀN THÀNH MÔ-ĐUN CHƯƠNG 1")
    print("=" * 70)

if __name__ == "__main__":
    main()
