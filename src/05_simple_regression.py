"""
Chương 4.1 — Hồi quy tuyến tính đơn (Mô hình & Suy luận)
===========================================================
Tác giả : Nguyễn Thị Thảo (Owner) — Reviewer: Khánh
Mô-đun  : src/05_simple_regression.py
Outputs :
    - outputs/figures/05_slr_bands.png
    - report/sections/05_chap4_slr.md

─────────────────────────────────────────────────────────────
LÝ THUYẾT & NỀN TẢNG TOÁN HỌC (Định lý 1, 3, 4, 5, 6, 7, 8)
─────────────────────────────────────────────────────────────
1. Mô hình Hồi quy tuyến tính đơn (Simple Linear Regression - SLR):
       Y = β₀ + β₁·X + ε

   Giả thiết 1 (Classical Assumptions - Gauss-Markov):
       (a) E(εᵢ) = 0 với mọi i = 1, 2, ..., n.
       (b) Var(εᵢ) = σ² (phương sai thuần nhất - Homoscedasticity).
       (c) Cov(εᵢ, εⱼ) = 0 với mọi i ≠ j (các sai số không tương quan).
       (d) Phân phối chuẩn: εᵢ ~ N(0, σ²) độc lập.

2. Ước lượng Bình phương nhỏ nhất (OLS - Ordinary Least Squares):
   Cực tiểu hóa hàm tổng bình phương sai số:
       L(β₀, β₁) = Σᵢ₌₁ⁿ (yᵢ − β₀ − β₁·xᵢ)²
   Hệ phương trình chuẩn:
       ∂L/∂β₀ = 0  và  ∂L/∂β₁ = 0
   Nghiệm OLS (Định lý 1 - BLUE):
       β̂₁ = S_xy / S_xx
       β̂₀ = ȳ − β̂₁·x̄
   trong đó:
       S_xx = Σ (xᵢ − x̄)² = Σ xᵢ² − n·x̄²
       S_yy = Σ (yᵢ − ȳ)² = Σ yᵢ² − n·ȳ²
       S_xy = Σ (xᵢ − x̄)(yᵢ − ȳ) = Σ xᵢ·yᵢ − n·x̄·ȳ

3. Phân phối của các ước lượng (Định lý 3 & 4):
       β̂₁ ~ N(β₁,  σ² / S_xx)
       β̂₀ ~ N(β₀,  σ²·[1/n + x̄² / S_xx])
       Cov(β̂₀, β̂₁) = −x̄·σ² / S_xx
   Ước lượng không chệch cho σ² (Định lý 4):
       s² = MSE = SSE / (n − 2)
       SSE = S_yy − β̂₁·S_xy = Σ (yᵢ − ŷᵢ)²
       SSE / σ² ~ χ²(n − 2), độc lập với β̂₀ và β̂₁.

4. Phân tích phương sai hồi quy (ANOVA for Regression - Định lý 6):
       SST = SSR + SSE
       SSR = β̂₁·S_xy = β̂₁²·S_xx       (df = 1, MSR = SSR / 1)
       SSE = Σ eᵢ²                    (df = n − 2, MSE = s² = SSE / (n − 2))
       SST = S_yy                     (df = n − 1)
   Thống kê kiểm định F cho H₀: β₁ = 0 vs H₁: β₁ ≠ 0:
       f₀ = MSR / MSE ~ F(1, n − 2)

5. Kiểm định t cho hệ số góc (Định lý 5):
       t₀ = β̂₁ / se(β̂₁) = β̂₁ / [s / √S_xx] ~ t(n − 2)
   ★ TÍNH TƯƠNG ĐƯƠNG CỐT LÕI:
       t₀² = [β̂₁ / (s / √S_xx)]² = [β̂₁²·S_xx] / s² = SSR / s² = MSR / MSE = f₀
       Miền bác bỏ và P-value của t-test và F-test là hoàn toàn tương đương!

6. Khoảng tin cậy 95% (Định lý 7):
       KTC cho β₁:  β̂₁ ± t_{α/2, n-2} · se(β̂₁)
       KTC cho β₀:  β̂₀ ± t_{α/2, n-2} · se(β̂₀)
       KTC cho kỳ vọng phản hồi E(Y|x₀) = μ_{Y|x₀}:
           ŷ₀ ± t_{α/2, n-2} · s · √[1/n + (x₀ − x̄)² / S_xx]

7. Khoảng dự đoán 95% cho giá trị mới y₀ tại x₀ (Định lý 8):
           ŷ₀ ± t_{α/2, n-2} · s · √[1 + 1/n + (x₀ − x̄)² / S_xx]
   ★ Khoảng dự đoán LUÔN RỘNG HƠN KTC vì có thêm số hạng '+1'
     bên trong căn bậc hai, phản ánh độ biến thiên ngẫu nhiên tự nhiên
     của chính cá thể mới (Var(y₀ − ŷ₀) = Var(ŷ₀) + Var(ε₀) = Var(ŷ₀) + σ²).
─────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend không cần giao diện cửa sổ
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Thêm thư mục gốc vào sys.path để import stats_utils
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.stats_utils import (
    load_data,
    sample_mean,
    sample_var,
    sample_std,
    simple_ols,
    fmt,
    md_table,
    TABLES_DIR,
    FIGURES_DIR,
    SECTIONS_DIR,
)

# scipy.stats CHỈ dùng để tra giá trị tới hạn và tính P-value
from scipy import stats as sp_stats

# ============================================================================
# 1. ĐỌC DỮ LIỆU & CHUẨN BỊ BIẾN
# ============================================================================
print("=" * 70)
print("CHƯƠNG 4.1 — HỒI QUY TUYẾN TÍNH ĐƠN (MÔ HÌNH & SUY LUẬN)")
print("=" * 70)

df = load_data()
x = df["Session_Duration"].values
y = df["Calories_Burned"].values
n = len(df)
alpha = 0.05

print(f"\n[INFO] Dữ liệu phân tích hồi quy đơn:")
print(f"   • Biến độc lập (X): Session_Duration (thời lượng buổi tập, giờ)")
print(f"   • Biến phụ thuộc (Y): Calories_Burned (lượng calo tiêu thụ, kcal)")
print(f"   • Cỡ mẫu n = {n}")

# ============================================================================
# 2. ƯỚC LƯỢNG OLS & CÁC ĐẠI LƯỢNG THỐNG KÊ MẪU
# ============================================================================
print("\n" + "-" * 70)
print("2. ƯỚC LƯỢNG OLS (TỰ CÀI ĐẶT CÔNG THỨC TOÁN)")
print("-" * 70)

ols = simple_ols(x, y)

xbar = sample_mean(x)
ybar = sample_mean(y)
b0 = ols["b0"]
b1 = ols["b1"]
sxx = ols["sxx"]
sxy = ols["sxy"]
syy = ols["syy"]
sse = ols["sse"]
ssr = ols["ssr"]
s2 = ols["s2"]
s = ols["s"]
r2 = ols["r2"]
r = ols["r"]

# Sai số chuẩn của các ước lượng hệ số
se_b1 = s / np.sqrt(sxx)
se_b0 = s * np.sqrt(1.0 / n + (xbar ** 2) / sxx)

print(f"   x̄ (TB Session_Duration) = {xbar:.4f} giờ")
print(f"   ȳ (TB Calories_Burned)  = {ybar:.4f} kcal")
print(f"   S_xx = {sxx:.4f}")
print(f"   S_yy = {syy:.4f}")
print(f"   S_xy = {sxy:.4f}")
print(f"\n   Phương trình hồi quy mẫu OLS:")
print(f"       Calories_Burned = {b0:.4f} + {b1:.4f} · Session_Duration")
print(f"       (se(β̂₀) = {se_b0:.4f},  se(β̂₁) = {se_b1:.4f})")
print(f"\n   Độ biến thiên & Sai số:")
print(f"   • SST = {syy:.4f}  (df = {n - 1})")
print(f"   • SSR = {ssr:.4f}  (df = 1)")
print(f"   • SSE = {sse:.4f}  (df = {n - 2})")
print(f"   • s² (MSE) = {s2:.4f}")
print(f"   • s (độ lệch chuẩn phần dư) = {s:.4f} kcal")
print(f"   • R² (hệ số xác định) = {r2:.4f} ({r2 * 100:.2f}%)")
print(f"   • r (hệ số tương quan mẫu) = {r:.4f}")

# ============================================================================
# 3. PHÂN TÍCH PHƯƠNG SAI HỒI QUY (ANOVA) & KIỂM ĐỊNH F
# ============================================================================
print("\n" + "-" * 70)
print("3. PHÂN TÍCH PHƯƠNG SAI HỒI QUY (ANOVA TABLE & F-TEST)")
print("-" * 70)

df_reg = 1
df_err = n - 2
df_tot = n - 1

msr = ssr / df_reg
mse = s2

f0 = msr / mse
f_crit = sp_stats.f.ppf(1 - alpha, df_reg, df_err)
p_val_f = 1 - sp_stats.f.cdf(f0, df_reg, df_err)

print(f"\n   ── BẢNG ANOVA HỒI QUY ──")
print(f"   {'Nguồn biến thiên':<20s} {'SS':>15s} {'df':>5s} {'MS':>15s} {'F₀':>10s} {'P-value':>12s}")
print(f"   {'─' * 80}")
print(f"   {'Hồi quy (SSR)':<20s} {ssr:>15.4f} {df_reg:>5d} {msr:>15.4f} {f0:>10.4f} {p_val_f:>12.4e}")
print(f"   {'Sai số (SSE)':<20s} {sse:>15.4f} {df_err:>5d} {mse:>15.4f}")
print(f"   {'Tổng cộng (SST)':<20s} {syy:>15.4f} {df_tot:>5d}")

print(f"\n   F-test cho H₀: β₁ = 0 vs H₁: β₁ ≠ 0:")
print(f"   • F_stat = {f0:.4f}")
print(f"   • F_critical = F({alpha}; {df_reg}, {df_err}) = {f_crit:.4f}")
print(f"   • P-value = {p_val_f:.6e}")
if f0 > f_crit:
    print(f"   → BÁC BỎ H₀ (F₀ = {f0:.4f} > F_crit = {f_crit:.4f}).")
    print(f"     Mối quan hệ tuyến tính giữa Session_Duration và Calories_Burned")
    print(f"     có ý nghĩa thống kê ở mức ý nghĩa α = {alpha}.")

# ============================================================================
# 4. KIỂM ĐỊNH T CHO HỆ SỐ GÓC & TÍNH TƯƠNG ĐƯƠNG t₀² = f₀
# ============================================================================
print("\n" + "-" * 70)
print("4. KIỂM ĐỊNH T & CHỨNG MINH TÍNH TƯƠNG ĐƯƠNG t₀² = f₀")
print("-" * 70)

t0 = b1 / se_b1
t_crit = sp_stats.t.ppf(1 - alpha / 2, df_err)
p_val_t = 2 * (1 - sp_stats.t.cdf(abs(t0), df_err))

print(f"   t-test cho H₀: β₁ = 0 vs H₁: β₁ ≠ 0:")
print(f"   • t₀ = β̂₁ / se(β̂₁) = {b1:.4f} / {se_b1:.4f} = {t0:.4f}")
print(f"   • t_critical = t({alpha/2}; {df_err}) = {t_crit:.4f}")
print(f"   • P-value = {p_val_t:.6e}")
if abs(t0) > t_crit:
    print(f"   → BÁC BỎ H₀ (|t₀| = {abs(t0):.4f} > t_crit = {t_crit:.4f}).")

print(f"\n   ★ SO SÁNH t-test VÀ F-test (Định lý phân phối):")
print(f"   • t₀² = ({t0:.4f})² = {t0**2:.4f}")
print(f"   • f₀  = {f0:.4f}")
print(f"   • Hiệu tuyệt đối: |t₀² − f₀| = {abs(t0**2 - f0):.2e}")
print(f"   • (t_crit)² = ({t_crit:.4f})² = {t_crit**2:.4f}  vs  F_crit = {f_crit:.4f}")
print(f"   → Hai kiểm định HOÀN TOÀN TƯƠNG ĐƯƠNG trong hồi quy tuyến tính đơn!")

# ============================================================================
# 5. KHOẢNG TIN CẬY 95% CHO CÁC HỆ SỐ
# ============================================================================
print("\n" + "-" * 70)
print("5. KHOẢNG TIN CẬY 95% CHO CÁC THAM SỐ")
print("-" * 70)

# KTC cho beta1
ci_b1_lower = b1 - t_crit * se_b1
ci_b1_upper = b1 + t_crit * se_b1

# KTC cho beta0
ci_b0_lower = b0 - t_crit * se_b0
ci_b0_upper = b0 + t_crit * se_b0

print(f"   • KTC 95% cho hệ số góc β₁:")
print(f"     [{ci_b1_lower:.4f},  {ci_b1_upper:.4f}] kcal/giờ")
print(f"     (Ý nghĩa: Khi tăng thời lượng tập thêm 1 giờ, lượng calo tiêu thụ")
print(f"      trung bình tăng trong khoảng từ {ci_b1_lower:.2f} đến {ci_b1_upper:.2f} kcal)")

print(f"\n   • KTC 95% cho hệ số chặn β₀:")
print(f"     [{ci_b0_lower:.4f},  {ci_b0_upper:.4f}] kcal")
print(f"     (KTC chứa giá trị 0, phù hợp với thực tế khi không tập luyện)")

# ============================================================================
# 6. DẢI KHOẢNG TIN CẬY & DẢI DỰ ĐOÁN (BANDS)
# ============================================================================
print("\n" + "-" * 70)
print("6. TÍNH DẢI KTC VÀ DẢI DỰ ĐOÁN TẠI CÁC ĐIỂM TIÊU BIỂU")
print("-" * 70)

# Chọn một số giá trị x0 thực tế để in bảng minh họa
x0_samples = np.array([0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])
sample_rows = []

for x0 in x0_samples:
    y_hat_0 = b0 + b1 * x0
    # Phương sai ước lượng kỳ vọng phản hồi: s² * [1/n + (x0 - xbar)² / Sxx]
    se_mean = s * np.sqrt(1.0 / n + ((x0 - xbar) ** 2) / sxx)
    ci_mean_low = y_hat_0 - t_crit * se_mean
    ci_mean_upp = y_hat_0 + t_crit * se_mean

    # Phương sai sai số dự đoán: s² * [1 + 1/n + (x0 - xbar)² / Sxx]
    se_pred = s * np.sqrt(1.0 + 1.0 / n + ((x0 - xbar) ** 2) / sxx)
    pi_pred_low = y_hat_0 - t_crit * se_pred
    pi_pred_upp = y_hat_0 + t_crit * se_pred

    sample_rows.append({
        "x0 (giờ)": x0,
        "ŷ₀ (dự báo)": y_hat_0,
        "se(Mean)": se_mean,
        "KTC 95% (Kỳ vọng E[Y])": f"[{ci_mean_low:.2f}, {ci_mean_upp:.2f}]",
        "Độ rộng KTC": ci_mean_upp - ci_mean_low,
        "se(Pred)": se_pred,
        "Khoảng dự đoán 95% (Cá thể y₀)": f"[{pi_pred_low:.2f}, {pi_pred_upp:.2f}]",
        "Độ rộng KDĐ": pi_pred_upp - pi_pred_low,
    })

df_bands_sample = pd.DataFrame(sample_rows)
print(df_bands_sample.to_string(index=False))

# ============================================================================
# 7. VẼ ĐỒ THỊ SCATTER PLOT, DẢI KTC VÀ DẢI DỰ ĐOÁN
# ============================================================================
print("\n" + "-" * 70)
print("7. VẼ ĐỒ THỊ HỒI QUY & DẢI DỰ ĐOÁN (05_slr_bands.png)")
print("-" * 70)

# Tạo lưới x0 mịn để vẽ đường cong
x_grid = np.linspace(np.min(x) - 0.05, np.max(x) + 0.05, 500)
y_hat_grid = b0 + b1 * x_grid

# Dải tin cậy cho kỳ vọng E(Y|x0)
se_mean_grid = s * np.sqrt(1.0 / n + ((x_grid - xbar) ** 2) / sxx)
ci_lower = y_hat_grid - t_crit * se_mean_grid
ci_upper = y_hat_grid + t_crit * se_mean_grid

# Dải dự đoán cho cá thể mới y0
se_pred_grid = s * np.sqrt(1.0 + 1.0 / n + ((x_grid - xbar) ** 2) / sxx)
pi_lower = y_hat_grid - t_crit * se_pred_grid
pi_upper = y_hat_grid + t_crit * se_pred_grid

fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

# 1. Điểm dữ liệu quan sát
ax.scatter(
    x, y,
    alpha=0.45,
    color="#1f77b4",
    edgecolors="none",
    s=25,
    label=f"Quan sát thực tế (n = {n})"
)

# 2. Dải dự đoán cá thể (Prediction Band - màu cam nhạt)
ax.fill_between(
    x_grid, pi_lower, pi_upper,
    color="#ff7f0e", alpha=0.18,
    label="Dải dự đoán 95% (Cá thể mới $y_0$)"
)
ax.plot(x_grid, pi_lower, color="#d95f02", linestyle="--", linewidth=1.2)
ax.plot(x_grid, pi_upper, color="#d95f02", linestyle="--", linewidth=1.2)

# 3. Dải tin cậy kỳ vọng (Confidence Band - màu xanh lá nhạt)
ax.fill_between(
    x_grid, ci_lower, ci_upper,
    color="#2ca02c", alpha=0.35,
    label="Dải tin cậy 95% (Kỳ vọng $E[Y|x_0]$)"
)
ax.plot(x_grid, ci_lower, color="#1b9e77", linestyle=":", linewidth=1.2)
ax.plot(x_grid, ci_upper, color="#1b9e77", linestyle=":", linewidth=1.2)

# 4. Đường hồi quy OLS
ax.plot(
    x_grid, y_hat_grid,
    color="#d62728", linewidth=2.0,
    label=f"Đường hồi quy OLS: $\\hat{{y}} = {b0:.2f} + {b1:.2f}x$"
)

# 5. Điểm trọng tâm mẫu (x̄, ȳ)
ax.scatter([xbar], [ybar], color="black", s=70, zorder=5, marker="D",
           label=f"Trọng tâm mẫu $(\\bar{{x}}={xbar:.2f}, \\bar{{y}}={ybar:.1f})$")

# Chú thích thông số mô hình
info_text = (
    f"Mô hình: $\\hat{{Y}} = {b0:.2f} + {b1:.2f}X$\n"
    f"$R^2 = {r2:.4f}$ ($r = {r:.4f}$)\n"
    f"$s = {s:.2f}$ kcal\n"
    f"$F_0 = {f0:.1f}$ ($P < 10^{{-15}}$)\n"
    f"$t_0 = {t0:.1f}$ ($t_0^2 = F_0$)"
)
ax.text(
    0.05, 0.95, info_text,
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#cccccc", alpha=0.9)
)

ax.set_title(
    "HỒI QUY TUYẾN TÍNH ĐƠN: CALORIES_BURNED ~ SESSION_DURATION\n"
    "Dải khoảng tin cậy 95% cho kỳ vọng và Dải dự đoán 95% cho cá thể mới",
    fontsize=12, fontweight="bold", pad=12
)
ax.set_xlabel("Thời lượng buổi tập — Session_Duration (giờ)", fontsize=11, fontweight="bold")
ax.set_ylabel("Lượng calo tiêu thụ — Calories_Burned (kcal)", fontsize=11, fontweight="bold")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="lower right", framealpha=0.9, fontsize=9)

plt.tight_layout()
fig_path = FIGURES_DIR / "05_slr_bands.png"
plt.savefig(fig_path, dpi=300)
plt.close()
print(f"   ✅ Đã lưu đồ thị tại: {fig_path}")

# ============================================================================
# 8. XUẤT BẢNG TỔNG HỢP & BÁO CÁO MARKDOWN
# ============================================================================
print("\n" + "-" * 70)
print("8. XUẤT BÁO CÁO MARKDOWN (05_chap4_slr.md)")
print("-" * 70)

# Tạo bảng tổng hợp các chỉ số
summary_table = pd.DataFrame([
    {"Chỉ số": "Cỡ mẫu (n)", "Giá trị": str(n), "Ý nghĩa": "Số quan sát thành viên phòng gym"},
    {"Chỉ số": "Hệ số chặn (β̂₀)", "Giá trị": f"{b0:.4f}", "Ý nghĩa": f"se = {se_b0:.4f}, KTC 95%: [{ci_b0_lower:.2f}, {ci_b0_upper:.2f}]"},
    {"Chỉ số": "Hệ số góc (β̂₁)", "Giá trị": f"{b1:.4f}", "Ý nghĩa": f"se = {se_b1:.4f}, KTC 95%: [{ci_b1_lower:.2f}, {ci_b1_upper:.2f}]"},
    {"Chỉ số": "Hệ số xác định (R²)", "Giá trị": f"{r2:.4f}", "Ý nghĩa": "82.47% biến thiên calo giải thích bởi thời lượng tập"},
    {"Chỉ số": "Hệ số tương quan (r)", "Giá trị": f"{r:.4f}", "Ý nghĩa": "Tương quan tuyến tính đồng biến rất mạnh"},
    {"Chỉ số": "Độ lệch chuẩn phần dư (s)", "Giá trị": f"{s:.4f}", "Ý nghĩa": "Độ biến thiên không được giải thích bởi mô hình"},
    {"Chỉ số": "Thống kê t (t₀)", "Giá trị": f"{t0:.4f}", "Ý nghĩa": f"t_crit = {t_crit:.4f}, P < 10⁻¹⁵ (Bác bỏ H₀)"},
    {"Chỉ số": "Thống kê F (F₀)", "Giá trị": f"{f0:.4f}", "Ý nghĩa": f"F_crit = {f_crit:.4f}, P < 10⁻¹⁵ (F₀ = t₀²)"},
])

out_summary_csv = TABLES_DIR / "05_regression_summary.csv"
summary_table.to_csv(out_summary_csv, index=False, encoding="utf-8-sig")
print(f"   ✅ {out_summary_csv}")

# Viết báo cáo chi tiết Markdown
md = []
md.append("# Chương 4.1 — Hồi quy tuyến tính đơn (Mô hình & Suy luận)\n")

md.append("## 1. Cơ sở lý thuyết & Mô hình toán học\n")
md.append("""### 1.1. Phương trình mô hình và Giả thiết 1

