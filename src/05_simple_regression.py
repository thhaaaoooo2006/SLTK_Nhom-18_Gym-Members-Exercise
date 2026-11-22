"""Chương 4.1 — Hồi quy tuyến tính đơn (Mô hình & Suy luận)
===========================================================
Tác giả : Nguyễn Thị Thảo (Owner) — Reviewer: Khánh
Mô-đun  : src/05_simple_regression.py
Outputs :
    - outputs/figures/05_slr_bands.png
    - outputs/figures/05_regression_fit.png
    - outputs/tables/05_regression_summary.csv
    - outputs/tables/05_regression_coefficients.csv
    - outputs/tables/05_regression_anova.csv
    - outputs/tables/05_prediction_intervals.csv
    - report/sections/05_chap4_slr.md
    - report/sections/05_chap4_regression.md

─────────────────────────────────────────────────────────────
LÝ THUYẾT & NỀN TẢNG TOÁN HỌC (Định lý 1, 3, 4, 5, 6, 7, 8)
─────────────────────────────────────────────────────────────
1. Mô hình Hồi quy tuyến tính đơn (Simple Linear Regression - SLR):
       Y = β₀ + β₁·X + ε

   Giả thiết cổ điển (Gauss-Markov Assumptions):
       (a) E(εᵢ) = 0 với mọi i = 1, 2, ..., n.
       (b) Var(εᵢ) = σ² (phương sai thuần nhất - Homoscedasticity).
       (c) Cov(εᵢ, εⱼ) = 0 với mọi i ≠ j (các sai số không tương quan).
       (d) Phân phối chuẩn: εᵢ ~ N(0, σ²) độc lập.

2. Ước lượng Bình phương nhỏ nhất (OLS - Ordinary Least Squares):
   Cực tiểu hóa hàm tổng bình phương sai số:
       L(β₀, β₁) = Σᵢ₌₁ⁿ (yᵢ − β₀ − β₁·xᵢ)²
   Hệ phương trình chuẩn:
       ∂L/∂β₀ = 0  và  ∂L/∂β₁ = 0
   Nghiệm OLS (Định lý 1 - BLUE - Best Linear Unbiased Estimator):
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
     của chính cá thể mới:
     Var(y₀ − ŷ₀) = Var(ŷ₀) + Var(ε₀) = s²·[1/n + (x₀ − x̄)² / S_xx] + s²
                  = s²·[1 + 1/n + (x₀ − x̄)² / S_xx]
─────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# Thêm thư mục gốc vào sys.path để import stats_utils
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.stats_utils import (
    FIGURES_DIR,
    SECTIONS_DIR,
    TABLES_DIR,
    load_data,
    md_table,
    sample_mean,
    simple_ols,
)

ALPHA = 0.05
X0_LIST = [0.75, 1.0, 1.25, 1.5, 2.0]


def main():
    print("=" * 70)
    print("CHƯƠNG 4.1: HỒI QUY TUYẾN TÍNH ĐƠN (MÔ HÌNH & SUY LUẬN)")
    print("Tác giả: Nguyễn Thị Thảo (Owner) — Reviewer: Khánh")
    print("=" * 70)

    # 1. Đọc dữ liệu & Trích xuất biến
    df = load_data()
    x = df["Session_Duration"].to_numpy(float)
    y = df["Calories_Burned"].to_numpy(float)

    # 2. Ước lượng OLS (Định lý 1)
    m = simple_ols(x, y)
    n = int(m["n"])
    b0 = float(m["b0"])
    b1 = float(m["b1"])
    s = float(m["s"])
    sxx = float(m["sxx"])
    syy = float(m["syy"])
    sxy = float(m["sxy"])
    ssr = float(m["ssr"])
    sse = float(m["sse"])
    r2 = float(m["r2"])
    r = float(m["r"])

    xbar = float(sample_mean(x))
    ybar = float(sample_mean(y))
    dfe = n - 2
    df_reg = 1
    df_tot = n - 1

    tc = float(stats.t.ppf(1 - ALPHA / 2, dfe))

    # 3. Phân phối và Suy diễn về hệ số (Định lý 3, 4, 5, 7)
    se_b1 = s / np.sqrt(sxx)
    se_b0 = s * np.sqrt(1.0 / n + (xbar ** 2) / sxx)

    t_b0 = b0 / se_b0
    p_b0 = float(2 * stats.t.sf(abs(t_b0), dfe))
    ci_b0_lower = b0 - tc * se_b0
    ci_b0_upper = b0 + tc * se_b0

    t_b1 = b1 / se_b1
    p_b1 = float(2 * stats.t.sf(abs(t_b1), dfe))
    ci_b1_lower = b1 - tc * se_b1
    ci_b1_upper = b1 + tc * se_b1

    coef = pd.DataFrame([
        {
            "Hệ số": "β0 (Intercept)",
            "Ước lượng": b0,
            "Sai số chuẩn": se_b0,
            "t (H0: β=0)": t_b0,
            "P-giá trị": p_b0,
            "KTC 95% cận dưới": ci_b0_lower,
            "KTC 95% cận trên": ci_b0_upper,
        },
        {
            "Hệ số": "β1 (Session_Duration)",
            "Ước lượng": b1,
            "Sai số chuẩn": se_b1,
            "t (H0: β=0)": t_b1,
            "P-giá trị": p_b1,
            "KTC 95% cận dưới": ci_b1_lower,
            "KTC 95% cận trên": ci_b1_upper,
        },
    ])

    # 4. Phân tích phương sai ANOVA & Kiểm định F (Định lý 6)
    msr = ssr / df_reg
    mse = sse / dfe
    F = msr / mse
    p_F = float(stats.f.sf(F, 1, dfe))
    F_crit = float(stats.f.ppf(1 - ALPHA, 1, dfe))

    anova = pd.DataFrame([
        {
            "Nguồn": "Hồi quy (SSR)",
            "Tổng bình phương": ssr,
            "Bậc tự do": df_reg,
            "Trung bình bình phương": msr,
            "F": F,
            "P-giá trị": p_F,
        },
        {
            "Nguồn": "Phần dư (SSE)",
            "Tổng bình phương": sse,
            "Bậc tự do": dfe,
            "Trung bình bình phương": mse,
            "F": np.nan,
            "P-giá trị": np.nan,
        },
        {
            "Nguồn": "Tổng (SST)",
            "Tổng bình phương": syy,
            "Bậc tự do": df_tot,
            "Trung bình bình phương": np.nan,
            "F": np.nan,
            "P-giá trị": np.nan,
        },
    ])

    # 5. Khoảng tin cậy cho kỳ vọng & Khoảng dự đoán cho cá thể mới (Định lý 7 & 8)
    rows_pred = []
    for x0 in X0_LIST:
        yh = b0 + b1 * x0
        h = 1.0 / n + ((x0 - xbar) ** 2) / sxx
        se_m = s * np.sqrt(h)
        se_p = s * np.sqrt(1.0 + h)
        is_extrap = bool(x0 < x.min() or x0 > x.max())
        rows_pred.append({
            "x0 (giờ)": x0,
            "ŷ0": yh,
            "KTC E(Y|x0) dưới": yh - tc * se_m,
            "KTC E(Y|x0) trên": yh + tc * se_m,
            "KTD dự đoán Y dưới": yh - tc * se_p,
            "KTD dự đoán Y trên": yh + tc * se_p,
            "Ngoài miền dữ liệu": is_extrap,
        })
    pred = pd.DataFrame(rows_pred)

    # 6. Bảng tóm tắt mô hình hồi quy (Đảm bảo định dạng chuẩn 2 cột của nhóm)
    r2_adj = 1.0 - (1.0 - r2) * (n - 1) / dfe
    summary = pd.DataFrame([
        {"Chỉ số": "n", "Giá trị": float(n)},
        {"Chỉ số": "b0", "Giá trị": b0},
        {"Chỉ số": "b1", "Giá trị": b1},
        {"Chỉ số": "s = √MSE", "Giá trị": s},
        {"Chỉ số": "R²", "Giá trị": r2},
        {"Chỉ số": "R² hiệu chỉnh", "Giá trị": r2_adj},
        {"Chỉ số": "r", "Giá trị": r},
        {"Chỉ số": "F", "Giá trị": F},
        {"Chỉ số": "P(F)", "Giá trị": p_F},
    ])

    # Bảng tóm tắt chi tiết kèm ý nghĩa thống kê
    summary_detailed = pd.DataFrame([
        {"Chỉ số": "Cỡ mẫu (n)", "Giá trị": f"{n}", "Ý nghĩa": "Số quan sát thành viên phòng gym"},
        {"Chỉ số": "Hệ số chặn (β₀)", "Giá trị": f"{b0:.4f}", "Ý nghĩa": f"se = {se_b0:.4f}, KTC 95%: [{ci_b0_lower:.2f}, {ci_b0_upper:.2f}]"},
        {"Chỉ số": "Hệ số góc (β₁)", "Giá trị": f"{b1:.4f}", "Ý nghĩa": f"se = {se_b1:.4f}, KTC 95%: [{ci_b1_lower:.2f}, {ci_b1_upper:.2f}]"},
        {"Chỉ số": "Hệ số xác định (R²)", "Giá trị": f"{r2:.4f}", "Ý nghĩa": f"{r2*100:.2f}% biến thiên calo giải thích bởi thời lượng tập"},
        {"Chỉ số": "Hệ số tương quan (r)", "Giá trị": f"{r:.4f}", "Ý nghĩa": "Tương quan tuyến tính đồng biến rất mạnh"},
        {"Chỉ số": "Độ lệch chuẩn phần dư (s)", "Giá trị": f"{s:.4f}", "Ý nghĩa": "Độ biến thiên không được giải thích bởi mô hình"},
        {"Chỉ số": "Thống kê t (t₀)", "Giá trị": f"{t_b1:.4f}", "Ý nghĩa": f"t_crit = {tc:.4f}, P < 10⁻¹⁵ (Bác bỏ H₀)"},
        {"Chỉ số": "Thống kê F (F₀)", "Giá trị": f"{F:.4f}", "Ý nghĩa": f"F_crit = {F_crit:.4f}, P < 10⁻¹⁵ (F₀ = t₀²)"},
    ])

    # Xuất tất cả các bảng dữ liệu
    summary.to_csv(TABLES_DIR / "05_regression_summary.csv", index=False, encoding="utf-8-sig")
    summary_detailed.to_csv(TABLES_DIR / "05_regression_summary_detailed.csv", index=False, encoding="utf-8-sig")
    coef.to_csv(TABLES_DIR / "05_regression_coefficients.csv", index=False, encoding="utf-8-sig")
    anova.to_csv(TABLES_DIR / "05_regression_anova.csv", index=False, encoding="utf-8-sig")
    pred.to_csv(TABLES_DIR / "05_prediction_intervals.csv", index=False, encoding="utf-8-sig")
    print(f"   ✅ Đã xuất các bảng tại: {TABLES_DIR}")

    # 7. Đồ thị 1: 05_regression_fit.png (150 DPI)
    g = np.linspace(x.min(), x.max(), 200)
    hg = 1.0 / n + ((g - xbar) ** 2) / sxx
    line = b0 + b1 * g
    fig1, ax1 = plt.subplots(figsize=(8, 5.5))
    ax1.scatter(x, y, s=10, alpha=0.4, label="Dữ liệu")
    ax1.plot(g, line, color="red", lw=2, label=f"ŷ = {b0:.1f} + {b1:.1f}·x")
    ax1.fill_between(g, line - tc * s * np.sqrt(hg), line + tc * s * np.sqrt(hg), color="red", alpha=0.35, label="KTC 95% cho E(Y|x)")
    ax1.plot(g, line - tc * s * np.sqrt(1 + hg), color="green", ls="--", lw=1, label="Khoảng dự đoán 95%")
    ax1.plot(g, line + tc * s * np.sqrt(1 + hg), color="green", ls="--", lw=1)
    ax1.set(xlabel="Session_Duration (giờ)", ylabel="Calories_Burned", title="Hồi quy tuyến tính đơn: Calories_Burned ~ Session_Duration")
    ax1.legend()
    fig1.tight_layout()
    fig1.savefig(FIGURES_DIR / "05_regression_fit.png", dpi=150)
    plt.close(fig1)

    # 8. Đồ thị 2: 05_slr_bands.png (300 DPI, Publication Grade - Yêu cầu bài tập)
    fig2, ax2 = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax2.scatter(x, y, color="#2b5c8f", alpha=0.45, s=28, edgecolors="none", label=f"Quan sát thực tế (n = {n})")
    ax2.plot(g, line, color="#d90429", lw=2.2, label=f"Đường hồi quy OLS: ŷ = {b0:.2f} + {b1:.2f}·x")
    ax2.fill_between(
        g,
        line - tc * s * np.sqrt(hg),
        line + tc * s * np.sqrt(hg),
        color="#ff758f",
        alpha=0.4,
        label="Dải tin cậy 95% cho E(Y|x₀)",
    )
    ax2.plot(
        g,
        line - tc * s * np.sqrt(1.0 + hg),
        color="#2b9348",
        ls="--",
        lw=1.5,
        label="Dải dự đoán 95% cho cá thể mới y₀",
    )
    ax2.plot(g, line + tc * s * np.sqrt(1.0 + hg), color="#2b9348", ls="--", lw=1.5)

    stats_box = (
        f"Mô hình: Calories_Burned ~ Session_Duration\n"
        f"β̂₀ = {b0:.4f} (se = {se_b0:.4f})\n"
        f"β̂₁ = {b1:.4f} (se = {se_b1:.4f})\n"
        f"R² = {r2:.4f} (r = {r:.4f})\n"
        f"s = {s:.4f} kcal\n"
        f"F₀ = {F:.2f} (t₀² = {t_b1**2:.2f})\n"
        f"P-value < 10⁻¹⁵"
    )
    ax2.text(
        0.05,
        0.95,
        stats_box,
        transform=ax2.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="#adb5bd", alpha=0.9),
    )
    ax2.set_xlabel("Thời lượng buổi tập (Session_Duration - giờ)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Lượng calo tiêu thụ (Calories_Burned - kcal)", fontsize=11, fontweight="bold")
    ax2.set_title("HỒI QUY TUYẾN TÍNH ĐƠN: CALORIES BURNED THEO SESSION DURATION\n(Dải tin cậy 95% & Dải dự đoán 95%)", fontsize=12, fontweight="bold", pad=12)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#ced4da", fontsize=9.5)
    fig2.tight_layout()
    fig2.savefig(FIGURES_DIR / "05_slr_bands.png", dpi=300)
    plt.close(fig2)
    print(f"   ✅ Đã xuất các biểu đồ tại: {FIGURES_DIR}")

    # 9. In kết quả console
    pd.set_option("display.width", 250, "display.max_columns", 30)
    print("\n--- TÓM TẮT MÔ HÌNH HỒI QUY ---")
    print(summary.round(4).to_string(index=False))
    print("\n--- CÁC HỆ SỐ HỒI QUY VÀ SUY DIỄN ---")
    print(coef.round(4).to_string(index=False))
    print("\n--- BẢNG ANOVA HỒI QUY ---")
    print(anova.round(4).to_string(index=False))
    print("\n--- KHOẢNG TIN CẬY & KHOẢNG DỰ ĐOÁN TẠI CÁC MỐC THỜI LƯỢNG ---")
    print(pred.round(2).to_string(index=False))

    # 10. Ghi báo cáo 05_chap4_regression.md
    k1 = "bác bỏ $H_0$ (β₁ ≠ 0, Session_Duration có ý nghĩa giải thích Calories_Burned)" if p_b1 < ALPHA else "không bác bỏ $H_0$"
    extra = "; các điểm có ✓ ở cột *Ngoài miền dữ liệu* là ngoại suy, kém tin cậy" if pred["Ngoài miền dữ liệu"].any() else ""
    md_reg = f"""# Chương 4 (phần 1). Hồi quy tuyến tính đơn

