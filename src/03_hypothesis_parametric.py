
"""Chương 3 - Kiểm định tham số 1 & 2 tổng thể

Quy trình 5 bước, mỗi bài toán được kết luận theo 3 cách:
  (1) Miền bác bỏ cổ điển, (2) P-giá trị, (3) đối chiếu khoảng tin cậy.
Các giá trị giả thuyết (MU0, VAR0, P0) là tham số cấu hình - chỉnh theo kết quả thống kê mô tả (Chương 1).
"""

import numpy as np
import pandas as pd
from scipy import stats  # chỉ tra quantile / P-giá trị

from stats_utils import (SECTIONS_DIR, TABLES_DIR, load_data, md_table,
                         sample_mean, sample_prop, sample_var)

ALPHA = 0.05
MU0 = 900.0      # H0: kỳ vọng Calories_Burned = MU0
VAR0 = 0.10      # H0: phương sai Session_Duration = VAR0
P0 = 0.5         # H0: tỷ lệ Male = P0
HIGH_CAL = 1000.0  # khớp với 02_estimation_chap2.py

DISTS = {"t": stats.t, "z": stats.norm, "chi2": stats.chi2, "f": stats.f}
ALT_TXT = {"two": "≠", "right": ">", "left": "<"}


def crit_region(dist, params, alt, alpha=ALPHA):
    d = DISTS[dist]
    if alt == "two":
        return d.ppf(alpha / 2, *params), d.ppf(1 - alpha / 2, *params)
    if alt == "right":
        return None, d.ppf(1 - alpha, *params)
    return d.ppf(alpha, *params), None


def p_value(dist, params, stat, alt):
    d = DISTS[dist]
    if alt == "right":
        return float(d.sf(stat, *params))
    if alt == "left":
        return float(d.cdf(stat, *params))
    return float(min(1.0, 2 * min(d.cdf(stat, *params), d.sf(stat, *params))))


def region_text(lo, hi, stat_name):
    parts = []
    if lo is not None:
        parts.append(f"{stat_name} < {lo:.4f}")
    if hi is not None:
        parts.append(f"{stat_name} > {hi:.4f}")
    return " hoặc ".join(parts)


def sym_ci(est, se, dist, df, alt):
    d = DISTS[dist]
    p = 1 - ALPHA / 2 if alt == "two" else 1 - ALPHA
    c = d.ppf(p, df) if dist == "t" else d.ppf(p)
    if alt == "two":
        return est - c * se, est + c * se
    return (est - c * se, np.inf) if alt == "right" else (-np.inf, est + c * se)


def run_test(name, param, theta0, est, alt, stat_name, stat, dist, params, ci_fn, h0_txt):
    lo, hi = crit_region(dist, params, alt)
    rej_crit = bool((lo is not None and stat < lo) or (hi is not None and stat > hi))
    p = p_value(dist, params, stat, alt)
    ci_lo, ci_hi = ci_fn(alt)
    rej_ci = not (ci_lo <= theta0 <= ci_hi)
    kl = lambda r: "Bác bỏ H0" if r else "Không bác bỏ H0"
    return {
        "Kiểm định": name, "H0": h0_txt, "H1": f"{param} {ALT_TXT[alt]} {theta0:g}" if "−" not in h0_txt and "/" not in h0_txt else h0_txt.replace("=", ALT_TXT[alt]),
        "Ước lượng điểm": est, "Thống kê": stat_name, "Giá trị thống kê": stat,
        "Phân phối": f"{dist}{tuple(round(float(q), 2) for q in params) if params else ''}",
        "Miền bác bỏ": region_text(lo, hi, stat_name), "P-giá trị": p,
        "KTC tương ứng": f"({ci_lo:.4f}; {ci_hi:.4f})",
        "KL (miền bác bỏ)": kl(rej_crit), "KL (P-giá trị)": kl(p < ALPHA), "KL (KTC)": kl(rej_ci),
        "Nhất quán 3 cách": rej_crit == (p < ALPHA) == rej_ci,
    }