Mô hình Hồi quy tuyến tính đơn tổng thể:
$$Y = \\beta_0 + \\beta_1 X + \\varepsilon$$

trong đó:
- $Y$: Biến phụ thuộc (`Calories_Burned`, lượng calo tiêu thụ, kcal).
- $X$: Biến độc lập (`Session_Duration`, thời lượng tập luyện, giờ).
- $\\beta_0$: Hệ số chặn (intercept).
- $\\beta_1$: Hệ số góc (slope) — độ dốc thể hiện mức thay đổi trung bình của $Y$ khi $X$ tăng 1 đơn vị.
- $\\varepsilon$: Sai số ngẫu nhiên thỏa mãn **Giả thiết 1 (Gauss-Markov)**:
  1. $E(\\varepsilon_i) = 0$ với mọi $i = 1, \\ldots, n$.
  2. $Var(\\varepsilon_i) = \\sigma^2$ (phương sai thuần nhất, homoscedasticity).
  3. $Cov(\\varepsilon_i, \\varepsilon_j) = 0$ với mọi $i \\neq j$ (sai số độc lập).
  4. $\\varepsilon_i \\sim N(0, \\sigma^2)$ độc lập cùng phân phối.

### 1.2. Phương pháp ước lượng Bình phương nhỏ nhất (OLS - Định lý 1)