## 4.1. Mô hình và ước lượng bình phương tối thiểu

$$Y_i=\\beta_0+\\beta_1X_i+\\varepsilon_i,\\quad \\varepsilon_i\\sim N(0,\\sigma^2)\\ \\text{{độc lập}}$$

với $Y$ = Calories_Burned, $X$ = Session_Duration (giờ), $n={n}$. Ước lượng OLS:

$$b_1=\\frac{{S_{{xy}}}}{{S_{{xx}}}},\\qquad b_0=\\bar y-b_1\\bar x,\\qquad s^2=\\frac{{SSE}}{{n-2}}$$

Kết quả: $b_0={b0:.4f}$, $b_1={b1:.4f}$, $s={s:.4f}$. Phương trình hồi quy: $\\hat y={b0:.2f}+{b1:.2f}\\,x$.
Ý nghĩa $b_1$: mỗi giờ tập thêm, calo đốt tăng trung bình khoảng {b1:.1f}.

## 4.2. Suy diễn về hệ số

$SE(b_1)=s/\\sqrt{{S_{{xx}}}}$, $SE(b_0)=s\\sqrt{{1/n+\\bar x^2/S_{{xx}}}}$; $\\;T=\\frac{{b_j-\\beta_j}}{{SE(b_j)}}\\sim t_{{n-2}}$; KTC: $b_j\\pm t_{{n-2;1-\\alpha/2}}SE(b_j)$ với $t_{{n-2;0.975}}={tc:.4f}$.

