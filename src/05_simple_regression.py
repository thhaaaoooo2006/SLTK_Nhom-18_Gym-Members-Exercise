
"""Chương 4.1 - Hồi quy tuyến tính đơn (OLS, t-test, F-test, KTC & khoảng dự đoán)

Mô hình: Calories_Burned (Y) = β0 + β1·Session_Duration (X) + ε,  ε ~ N(0, σ²)
Nội dung: ước lượng OLS, sai số chuẩn, KTC & kiểm định t cho β0, β1, bảng ANOVA (F-test),
          R², KTC cho giá trị trung bình E(Y|x0) và khoảng dự đoán cho Y tại x0, đồ thị đường hồi quy.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats  # chỉ tra quantile / P-giá trị

from stats_utils import (FIGURES_DIR, SECTIONS_DIR, TABLES_DIR, load_data, md_table,
                         sample_mean, simple_ols)

ALPHA = 0.05
X0_LIST = [0.75, 1.0, 1.25, 1.5, 2.0]  # các giá trị Session_Duration (giờ) cần dự báo - chỉnh theo đề


def main():
    df = load_data()
    x = df["Session_Duration"].to_numpy(float)
    y = df["Calories_Burned"].to_numpy(float)
    m = simple_ols(x, y)
    n, b0, b1, s, sxx = m["n"], m["b0"], m["b1"], m["s"], m["sxx"]
    xbar = sample_mean(x)
    dfe = n - 2
    tc = float(stats.t.ppf(1 - ALPHA / 2, dfe))

    # ---------------- Hệ số hồi quy ----------------
    se_b1 = s / np.sqrt(sxx)
    se_b0 = s * np.sqrt(1 / n + xbar**2 / sxx)
    coef = []
    for name, b, se in (("β0 (Intercept)", b0, se_b0), ("β1 (Session_Duration)", b1, se_b1)):
        t = b / se
        coef.append({"Hệ số": name, "Ước lượng": b, "Sai số chuẩn": se, "t (H0: β=0)": t,
                     "P-giá trị": float(2 * stats.t.sf(abs(t), dfe)),
                     "KTC 95% cận dưới": b - tc * se, "KTC 95% cận trên": b + tc * se})
    coef = pd.DataFrame(coef)

    # ---------------- ANOVA (F-test) ----------------
    ssr, sse, sst = m["ssr"], m["sse"], m["syy"]
    msr, mse = ssr, sse / dfe
    F = msr / mse
    p_F = float(stats.f.sf(F, 1, dfe))
    F_crit = float(stats.f.ppf(1 - ALPHA, 1, dfe))
    anova = pd.DataFrame([
        {"Nguồn": "Hồi quy (SSR)", "Tổng bình phương": ssr, "Bậc tự do": 1, "Trung bình bình phương": msr, "F": F, "P-giá trị": p_F},
        {"Nguồn": "Phần dư (SSE)", "Tổng bình phương": sse, "Bậc tự do": dfe, "Trung bình bình phương": mse, "F": np.nan, "P-giá trị": np.nan},
        {"Nguồn": "Tổng (SST)", "Tổng bình phương": sst, "Bậc tự do": n - 1, "Trung bình bình phương": np.nan, "F": np.nan, "P-giá trị": np.nan},
    ])

    # ---------------- KTC trung bình & khoảng dự đoán ----------------
    rows = []
    for x0 in X0_LIST:
        yh = b0 + b1 * x0
        h = 1 / n + (x0 - xbar) ** 2 / sxx
        se_m, se_p = s * np.sqrt(h), s * np.sqrt(1 + h)
        rows.append({"x0 (giờ)": x0, "ŷ0": yh,
                     "KTC E(Y|x0) dưới": yh - tc * se_m, "KTC E(Y|x0) trên": yh + tc * se_m,
                     "KTD dự đoán Y dưới": yh - tc * se_p, "KTD dự đoán Y trên": yh + tc * se_p,
                     "Ngoài miền dữ liệu": bool(x0 < x.min() or x0 > x.max())})
    pred = pd.DataFrame(rows)

    summary = pd.DataFrame([
        {"Chỉ số": "n", "Giá trị": n}, {"Chỉ số": "b0", "Giá trị": b0}, {"Chỉ số": "b1", "Giá trị": b1},
        {"Chỉ số": "s = √MSE", "Giá trị": s}, {"Chỉ số": "R²", "Giá trị": m["r2"]},
        {"Chỉ số": "R² hiệu chỉnh", "Giá trị": 1 - (1 - m["r2"]) * (n - 1) / dfe},
        {"Chỉ số": "r", "Giá trị": m["r"]}, {"Chỉ số": "F", "Giá trị": F}, {"Chỉ số": "P(F)", "Giá trị": p_F},
    ])
    summary.to_csv(TABLES_DIR / "05_regression_summary.csv", index=False, encoding="utf-8-sig")
    coef.to_csv(TABLES_DIR / "05_regression_coefficients.csv", index=False, encoding="utf-8-sig")
    anova.to_csv(TABLES_DIR / "05_regression_anova.csv", index=False, encoding="utf-8-sig")
    pred.to_csv(TABLES_DIR / "05_prediction_intervals.csv", index=False, encoding="utf-8-sig")

    # ---------------- Đồ thị ----------------
    g = np.linspace(x.min(), x.max(), 200)
    hg = 1 / n + (g - xbar) ** 2 / sxx
    line = b0 + b1 * g
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter(x, y, s=10, alpha=0.4, label="Dữ liệu")
    ax.plot(g, line, color="red", lw=2, label=f"ŷ = {b0:.1f} + {b1:.1f}·x")
    ax.fill_between(g, line - tc * s * np.sqrt(hg), line + tc * s * np.sqrt(hg), color="red", alpha=0.35, label="KTC 95% cho E(Y|x)")
    ax.plot(g, line - tc * s * np.sqrt(1 + hg), color="green", ls="--", lw=1, label="Khoảng dự đoán 95%")
    ax.plot(g, line + tc * s * np.sqrt(1 + hg), color="green", ls="--", lw=1)
    ax.set(xlabel="Session_Duration (giờ)", ylabel="Calories_Burned", title="Hồi quy tuyến tính đơn: Calories_Burned ~ Session_Duration")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "05_regression_fit.png", dpi=150)
    plt.close(fig)

    pd.set_option("display.width", 250, "display.max_columns", 30)
    print(summary.round(4).to_string(index=False))
    print(coef.round(4).to_string(index=False))
    print(anova.round(4).to_string(index=False))
    print(pred.round(2).to_string(index=False))

    # ---------------- Báo cáo ----------------
    k1 = "bác bỏ $H_0$ (β₁ ≠ 0, Session_Duration có ý nghĩa giải thích Calories_Burned)" if coef.loc[1, "P-giá trị"] < ALPHA else "không bác bỏ $H_0$"
    extra = "; các điểm có ✓ ở cột *Ngoài miền dữ liệu* là ngoại suy, kém tin cậy" if pred["Ngoài miền dữ liệu"].any() else ""
    md = f"""# Chương 4 (phần 1). Hồi quy tuyến tính đơn