Cực tiểu hóa hàm mục tiêu:
$$L(\\beta_0, \\beta_1) = \\sum_{i=1}^{n} (y_i - \\beta_0 - \\beta_1 x_i)^2$$

Nghiệm OLS:
$$\\hat{\\beta}_1 = \\frac{S_{xy}}{S_{xx}} = \\frac{\\sum (x_i - \\bar{x})(y_i - \\bar{y})}{\\sum (x_i - \\bar{x})^2}$$
$$\\hat{\\beta}_0 = \\bar{y} - \\hat{\\beta}_1 \\bar{x}$$

Theo Định lý Gauss-Markov, $\\hat{\\beta}_0$ và $\\hat{\\beta}_1$ là các **ước lượng tuyến tính không chệch tốt nhất (BLUE)**.

### 1.3. Phân phối xác suất của ước lượng và ước lượng phương sai sai số (Định lý 3 & 4)

- $\\hat{\\beta}_1 \\sim N\\left(\\beta_1, \\frac{\\sigma^2}{S_{xx}}\\right)$, suy ra $se(\\hat{\\beta}_1) = \\frac{s}{\\sqrt{S_{xx}}}$.
- $\\hat{\\beta}_0 \\sim N\\left(\\beta_0, \\sigma^2 \\left[\\frac{1}{n} + \\frac{\\bar{x}^2}{S_{xx}}\\right]\\right)$, suy ra $se(\\hat{\\beta}_0) = s \\sqrt{\\frac{1}{n} + \\frac{\\bar{x}^2}{S_{xx}}}$.
- Ước lượng không chệch cho $\\sigma^2$:
  $$s^2 = MSE = \\frac{SSE}{n - 2} = \\frac{S_{yy} - \\hat{\\beta}_1 S_{xy}}{n - 2}$$
  và $\\frac{(n-2)s^2}{\\sigma^2} \\sim \\chi^2(n - 2)$, độc lập với $\\hat{\\beta}_0, \\hat{\\beta}_1$.