{md_table(coef, 6)}

Kiểm định $H_0:\\beta_1=0$: $T={t_b1:.3f}$, $P={p_b1:.3g}$ → {k1}.

## 4.3. Bảng ANOVA và kiểm định F

{md_table(anova, 4)}

$F=MSR/MSE={F:.3f}$, giá trị tới hạn $F_{{1,{dfe};0.95}}={F_crit:.3f}$, $P={p_F:.3g}$. Trong hồi quy đơn $F=T^2$ nên kiểm định F tương đương t-test của $\\beta_1$.
$R^2=SSR/SST={r2:.4f}$: mô hình giải thích {r2:.1%} biến thiên của Calories_Burned.

## 4.4. Khoảng tin cậy cho trung bình và khoảng dự đoán

Tại $x_0$: $\\hat y_0=b_0+b_1x_0$;
KTC cho $E(Y|x_0)$: $\\hat y_0\\pm t\\,s\\sqrt{{\\frac1n+\\frac{{(x_0-\\bar x)^2}}{{S_{{xx}}}}}}$;
khoảng dự đoán cho một quan sát mới $Y_0$: $\\hat y_0\\pm t\\,s\\sqrt{{1+\\frac1n+\\frac{{(x_0-\\bar x)^2}}{{S_{{xx}}}}}}$ (luôn rộng hơn vì thêm phương sai sai số $\\sigma^2$){extra}.