# ---------------------------------------------------------------------------
# Sai lầm loại II / lực kiểm định (xấp xỉ chuẩn)
# ---------------------------------------------------------------------------
def power_two_sided(shift):
    zc = stats.norm.ppf(1 - ALPHA / 2)
    return float(stats.norm.cdf(-zc + shift) + stats.norm.cdf(-zc - shift))


def power_prop(p0, p1, n):
    zc = stats.norm.ppf(1 - ALPHA / 2)
    se0, se1 = np.sqrt(p0 * (1 - p0) / n), np.sqrt(p1 * (1 - p1) / n)
    d = abs(p1 - p0)
    return float(stats.norm.cdf((d - zc * se0) / se1) + stats.norm.cdf((-d - zc * se0) / se1))


def main():
    df = load_data()
    y = df["Calories_Burned"].to_numpy(float)
    x = df["Session_Duration"].to_numpy(float)
    male = (df["Gender"].str.strip().str.lower() == "male").to_numpy()
    n = len(df)
    results = []

    # ---- 1 tổng thể ----
    ybar, s2y = sample_mean(y), sample_var(y)
    se = np.sqrt(s2y / n)
    results.append(run_test("1. Kỳ vọng Calories_Burned", "μ", MU0, ybar, "two", "T", (ybar - MU0) / se, "t", (n - 1,),
                            lambda a: sym_ci(ybar, se, "t", n - 1, a), f"μ = {MU0:g}"))

    s2x = sample_var(x)
    chi = (n - 1) * s2x / VAR0
    def var_ci(a):
        k = (n - 1) * s2x
        if a == "two":
            return k / stats.chi2.ppf(1 - ALPHA / 2, n - 1), k / stats.chi2.ppf(ALPHA / 2, n - 1)
        return (k / stats.chi2.ppf(1 - ALPHA, n - 1), np.inf) if a == "right" else (0.0, k / stats.chi2.ppf(ALPHA, n - 1))
    results.append(run_test("2. Phương sai Session_Duration", "σ²", VAR0, s2x, "two", "χ²", chi, "chi2", (n - 1,),
                            var_ci, f"σ² = {VAR0:g}"))

    p_hat = sample_prop(male)
    z = (p_hat - P0) / np.sqrt(P0 * (1 - P0) / n)
    se_p = np.sqrt(p_hat * (1 - p_hat) / n)
    results.append(run_test("3. Tỷ lệ Gender = Male", "p", P0, p_hat, "two", "Z", z, "z", (),
                            lambda a: sym_ci(p_hat, se_p, "z", None, a), f"p = {P0:g}"))

    # ---- 2 tổng thể (Male vs Female) ----
    y1, y2 = y[male], y[~male]
    n1, n2 = len(y1), len(y2)
    m1, m2, v1, v2 = sample_mean(y1), sample_mean(y2), sample_var(y1), sample_var(y2)

    F = v1 / v2
    def ratio_ci(a):
        d1, d2 = n1 - 1, n2 - 1
        if a == "two":
            return F / stats.f.ppf(1 - ALPHA / 2, d1, d2), F / stats.f.ppf(ALPHA / 2, d1, d2)
        return (F / stats.f.ppf(1 - ALPHA, d1, d2), np.inf) if a == "right" else (0.0, F / stats.f.ppf(ALPHA, d1, d2))
    r_var = run_test("4. So sánh 2 phương sai Calories (Male/Female)", "σ₁²/σ₂²", 1.0, F, "two", "F", F, "f",
                     (n1 - 1, n2 - 1), ratio_ci, "σ₁²/σ₂² = 1")
    r_var["H0"], r_var["H1"] = "σ₁² = σ₂²", "σ₁² ≠ σ₂²"
    results.append(r_var)
    equal_var = r_var["KL (P-giá trị)"] == "Không bác bỏ H0"

    d = m1 - m2
    if equal_var:
        sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)
        se_d, df_d, mname = np.sqrt(sp2 * (1 / n1 + 1 / n2)), n1 + n2 - 2, "t gộp"
    else:
        se_d = np.sqrt(v1 / n1 + v2 / n2)
        df_d = se_d**4 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
        mname = "t Welch"
    for alt, lab in (("two", "5a"), ("right", "5b")):
        r = run_test(f"{lab}. So sánh 2 kỳ vọng Calories ({mname})", "μ₁−μ₂", 0.0, d, alt, "T", d / se_d, "t", (df_d,),
                     lambda a: sym_ci(d, se_d, "t", df_d, a), "μ₁ = μ₂")
        r["H0"], r["H1"] = "μ₁ = μ₂", f"μ₁ {ALT_TXT[alt]} μ₂"
        results.append(r)

    pm, pf = sample_prop(y1 >= HIGH_CAL), sample_prop(y2 >= HIGH_CAL)
    x1, x2 = np.sum(y1 >= HIGH_CAL), np.sum(y2 >= HIGH_CAL)
    pbar = (x1 + x2) / (n1 + n2)
    zz = (pm - pf) / np.sqrt(pbar * (1 - pbar) * (1 / n1 + 1 / n2))
    se_u = np.sqrt(pm * (1 - pm) / n1 + pf * (1 - pf) / n2)
    r = run_test(f"6. So sánh 2 tỷ lệ Calories ≥ {HIGH_CAL:.0f} (Male/Female)", "p₁−p₂", 0.0, pm - pf, "two", "Z", zz, "z", (),
                 lambda a: sym_ci(pm - pf, se_u, "z", None, a), "p₁ = p₂")
    r["H0"], r["H1"] = "p₁ = p₂", "p₁ ≠ p₂"
    results.append(r)

    res = pd.DataFrame(results)
    res.to_csv(TABLES_DIR / "03_parametric_tests.csv", index=False, encoding="utf-8-sig")

    # ---- Sai lầm loại II ----
    sy = np.sqrt(s2y)
    pw = []
    for dd in (0.1, 0.2, 0.5):
        pw.append(("Kỳ vọng Calories (1 mẫu)", f"μ₁ = μ₀ + {dd}·s (hiệu ứng d={dd})", power_two_sided(dd * np.sqrt(n))))
    for dd in (0.1, 0.2, 0.5):
        pw.append(("So sánh 2 kỳ vọng Male/Female", f"|μ₁−μ₂| = {dd}·s (d={dd})", power_two_sided(dd * np.sqrt(n1 * n2 / (n1 + n2)))))
    for dp in (0.03, 0.05, 0.10):
        pw.append(("Tỷ lệ Male (1 mẫu)", f"p₁ = p₀ + {dp}", power_prop(P0, P0 + dp, n)))
    pwr = pd.DataFrame([{"Kiểm định": a, "Phương án đối cụ thể": b, "α = P(sai lầm loại I)": ALPHA,
                         "β = P(sai lầm loại II)": 1 - c, "Lực kiểm định 1−β": c} for a, b, c in pw])
    pwr.to_csv(TABLES_DIR / "03_error_power.csv", index=False, encoding="utf-8-sig")

    pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 45)
    print(res[["Kiểm định", "Thống kê", "Giá trị thống kê", "P-giá trị", "KL (miền bác bỏ)", "KL (P-giá trị)", "KL (KTC)", "Nhất quán 3 cách"]].to_string(index=False))
    print(pwr.round(4).to_string(index=False))

    # ---- Báo cáo ----
    short = res[["Kiểm định", "H0", "H1", "Thống kê", "Giá trị thống kê", "Phân phối", "P-giá trị"]]
    concl = "\n".join(
        f"- **{r['Kiểm định']}** — miền bác bỏ: {r['Miền bác bỏ']}; P-giá trị = {r['P-giá trị']:.4g}; KTC {r['KTC tương ứng']}. "
        f"Kết luận ở mức α = {ALPHA}: **{r['KL (P-giá trị)']}**"
        f"{'' if r['Nhất quán 3 cách'] else ' (lưu ý: 3 cách chưa nhất quán do KTC Wald dùng sai số chuẩn khác kiểm định)'}."
        for _, r in res.iterrows())
    md = f"""# Chương 3 (phần 1). Kiểm định giả thuyết về tham số

## 3.1. Quy trình 5 bước

1. Phát biểu $H_0$ và $H_1$ (giả thuyết hai phía hoặc một phía).
2. Chọn mức ý nghĩa $\\alpha={ALPHA}$ và thống kê kiểm định cùng phân phối của nó dưới $H_0$.
3. Tính giá trị thống kê từ mẫu.
4. Ra quyết định theo ba cách tương đương:
   - **Miền bác bỏ:** bác bỏ $H_0$ nếu thống kê rơi vào miền bác bỏ cho bởi giá trị tới hạn.
   - **P-giá trị:** bác bỏ $H_0$ nếu $P\\text{{-value}}<\\alpha$.
   - **Khoảng tin cậy:** với $H_1$ hai phía, bác bỏ $H_0$ nếu $\\theta_0$ nằm ngoài khoảng tin cậy $(1-\\alpha)$ của $\\theta$ (với $H_1$ một phía dùng khoảng một phía).
5. Kết luận trong ngữ cảnh bài toán.

**Thống kê sử dụng:** $T=\\frac{{\\bar X-\\mu_0}}{{S/\\sqrt n}}\\sim t_{{n-1}}$; $\\chi^2=\\frac{{(n-1)S^2}}{{\\sigma_0^2}}\\sim\\chi^2_{{n-1}}$; $Z=\\frac{{\\hat p-p_0}}{{\\sqrt{{p_0(1-p_0)/n}}}}$; $F=S_1^2/S_2^2\\sim F_{{n_1-1,n_2-1}}$; $T=\\frac{{\\bar X_1-\\bar X_2}}{{\\sqrt{{S_p^2(1/n_1+1/n_2)}}}}$ (hoặc Welch); $Z=\\frac{{\\hat p_1-\\hat p_2}}{{\\sqrt{{\\bar p\\bar q(1/n_1+1/n_2)}}}}$.

Giá trị giả thuyết dùng trong bài: $\\mu_0={MU0:g}$, $\\sigma_0^2={VAR0:g}$, $p_0={P0:g}$.
Kiểm định so sánh hai kỳ vọng được chọn dạng {'t gộp' if equal_var else 't Welch'} theo kết quả kiểm định $F$ về hai phương sai.

## 3.2. Kết quả

{md_table(short)}

### Kết luận theo từng kiểm định

{concl}

## 3.3. Sai lầm loại I, loại II và lực kiểm định

- **Sai lầm loại I:** bác bỏ $H_0$ khi $H_0$ đúng, xác suất bằng $\\alpha={ALPHA}$.
- **Sai lầm loại II:** không bác bỏ $H_0$ khi $H_1$ đúng, xác suất $\\beta$; lực kiểm định $1-\\beta$.
- $\\beta$ giảm khi tăng cỡ mẫu $n$, tăng $\\alpha$ hoặc khi phương án đối lệch xa $H_0$.

Với kiểm định hai phía, xấp xỉ chuẩn: $1-\\beta=\\Phi(-z_{{1-\\alpha/2}}+\\lambda)+\\Phi(-z_{{1-\\alpha/2}}-\\lambda)$ với $\\lambda=d\\sqrt n$ (một mẫu), $\\lambda=d\\sqrt{{n_1n_2/(n_1+n_2)}}$ (hai mẫu), $d$ là hiệu ứng chuẩn hóa.

{md_table(pwr)}
"""
    (SECTIONS_DIR / "03_chap3_part1.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()