""")

md.append("## 2. Kết quả ước lượng mô hình thực nghiệm\n")
md.append("- **Phương trình hồi quy OLS**:")
md.append(r"$$\widehat{\text{Calories\_Burned}} = " + f"{b0:.4f} + {b1:.4f}" + r" \times \text{Session\_Duration}$$")
md.append(f"- Hệ số chặn: $\\hat{{\\beta}}_0 = {b0:.4f}$ (se = {se_b0:.4f})")
md.append(f"- Hệ số góc: $\\hat{{\\beta}}_1 = {b1:.4f}$ (se = {se_b1:.4f})")
md.append(f"- Hệ số xác định: $R^2 = {r2:.4f}$ ({r2*100:.2f}%)")
md.append(f"- Hệ số tương quan: $r = {r:.4f}$ (tương quan tuyến tính đồng biến rất mạnh)")
md.append(f"- Độ lệch chuẩn phần dư: $s = {s:.4f}$ kcal\n")

md.append("### Bảng tổng hợp các chỉ số mô hình\n")
md.append(md_table(summary_table, nd=4))
md.append("")

md.append("## 3. Phân tích phương sai hồi quy (ANOVA) & Kiểm định giả thuyết\n")
md.append("### 3.1. Bảng ANOVA hồi quy (Định lý 6)\n")
anova_reg_df = pd.DataFrame([
    {"Nguồn biến thiên": "Hồi quy (SSR)", "SS": ssr, "df": df_reg, "MS": msr, "F₀": f0, "P-value": p_val_f},
    {"Nguồn biến thiên": "Sai số (SSE)", "SS": sse, "df": df_err, "MS": mse, "F₀": "", "P-value": ""},
    {"Nguồn biến thiên": "Tổng cộng (SST)", "SS": syy, "df": df_tot, "MS": "", "F₀": "", "P-value": ""},
])
md.append(md_table(anova_reg_df, nd=4))
md.append(f"\n- $F_0 = {f0:.4f} > F_{{0.05; 1, {df_err}}} = {f_crit:.4f}$")
md.append(f"- $P\\text{{-value}} = {p_val_f:.6e} < 0.05$ $\\rightarrow$ **Bác bỏ $H_0$**.\n")

md.append("""### 3.2. Kiểm định t cho hệ số góc (Định lý 5) và Tính tương đương $t_0^2 = f_0$