## 4.1. Mô hình và ước lượng bình phương tối thiểu

$$Y_i=\\beta_0+\\beta_1X_i+\\varepsilon_i,\\quad \\varepsilon_i\\sim N(0,\\sigma^2)\\ \\text{{độc lập}}$$

với $Y$ = Calories_Burned, $X$ = Session_Duration (giờ), $n={n}$. Ước lượng OLS:

$$b_1=\\frac{{S_{{xy}}}}{{S_{{xx}}}},\\qquad b_0=\\bar y-b_1\\bar x,\\qquad s^2=\\frac{{SSE}}{{n-2}}$$

Kết quả: $b_0={b0:.4f}$, $b_1={b1:.4f}$, $s={s:.4f}$. Phương trình hồi quy: $\\hat y={b0:.2f}+{b1:.2f}\\,x$.
Ý nghĩa $b_1$: mỗi giờ tập thêm, calo đốt tăng trung bình khoảng {b1:.1f}.

## 4.2. Suy diễn về hệ số

$SE(b_1)=s/\\sqrt{{S_{{xx}}}}$, $SE(b_0)=s\\sqrt{{1/n+\\bar x^2/S_{{xx}}}}$; $\\;T=\\frac{{b_j-\\beta_j}}{{SE(b_j)}}\\sim t_{{n-2}}$; KTC: $b_j\\pm t_{{n-2;1-\\alpha/2}}SE(b_j)$ với $t_{{n-2;0.975}}={tc:.4f}$.

{md_table(coef, 6)}

Kiểm định $H_0:\\beta_1=0$: $T={coef.loc[1, 't (H0: β=0)']:.3f}$, $P={coef.loc[1, 'P-giá trị']:.3g}$ → {k1}.

## 4.3. Bảng ANOVA và kiểm định F

{md_table(anova, 4)}

$F=MSR/MSE={F:.3f}$, giá trị tới hạn $F_{{1,{dfe};0.95}}={F_crit:.3f}$, $P={p_F:.3g}$. Trong hồi quy đơn $F=T^2$ nên kiểm định F tương đương t-test của $\\beta_1$.
$R^2=SSR/SST={m['r2']:.4f}$: mô hình giải thích {m['r2']:.1%} biến thiên của Calories_Burned.

## 4.4. Khoảng tin cậy cho trung bình và khoảng dự đoán

Tại $x_0$: $\\hat y_0=b_0+b_1x_0$;
KTC cho $E(Y|x_0)$: $\\hat y_0\\pm t\\,s\\sqrt{{\\frac1n+\\frac{{(x_0-\\bar x)^2}}{{S_{{xx}}}}}}$;
khoảng dự đoán cho một quan sát mới $Y_0$: $\\hat y_0\\pm t\\,s\\sqrt{{1+\\frac1n+\\frac{{(x_0-\\bar x)^2}}{{S_{{xx}}}}}}$ (luôn rộng hơn vì thêm phương sai sai số $\\sigma^2$){extra}.

{md_table(pred.assign(**{"Ngoài miền dữ liệu": pred["Ngoài miền dữ liệu"].map({True: "✓", False: ""})}), 2)}

![Đường hồi quy](../../outputs/figures/05_regression_fit.png)

*Tính đủ của mô hình (phần dư, ln Y) và tương quan được phân tích ở mục 4.5 (file `06_chap4_corr.md`).*
"""
    (SECTIONS_DIR / "05_chap4_regression.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()