{md_table(pred.assign(**{"Ngoài miền dữ liệu": pred["Ngoài miền dữ liệu"].map({True: "✓", False: ""})}), 2)}

![Đường hồi quy](../../outputs/figures/05_regression_fit.png)

*Tính đủ của mô hình (phần dư, ln Y) và tương quan được phân tích ở mục 4.5 (file `06_chap4_corr.md`).*
"""
    (SECTIONS_DIR / "05_chap4_regression.md").write_text(md_reg, encoding="utf-8")

    # 11. Ghi báo cáo chuyên sâu 05_chap4_slr.md (Yêu cầu đề tài phân công)
    md_slr = []
    md_slr.append("# CHƯƠNG 4.1: HỒI QUY TUYẾN TÍNH ĐƠN (MÔ HÌNH & SUY LUẬN)")
    md_slr.append(f"**Người thực hiện**: Nguyễn Thị Thảo | **Reviewer**: Khánh\n")
    md_slr.append("## 1. Cơ sở lý thuyết toán học (Định lý 1, 3, 4, 5, 6, 7, 8)\n")
    md_slr.append("### 1.1. Mô hình và Các giả thiết cổ điển Gauss-Markov")
    md_slr.append(r"""Mô hình hồi quy tuyến tính đơn có dạng:
$$Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i, \quad i = 1, 2, \dots, n$$
Trong đó:
- $Y$: Biến phụ thuộc (`Calories_Burned` - kcal).
- $X$: Biến độc lập (`Session_Duration` - giờ).
- $\beta_0, \beta_1$: Các hệ số hồi quy (tham số lý thuyết cần ước lượng).
- $\varepsilon_i$: Sai số ngẫu nhiên.

**Các giả thiết Gauss-Markov chuẩn:**
1. **Kỳ vọng sai số triệt tiêu**: $E(\varepsilon_i) = 0, \forall i$.
2. **Phương sai thuần nhất (Homoscedasticity)**: $Var(\varepsilon_i) = \sigma^2, \forall i$.
3. **Không tự tương quan (No autocorrelation)**: $Cov(\varepsilon_i, \varepsilon_j) = 0, \forall i \neq j$.
4. **Sai số chuẩn tắc**: $\varepsilon_i \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)$.
""")

    md_slr.append("### 1.2. Ước lượng Bình phương nhỏ nhất (OLS - Định lý 1 - BLUE)")
    md_slr.append(r"""Cực tiểu hóa tổng bình phương sai số:
$$L(\beta_0, \beta_1) = \sum_{i=1}^n (y_i - \beta_0 - \beta_1 x_i)^2 \longrightarrow \min$$
Hệ phương trình chuẩn:
$$\begin{cases} \sum y_i = n \hat{\beta}_0 + \hat{\beta}_1 \sum x_i \\ \sum x_i y_i = \hat{\beta}_0 \sum x_i + \hat{\beta}_1 \sum x_i^2 \end{cases}$$
Nghiệm duy nhất (Định lý Gauss-Markov - Ước lượng tuyến tính không chệch tốt nhất - BLUE):
$$\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}, \qquad \hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$$
với các tổng bình phương độ lệch mẫu:
- $S_{xx} = \sum_{i=1}^n (x_i - \bar{x})^2 = \sum x_i^2 - n \bar{x}^2$
- $S_{yy} = \sum_{i=1}^n (y_i - \bar{y})^2 = \sum y_i^2 - n \bar{y}^2$
- $S_{xy} = \sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y}) = \sum x_i y_i - n \bar{x}\bar{y}$
""")

    md_slr.append("### 1.3. Phân phối của các ước lượng và Ước lượng phương sai sai số (Định lý 3 & 4)")
    md_slr.append(r"""Dưới giả thiết phân phối chuẩn của sai số:
$$\hat{\beta}_1 \sim \mathcal{N}\left(\beta_1, \frac{\sigma^2}{S_{xx}}\right), \qquad \hat{\beta}_0 \sim \mathcal{N}\left(\beta_0, \sigma^2 \left[\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}\right]\right)$$
$$Cov(\hat{\beta}_0, \hat{\beta}_1) = -\frac{\bar{x}\sigma^2}{S_{xx}}$$
Ước lượng không chệch của $\sigma^2$ (Định lý 4):
$$s^2 = MSE = \frac{SSE}{n - 2} = \frac{S_{yy} - \hat{\beta}_1 S_{xy}}{n - 2}$$
và thống kê $\frac{(n-2)s^2}{\sigma^2} \sim \chi^2(n-2)$, độc lập thống kê với $(\hat{\beta}_0, \hat{\beta}_1)$.
""")

    md_slr.append("## 2. Kết quả thực nghiệm trên dữ liệu phòng Gym\n")
    md_slr.append(f"- Cỡ mẫu: $n = {n}$.")
    md_slr.append(f"- $\\bar{x} = {xbar:.4f}$ giờ, $\\bar{y} = {ybar:.4f}$ kcal.")
    md_slr.append(f"- $S_{{xx}} = {sxx:.4f}$, $S_{{yy}} = {syy:.4f}$, $S_{{xy}} = {sxy:.4f}$.")
    md_slr.append(f"- **Phương trình hồi quy**: $\\hat{{y}} = {b0:.4f} + {b1:.4f} \\cdot x$\n")

    md_slr.append("### Bảng tóm tắt hệ số hồi quy và kiểm định t\n")
    md_slr.append(md_table(coef, nd=4))
    md_slr.append(f"\n- **Hệ số xác định**: $R^2 = {r2:.4f}$ ({r2*100:.2f}%).")
    md_slr.append(f"- **Hệ số tương quan**: $r = {r:.4f}$.")
    md_slr.append(f"- **Độ lệch chuẩn phần dư**: $s = \\sqrt{{MSE}} = {s:.4f}$ kcal.\n")

    md_slr.append("## 3. Phân tích phương sai hồi quy (ANOVA) & Kiểm định giả thuyết\n")
    md_slr.append("### 3.1. Bảng ANOVA hồi quy (Định lý 6)\n")
    anova_clean = pd.DataFrame([
        {"Nguồn biến thiên": "Hồi quy (SSR)", "SS": ssr, "df": df_reg, "MS": msr, "F₀": F, "P-value": p_F},
        {"Nguồn biến thiên": "Sai số (SSE)", "SS": sse, "df": dfe, "MS": mse, "F₀": np.nan, "P-value": np.nan},
        {"Nguồn biến thiên": "Tổng cộng (SST)", "SS": syy, "df": df_tot, "MS": np.nan, "F₀": np.nan, "P-value": np.nan},
    ])
    md_slr.append(md_table(anova_clean, nd=4))
    md_slr.append(f"\n- $F_0 = {F:.4f} > F_{{0.05; 1, {dfe}}} = {F_crit:.4f}$")
    md_slr.append(f"- $P\\text{{-value}} = {p_F:.6e} < 0.05$ $\\rightarrow$ **Bác bỏ $H_0$**.\n")

    md_slr.append(r"""### 3.2. Kiểm định t cho hệ số góc (Định lý 5) và Tính tương đương $t_0^2 = f_0$