Kiểm định giả thuyết:
- $H_0: \\beta_1 = 0$ (thời lượng tập không có ảnh hưởng tuyến tính lên lượng calo tiêu thụ).
- $H_1: \\beta_1 \\neq 0$.

Thống kê kiểm định:
$$t_0 = \\frac{\\hat{\\beta}_1}{se(\\hat{\\beta}_1)} = \\frac{721.7860}{10.6786} = 67.5919$$
Giá trị tới hạn hai phía $t_{0.025; 971} = 1.9624$, $P\\text{-value} < 10^{-15}$.

**Chứng minh tính tương đương $t_0^2 = f_0$:**
$$t_0^2 = \\left(\\frac{\\hat{\\beta}_1}{s / \\sqrt{S_{xx}}}\\right)^2 = \\frac{\\hat{\\beta}_1^2 S_{xx}}{s^2} = \\frac{SSR}{s^2} = \\frac{MSR}{MSE} = f_0$$
$$t_0^2 = 67.5919^2 = 4568.6744 = f_0$$
Theo lý thuyết xác suất, nếu $T \\sim t(\\nu)$ thì $T^2 \\sim F(1, \\nu)$. Do đó, trong hồi quy tuyến tính đơn (1 biến độc lập), kiểm định $t$ và kiểm định $F$ là **hoàn toàn tương đương** về miền bác bỏ và $P$-giá trị.
""")

md.append("## 4. Khoảng tin cậy & Khoảng dự đoán (Định lý 7 & 8)\n")
md.append("### 4.1. Khoảng tin cậy 95% cho các tham số\n")
md.append(f"- **Hệ số góc $\\beta_1$**: [{ci_b1_lower:.4f}, {ci_b1_upper:.4f}] kcal/giờ.")
md.append(f"- **Hệ số chặn $\\beta_0$**: [{ci_b0_lower:.4f}, {ci_b0_upper:.4f}] kcal.\n")
md.append(r"""### 4.2. So sánh Dải Khoảng tin cậy cho $E[Y|x_0]$ và Dải Dự đoán cho cá thể $y_0$
- **KTC 95% cho kỳ vọng phản hồi**:
  $$\hat{y}_0 \pm t_{\alpha/2, n-2} \cdot s \sqrt{\frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$
- **Khoảng dự đoán 95% cho quan sát mới $y_0$**:
  $$\hat{y}_0 \pm t_{\alpha/2, n-2} \cdot s \sqrt{1 + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$

**Tại sao Khoảng dự đoán luôn rộng hơn Khoảng tin cậy?**
Sai số dự đoán $y_0 - \hat{y}_0$ chịu ảnh hưởng của hai nguồn bất định độc lập:
1. Sai số ước lượng mặt phẳng hồi quy: $Var(\hat{y}_0) = s^2 \left[\frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}\right]$.
2. Độ biến thiên tự nhiên ngẫu nhiên của chính cá thể mới: $Var(\varepsilon_0) = \sigma^2$ (ước lượng bằng $s^2$).
Do đó:
$$Var(y_0 - \hat{y}_0) = Var(\hat{y}_0) + Var(\varepsilon_0) = s^2 \left[1 + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}\right]$$
Số hạng **`+1`** bên trong dấu căn khiến phương sai dự đoán luôn lớn hơn phương sai ước lượng kỳ vọng đúng một lượng bằng $s^2$.
""")

md.append("### 4.3. Bảng giá trị KTC và Khoảng dự đoán tại các mốc thời lượng tập tiêu biểu\n")
md.append(md_table(df_bands_sample, nd=2))
md.append("")

md.append("""## 5. Ý nghĩa thực tế của hệ số chặn $\\hat{\\beta}_0$

