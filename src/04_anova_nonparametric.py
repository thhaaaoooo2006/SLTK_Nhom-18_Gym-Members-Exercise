"""
Chương 3 (phần 2) — ANOVA 1 nhân tố & Kiểm định phi tham số
==============================================================
Tác giả : Nguyễn Thị Thảo (Owner) — Reviewer: Khánh
Mô-đun  : src/04_anova_nonparametric.py
Outputs :
    - outputs/tables/04_anova_chi2.csv
    - report/sections/04_chap3_part2.md

─────────────────────────────────────────────────────────────
LÝ THUYẾT
─────────────────────────────────────────────────────────────
A) PHÂN TÍCH PHƯƠNG SAI 1 NHÂN TỐ (One-Way ANOVA)
   • Mục tiêu: So sánh kỳ vọng μ của k ≥ 3 tổng thể.
   • Giả thiết: H₀: μ₁ = μ₂ = … = μₖ
                H₁: Tồn tại ít nhất 2 kỳ vọng khác nhau.
   • Phân tích tổng bình phương:
        SST = SSF + SSE
        SST = Σᵢ Σⱼ (xᵢⱼ − x̄)²          (tổng)
        SSF = Σᵢ nᵢ (x̄ᵢ − x̄)²           (giữa nhóm / Factor)
        SSE = Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)²         (trong nhóm / Error)
   • Thống kê kiểm định:
        F = MSF / MSE = [SSF/(k−1)] / [SSE/(N−k)]
     trong đó F ~ F(k−1, N−k) dưới H₀.

B) KIỂM ĐỊNH CHI-BÌNH PHƯƠNG PHÙ HỢP PHÂN PHỐI
   • Mục tiêu: Kiểm tra X có tuân theo phân phối lý thuyết F₀ không.
   • Giả thiết: H₀: X ~ F₀  vs  H₁: X không tuân theo F₀.
   • Chia miền giá trị thành m khoảng, đếm tần số quan sát Oᵢ.
   • Tần số kỳ vọng: Eᵢ = n · P(X ∈ khoảng i | H₀).
   • Thống kê:  χ² = Σᵢ (Oᵢ − Eᵢ)² / Eᵢ  ~ χ²(m − 1 − p)
     (p = số tham số được ước lượng từ mẫu, ở đây p = 2: μ̂ và σ̂²).

C) KIỂM ĐỊNH CHI-BÌNH PHƯƠNG TÍNH ĐỘC LẬP
   • Mục tiêu: Kiểm tra 2 biến phân loại có độc lập không.
   • Giả thiết: H₀: Hai biến độc lập  vs  H₁: Hai biến không độc lập.
   • Bảng chéo r × c, tần số kỳ vọng:
        Eᵢⱼ = (tổng hàng i × tổng cột j) / N
   • Thống kê:  χ² = Σᵢ Σⱼ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ  ~ χ²((r−1)(c−1))
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
    one_way_anova,
    chi2_goodness_of_fit,
    chi2_independence,
    fmt,
    md_table,
    TABLES_DIR,
    SECTIONS_DIR,
)

# Chỉ dùng scipy.stats để tra giá trị tới hạn & P-giá trị
from scipy import stats as sp_stats

# ============================================================================
# 0. ĐỌC DỮ LIỆU
# ============================================================================
print("=" * 70)
print("CHƯƠNG 3 (P2) — ANOVA 1 NHÂN TỐ & KIỂM ĐỊNH PHI THAM SỐ")
print("=" * 70)

df = load_data()
n_total = len(df)
alpha = 0.05
print(f"\n[INFO] Dữ liệu: {n_total} quan sát, α = {alpha}")

# Danh sách kết quả để xuất CSV
all_results = []


# ============================================================================
# A. ANOVA 1 NHÂN TỐ: Calories_Burned theo Workout_Type
# ============================================================================
print("\n" + "=" * 70)
print("A. ANOVA 1 NHÂN TỐ")
print("   So sánh Calories_Burned theo 4 loại Workout_Type")
print("=" * 70)

workout_types = sorted(df["Workout_Type"].unique())
groups = [df.loc[df["Workout_Type"] == wt, "Calories_Burned"].values for wt in workout_types]

print(f"\n   Số nhóm k = {len(workout_types)}: {', '.join(workout_types)}")
for wt, g in zip(workout_types, groups):
    print(f"   • {wt:10s}: n = {len(g):3d},  x̄ = {sample_mean(g):.2f},  S = {sample_std(g):.2f}")

# Giả thiết
print(f"\n   H₀: μ_Cardio = μ_HIIT = μ_Strength = μ_Yoga")
print(f"   H₁: Tồn tại ít nhất 2 kỳ vọng khác nhau")
print(f"   Mức ý nghĩa α = {alpha}")

# Tính ANOVA bằng hàm tự cài đặt
anova = one_way_anova(*groups)

print(f"\n   ── Bảng ANOVA ──")
print(f"   {'Nguồn':<15s} {'SS':>14s} {'df':>5s} {'MS':>14s} {'F':>10s}")
print(f"   {'─' * 60}")
print(f"   {'Nhân tố (SSF)':<15s} {anova['SSF']:>14.4f} {anova['df_F']:>5d} {anova['MSF']:>14.4f} {anova['F_stat']:>10.4f}")
print(f"   {'Sai số (SSE)':<15s} {anova['SSE']:>14.4f} {anova['df_E']:>5d} {anova['MSE']:>14.4f}")
print(f"   {'Tổng (SST)':<15s} {anova['SST']:>14.4f} {anova['N'] - 1:>5d}")

# Giá trị tới hạn & P-giá trị (dùng scipy.stats)
f_critical = sp_stats.f.ppf(1 - alpha, anova["df_F"], anova["df_E"])
p_value_anova = 1 - sp_stats.f.cdf(anova["F_stat"], anova["df_F"], anova["df_E"])

print(f"\n   F_stat     = {anova['F_stat']:.4f}")
print(f"   F_critical = F({alpha}; {anova['df_F']}, {anova['df_E']}) = {f_critical:.4f}")
print(f"   P-value    = {p_value_anova:.6e}")

if anova["F_stat"] > f_critical:
    anova_decision = "BÁC BỎ H₀"
    print(f"\n   → Kết luận: {anova_decision} (F = {anova['F_stat']:.4f} > F_critical = {f_critical:.4f})")
    print(f"     Có sự KHÁC BIỆT có ý nghĩa thống kê về Calories_Burned")
    print(f"     giữa ít nhất 2 loại Workout_Type (ở mức α = {alpha}).")
else:
    anova_decision = "KHÔNG BÁC BỎ H₀"
    print(f"\n   → Kết luận: {anova_decision}")

all_results.append({
    "Kiểm định": "ANOVA 1 nhân tố",
    "Biến phân tích": "Calories_Burned ~ Workout_Type",
    "Thống kê": f"F = {anova['F_stat']:.4f}",
    "df": f"({anova['df_F']}, {anova['df_E']})",
    "Giá trị tới hạn": f"F_crit = {f_critical:.4f}",
    "P-value": f"{p_value_anova:.6e}",
    "Kết luận": anova_decision,
})


# ============================================================================
# B. KIỂM ĐỊNH CHI-BÌNH PHƯƠNG PHÙ HỢP PHÂN PHỐI CHUẨN
# ============================================================================
print("\n" + "=" * 70)
print("B. KIỂM ĐỊNH CHI-BÌNH PHƯƠNG PHÙ HỢP PHÂN PHỐI CHUẨN")
print("=" * 70)


def chi2_normal_test(data: np.ndarray, var_name: str, n_bins: int = 10) -> dict:
    """Kiểm định Chi-bình phương phù hợp phân phối chuẩn N(μ̂, σ̂²).

    - Chia dữ liệu thành n_bins khoảng đều nhau.
    - Ước lượng μ̂ = x̄ và σ̂ = S từ mẫu.
    - Tính tần số kỳ vọng Eᵢ = n · [Φ(bᵢ) − Φ(aᵢ)].
    - Gộp các khoảng có Eᵢ < 5 vào khoảng liền kề.
    - df = (số khoảng sau gộp) − 1 − 2 (vì ước lượng 2 tham số μ, σ).
    """
    n = len(data)
    mu_hat = sample_mean(data)
    sigma_hat = sample_std(data, ddof=1)

    print(f"\n   Biến: {var_name}")
    print(f"   n = {n},  μ̂ = x̄ = {mu_hat:.4f},  σ̂ = S = {sigma_hat:.4f}")
    print(f"   H₀: {var_name} ~ N({mu_hat:.2f}, {sigma_hat:.2f}²)")
    print(f"   H₁: {var_name} không tuân theo phân phối chuẩn")

    # Tạo các bin edges đều nhau
    data_min, data_max = float(np.min(data)), float(np.max(data))
    margin = (data_max - data_min) * 0.001
    edges = np.linspace(data_min - margin, data_max + margin, n_bins + 1)

    # Tần số quan sát
    observed = np.array([int(((data >= edges[i]) & (data < edges[i + 1])).sum())
                         for i in range(n_bins)], dtype=float)
    # Đảm bảo bin cuối cùng chứa cả giá trị max
    observed[-1] += n - observed.sum()

    # Tần số kỳ vọng dưới H₀: N(μ̂, σ̂²)
    expected = np.array([
        n * (sp_stats.norm.cdf(edges[i + 1], mu_hat, sigma_hat)
             - sp_stats.norm.cdf(edges[i], mu_hat, sigma_hat))
        for i in range(n_bins)
    ], dtype=float)

    # Gộp các khoảng có E < 5 từ hai đầu vào khoảng liền kề
    while len(expected) > 2 and expected[0] < 5:
        observed[1] += observed[0]
        expected[1] += expected[0]
        observed = observed[1:]
        expected = expected[1:]
        edges = np.concatenate([[edges[0]], edges[2:]])

    while len(expected) > 2 and expected[-1] < 5:
        observed[-2] += observed[-1]
        expected[-2] += expected[-1]
        observed = observed[:-1]
        expected = expected[:-1]
        edges = np.concatenate([edges[:-2], [edges[-1]]])

    m = len(observed)  # số khoảng sau gộp
    p_params = 2       # số tham số ước lượng (μ, σ)
    df = m - 1 - p_params

    if df < 1:
        print(f"   ⚠ Bậc tự do = {df} < 1 — không đủ khoảng để kiểm định.")
        return None

    # Thống kê Chi-bình phương (tự cài đặt)
    result = chi2_goodness_of_fit(observed, expected)
    chi2_stat = result["chi2_stat"]

    # Giá trị tới hạn & P-value (scipy)
    chi2_crit = sp_stats.chi2.ppf(1 - alpha, df)
    p_val = 1 - sp_stats.chi2.cdf(chi2_stat, df)

    print(f"   Số khoảng sau gộp: m = {m}, df = m − 1 − 2 = {df}")

    # In bảng tần số
    print(f"\n   {'Khoảng':<25s} {'Oᵢ':>6s} {'Eᵢ':>10s} {'(O−E)²/E':>12s}")
    print(f"   {'─' * 55}")
    for i in range(m):
        contrib = (observed[i] - expected[i]) ** 2 / expected[i]
        label = f"[{edges[i]:.2f}, {edges[i+1]:.2f})"
        print(f"   {label:<25s} {observed[i]:>6.0f} {expected[i]:>10.4f} {contrib:>12.4f}")

    print(f"\n   χ²_stat    = {chi2_stat:.4f}")
    print(f"   χ²_critical = χ²({alpha}; {df}) = {chi2_crit:.4f}")
    print(f"   P-value    = {p_val:.6e}")

    if chi2_stat > chi2_crit:
        decision = "BÁC BỎ H₀"
        print(f"\n   → {decision}: Dữ liệu KHÔNG phù hợp phân phối chuẩn (ở mức α = {alpha}).")
    else:
        decision = "KHÔNG BÁC BỎ H₀"
        print(f"\n   → {decision}: Không đủ bằng chứng bác bỏ — dữ liệu có thể")
        print(f"     tuân theo phân phối chuẩn (ở mức α = {alpha}).")

    return {
        "var_name": var_name, "chi2_stat": chi2_stat, "df": df,
        "chi2_crit": chi2_crit, "p_value": p_val, "decision": decision,
    }


# B1. Session_Duration
print("\n" + "-" * 50)
result_sd = chi2_normal_test(df["Session_Duration"].values, "Session_Duration")
if result_sd:
    all_results.append({
        "Kiểm định": "Chi² phù hợp chuẩn",
        "Biến phân tích": "Session_Duration ~ N(μ̂, σ̂²)",
        "Thống kê": f"χ² = {result_sd['chi2_stat']:.4f}",
        "df": str(result_sd["df"]),
        "Giá trị tới hạn": f"χ²_crit = {result_sd['chi2_crit']:.4f}",
        "P-value": f"{result_sd['p_value']:.6e}",
        "Kết luận": result_sd["decision"],
    })

# B2. Calories_Burned
print("\n" + "-" * 50)
result_cb = chi2_normal_test(df["Calories_Burned"].values, "Calories_Burned")
if result_cb:
    all_results.append({
        "Kiểm định": "Chi² phù hợp chuẩn",
        "Biến phân tích": "Calories_Burned ~ N(μ̂, σ̂²)",
        "Thống kê": f"χ² = {result_cb['chi2_stat']:.4f}",
        "df": str(result_cb["df"]),
        "Giá trị tới hạn": f"χ²_crit = {result_cb['chi2_crit']:.4f}",
        "P-value": f"{result_cb['p_value']:.6e}",
        "Kết luận": result_cb["decision"],
    })


# ============================================================================
# C. KIỂM ĐỊNH CHI-BÌNH PHƯƠNG TÍNH ĐỘC LẬP: Gender × Experience_Level
# ============================================================================
print("\n" + "=" * 70)
print("C. KIỂM ĐỊNH CHI-BÌNH PHƯƠNG TÍNH ĐỘC LẬP")
print("   Gender × Experience_Level")
print("=" * 70)

print(f"\n   H₀: Gender và Experience_Level là ĐỘC LẬP")
print(f"   H₁: Gender và Experience_Level KHÔNG độc lập")
print(f"   Mức ý nghĩa α = {alpha}")

# Lập bảng chéo (Contingency Table)
ct = pd.crosstab(df["Gender"], df["Experience_Level"])
print(f"\n   ── Bảng chéo (Observed) ──")
print(ct.to_string().replace("\n", "\n   "))

# Kiểm định bằng hàm tự cài đặt
indep = chi2_independence(ct.values)

print(f"\n   ── Bảng tần số kỳ vọng (Expected) ──")
df_expected = pd.DataFrame(indep["expected"],
                           index=ct.index, columns=ct.columns)
print(df_expected.round(4).to_string().replace("\n", "\n   "))

r, c = ct.shape
df_indep = indep["df"]

# Giá trị tới hạn & P-value (scipy)
chi2_crit_indep = sp_stats.chi2.ppf(1 - alpha, df_indep)
p_val_indep = 1 - sp_stats.chi2.cdf(indep["chi2_stat"], df_indep)

print(f"\n   r = {r} (hàng),  c = {c} (cột),  df = (r−1)(c−1) = {df_indep}")
print(f"   χ²_stat    = {indep['chi2_stat']:.4f}")
print(f"   χ²_critical = χ²({alpha}; {df_indep}) = {chi2_crit_indep:.4f}")
print(f"   P-value    = {p_val_indep:.6e}")

if indep["chi2_stat"] > chi2_crit_indep:
    indep_decision = "BÁC BỎ H₀"
    print(f"\n   → {indep_decision}: Gender và Experience_Level KHÔNG độc lập (α = {alpha}).")
else:
    indep_decision = "KHÔNG BÁC BỎ H₀"
    print(f"\n   → {indep_decision}: Không đủ bằng chứng — Gender và Experience_Level")
    print(f"     có thể độc lập nhau (ở mức α = {alpha}).")

all_results.append({
    "Kiểm định": "Chi² tính độc lập",
    "Biến phân tích": "Gender × Experience_Level",
    "Thống kê": f"χ² = {indep['chi2_stat']:.4f}",
    "df": str(df_indep),
    "Giá trị tới hạn": f"χ²_crit = {chi2_crit_indep:.4f}",
    "P-value": f"{p_val_indep:.6e}",
    "Kết luận": indep_decision,
})


# ============================================================================
# D. XUẤT KẾT QUẢ
# ============================================================================
print("\n" + "=" * 70)
print("D. XUẤT KẾT QUẢ RA FILE")
print("=" * 70)

# CSV
df_results = pd.DataFrame(all_results)
out_csv = TABLES_DIR / "04_anova_chi2.csv"
df_results.to_csv(out_csv, index=False, encoding="utf-8-sig")
print(f"   ✅ {out_csv}")

# Markdown report
md = []
md.append("# Chương 3 (Phần 2) — ANOVA 1 nhân tố & Kiểm định phi tham số\n")

md.append("## A. ANOVA 1 nhân tố: Calories_Burned ~ Workout_Type\n")
md.append("### Giả thiết\n")
md.append("- $H_0$: $\\mu_{Cardio} = \\mu_{HIIT} = \\mu_{Strength} = \\mu_{Yoga}$")
md.append("- $H_1$: Tồn tại ít nhất 2 kỳ vọng khác nhau\n")
md.append("### Bảng ANOVA\n")
anova_df = pd.DataFrame([
    {"Nguồn": "Nhân tố (SSF)", "SS": anova["SSF"], "df": anova["df_F"],
     "MS": anova["MSF"], "F": anova["F_stat"]},
    {"Nguồn": "Sai số (SSE)", "SS": anova["SSE"], "df": anova["df_E"],
     "MS": anova["MSE"], "F": ""},
    {"Nguồn": "Tổng (SST)", "SS": anova["SST"], "df": anova["N"] - 1,
     "MS": "", "F": ""},
])
md.append(md_table(anova_df, nd=4))
md.append(f"\n- $F_{{stat}} = {anova['F_stat']:.4f}$, "
          f"$F_{{critical}} = {f_critical:.4f}$, "
          f"$P = {p_value_anova:.6e}$")
md.append(f"- **Kết luận**: {anova_decision}\n")

md.append("## B. Kiểm định Chi-bình phương phù hợp phân phối chuẩn\n")
for r in [result_sd, result_cb]:
    if r:
        md.append(f"### {r['var_name']}\n")
        md.append(f"- $H_0$: {r['var_name']} $\\sim N(\\hat{{\\mu}}, \\hat{{\\sigma}}^2)$")
        md.append(f"- $\\chi^2 = {r['chi2_stat']:.4f}$, "
                  f"$df = {r['df']}$, "
                  f"$\\chi^2_{{crit}} = {r['chi2_crit']:.4f}$, "
                  f"$P = {r['p_value']:.6e}$")
        md.append(f"- **Kết luận**: {r['decision']}\n")

md.append("## C. Kiểm định Chi-bình phương tính độc lập: Gender × Experience_Level\n")
md.append("- $H_0$: Gender và Experience_Level độc lập")
md.append("- $H_1$: Gender và Experience_Level không độc lập\n")
md.append("### Bảng chéo (Observed)\n")
ct_display = ct.reset_index()
ct_display.columns = [str(c) for c in ct_display.columns]
md.append(md_table(ct_display))
md.append(f"\n- $\\chi^2 = {indep['chi2_stat']:.4f}$, "
          f"$df = {df_indep}$, "
          f"$\\chi^2_{{crit}} = {chi2_crit_indep:.4f}$, "
          f"$P = {p_val_indep:.6e}$")
md.append(f"- **Kết luận**: {indep_decision}\n")

md.append("## Tổng hợp kết quả\n")
md.append(md_table(df_results, nd=4))
md.append("")

report_path = SECTIONS_DIR / "04_chap3_part2.md"
report_path.write_text("\n".join(md), encoding="utf-8")
print(f"   ✅ {report_path}")

print("\n" + "=" * 70)
print("HOÀN THÀNH CHƯƠNG 3 (PHẦN 2)")
print("=" * 70)