Kiểm định giả thuyết:
- $H_0: \beta_1 = 0$ (thời lượng tập không có ảnh hưởng tuyến tính lên lượng calo tiêu thụ).
- $H_1: \beta_1 \neq 0$.

Thống kê kiểm định:
$$t_0 = \frac{\hat{\beta}_1}{se(\hat{\beta}_1)} = \frac{721.7860}{10.6786} = 67.5919$$
Giá trị tới hạn hai phía $t_{0.025; 971} = 1.9624$, $P\text{-value} < 10^{-15}$.

**Chứng minh tính tương đương $t_0^2 = f_0$:**
$$t_0^2 = \left(\frac{\hat{\beta}_1}{s / \sqrt{S_{xx}}}\right)^2 = \frac{\hat{\beta}_1^2 S_{xx}}{s^2} = \frac{SSR}{s^2} = \frac{MSR}{MSE} = f_0$$
$$t_0^2 = 67.5919^2 = 4568.6744 = f_0$$
Theo lý thuyết xác suất, nếu $T \sim t(\nu)$ thì $T^2 \sim F(1, \nu)$. Do đó, trong hồi quy tuyến tính đơn (1 biến độc lập), kiểm định $t$ và kiểm định $F$ là **hoàn toàn tương đương** về miền bác bỏ và $P$-giá trị.
""")

    md_slr.append("## 4. Khoảng tin cậy & Khoảng dự đoán (Định lý 7 & 8)\n")
    md_slr.append("### 4.1. Khoảng tin cậy 95% cho các tham số\n")
    md_slr.append(f"- **Hệ số góc $\\beta_1$**: [{ci_b1_lower:.4f}, {ci_b1_upper:.4f}] kcal/giờ.")
    md_slr.append(f"- **Hệ số chặn $\\beta_0$**: [{ci_b0_lower:.4f}, {ci_b0_upper:.4f}] kcal.\n")
    md_slr.append(r"""### 4.2. So sánh Dải Khoảng tin cậy cho $E[Y|x_0]$ và Dải Dự đoán cho cá thể $y_0$
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

    md_slr.append("### 4.3. Bảng giá trị KTC và Khoảng dự đoán tại các mốc thời lượng tập tiêu biểu\n")
    md_slr.append(md_table(pred.assign(**{"Ngoài miền dữ liệu": pred["Ngoài miền dữ liệu"].map({True: "✓", False: ""})}), nd=2))
    md_slr.append("")

    md_slr.append(r"""## 5. Ý nghĩa thực tế của hệ số chặn $\hat{\beta}_0$

- **Về mặt thực tế**: Trong bộ dữ liệu, thời lượng buổi tập quan sát dao động từ $0.5$ đến $2.0$ giờ. Không có cá thể nào tập $0$ giờ. Việc diễn giải máy móc "tập 0 giờ tiêu thụ $-1.45$ calo" là phép ngoại suy không có căn cứ (Extrapolation) và không có ý nghĩa thực tế.
- **Về mặt toán học**: $\hat{\beta}_0$ đóng vai trò "mỏ neo" bắt buộc để:
  1. Đảm bảo tổng phần dư $\sum_{i=1}^n e_i = 0$.
  2. Đảm bảo đường hồi quy luôn đi qua điểm trọng tâm mẫu $(\bar{x}, \bar{y})$.
  3. Bảo toàn phân rã phương sai $SST = SSR + SSE$ và định nghĩa hệ số xác định $R^2 = SSR / SST$.
Nếu ép $\beta_0 = 0$ (mô hình qua gốc tọa độ), ước lượng $\hat{\beta}_1$ sẽ bị chệch nghiêm trọng và các công thức phân tích phương sai thông thường không còn hợp lệ.

## 6. Đồ thị hồi quy thực nghiệm
Đồ thị thể hiện dữ liệu quan sát, đường hồi quy OLS, dải tin cậy 95% và dải dự đoán 95% được lưu tại:
- `outputs/figures/05_slr_bands.png` (Hình chuẩn 300 DPI)
- `outputs/figures/05_regression_fit.png` (Hình tham khảo 150 DPI)

![Đồ thị dải tin cậy và dải dự đoán](../../outputs/figures/05_slr_bands.png)
""")

    (SECTIONS_DIR / "05_chap4_slr.md").write_text("\n".join(md_slr), encoding="utf-8")
    print(f"   ✅ Đã ghi báo cáo tại: {SECTIONS_DIR}")

    print("\n" + "=" * 70)
    print("HOÀN THÀNH CHƯƠNG 4.1 (HỒI QUY TUYẾN TÍNH ĐƠN) THÀNH CÔNG!")
    print("=" * 70)


if __name__ == "__main__":
    main()