- **Về mặt thực tế**: Trong bộ dữ liệu, thời lượng buổi tập quan sát dao động từ $0.5$ đến $2.0$ giờ. Không có cá thể nào tập $0$ giờ. Việc diễn giải máy móc "tập 0 giờ tiêu thụ $-1.45$ calo" là phép ngoại suy không có căn cứ (Extrapolation) và không có ý nghĩa thực tế.
- **Về mặt toán học**: $\\hat{\\beta}_0$ đóng vai trò "mỏ neo" bắt buộc để:
  1. Đảm bảo tổng phần dư $\\sum_{i=1}^n e_i = 0$.
  2. Đảm bảo đường hồi quy luôn đi qua điểm trọng tâm mẫu $(\\bar{x}, \\bar{y})$.
  3. Bảo toàn phân rã phương sai $SST = SSR + SSE$ và định nghĩa hệ số xác định $R^2 = SSR / SST$.
Nếu ép $\\beta_0 = 0$ (mô hình qua gốc tọa độ), ước lượng $\\hat{\\beta}_1$ sẽ bị chệch nghiêm trọng và các công thức phân tích phương sai thông thường không còn hợp lệ.

## 6. Đồ thị hồi quy thực nghiệm
Đồ thị thể hiện dữ liệu quan sát, đường hồi quy OLS, dải tin cậy 95% và dải dự đoán 95% được lưu tại:
`outputs/figures/05_slr_bands.png`
""")

md_path = SECTIONS_DIR / "05_chap4_slr.md"
md_path.write_text("\n".join(md), encoding="utf-8")
print(f"   ✅ Đã ghi báo cáo tại: {md_path}")

print("\n" + "=" * 70)
print("HOÀN THÀNH CHƯƠNG 4.1 (HỒI QUY TUYẾN TÍNH ĐƠN)")
print("=" * 70)
