"""Chương 2 - Ước lượng điểm & Khoảng tin cậy 95%"""
"""
Biến phân tích:
  - Calories_Burned (Y): ước lượng kỳ vọng
  - Session_Duration (X1): ước lượng phương sai
  - Gender == "Male": ước lượng tỷ lệ
  - So sánh 2 tổng thể theo Gender: hiệu 2 kỳ vọng (sau khi xét tỷ số 2 phương sai), hiệu 2 tỷ lệ
"""

import numpy as np
import pandas as pd
from scipy import stats  # chỉ để tra giá trị tới hạn

from stats_utils import (SECTIONS_DIR, TABLES_DIR, load_data, md_table,
                         sample_mean, sample_prop, sample_std, sample_var)

ALPHA = 0.05
HIGH_CAL = 1000.0  # ngưỡng "đốt nhiều calo" để định nghĩa tỷ lệ cho bài toán hiệu 2 tỷ lệ
CONF = int(round((1 - ALPHA) * 100))


# ---------------------------------------------------------------------------
# Hàm tính khoảng tin cậy (tự cài đặt công thức, scipy chỉ tra quantile)
# ---------------------------------------------------------------------------
def sym_cis(est, se, dist, df=None, alpha=ALPHA):
    q = (lambda p: stats.t.ppf(p, df)) if dist == "t" else stats.norm.ppf
    c2, c1 = q(1 - alpha / 2), q(1 - alpha)
    return {
        "Hai phía": (est - c2 * se, est + c2 * se),
        "Một phía (cận dưới)": (est - c1 * se, np.inf),
        "Một phía (cận trên)": (-np.inf, est + c1 * se),
    }


def var_cis(s2, n, alpha=ALPHA):
    k = (n - 1) * s2
    return {
        "Hai phía": (k / stats.chi2.ppf(1 - alpha / 2, n - 1), k / stats.chi2.ppf(alpha / 2, n - 1)),
        "Một phía (cận dưới)": (k / stats.chi2.ppf(1 - alpha, n - 1), np.inf),
        "Một phía (cận trên)": (0.0, k / stats.chi2.ppf(alpha, n - 1)),
    }


def ratio_var_cis(s1, s2, n1, n2, alpha=ALPHA):
    r = s1 / s2
    d1, d2 = n1 - 1, n2 - 1
    return {
        "Hai phía": (r / stats.f.ppf(1 - alpha / 2, d1, d2), r / stats.f.ppf(alpha / 2, d1, d2)),
        "Một phía (cận dưới)": (r / stats.f.ppf(1 - alpha, d1, d2), np.inf),
        "Một phía (cận trên)": (0.0, r / stats.f.ppf(alpha, d1, d2)),
    }


ROWS = []


def add(chi_tieu, tham_so, phuong_phap, est, cis, n, dieu_kien):
    for kind, (lo, hi) in cis.items():
        ROWS.append({"Chỉ tiêu": chi_tieu, "Tham số": tham_so, "Phương pháp": phuong_phap,
                     "Loại KTC": kind, "Ước lượng điểm": est, "Cận dưới": lo, "Cận trên": hi,
                     "n": n, "Điều kiện áp dụng": dieu_kien})


def main():
    df = load_data()
    y = df["Calories_Burned"].to_numpy(float)
    x = df["Session_Duration"].to_numpy(float)
    male = (df["Gender"].str.strip().str.lower() == "male").to_numpy()
    n = len(df)

    # ---------------- Ước lượng điểm ----------------
    ybar, s2y, s2y_mle = sample_mean(y), sample_var(y), sample_var(y, 0)
    xbar, s2x, s2x_mle = sample_mean(x), sample_var(x), sample_var(x, 0)
    p_hat = sample_prop(male)
    point = pd.DataFrame([
        {"Tham số": "μ (Calories_Burned)", "MoM": ybar, "MLE": ybar, "Ước lượng hiệu chỉnh": ybar},
        {"Tham số": "σ² (Calories_Burned)", "MoM": s2y_mle, "MLE": s2y_mle, "Ước lượng hiệu chỉnh": s2y},
        {"Tham số": "μ (Session_Duration)", "MoM": xbar, "MLE": xbar, "Ước lượng hiệu chỉnh": xbar},
        {"Tham số": "σ² (Session_Duration)", "MoM": s2x_mle, "MLE": s2x_mle, "Ước lượng hiệu chỉnh": s2x},
        {"Tham số": "p (Gender = Male)", "MoM": p_hat, "MLE": p_hat, "Ước lượng hiệu chỉnh": p_hat},
    ])
    point.to_csv(TABLES_DIR / "02_point_estimates.csv", index=False, encoding="utf-8-sig")

    # ---------------- KTC ----------------
    # 1) Kỳ vọng Calories_Burned (σ chưa biết -> t_{n-1}; n lớn nên xấp xỉ z)
    se = sample_std(y) / np.sqrt(n)
    add("Kỳ vọng Calories_Burned", "μ", "t-Student (σ chưa biết)", ybar, sym_cis(ybar, se, "t", n - 1), n,
        "Y xấp xỉ chuẩn hoặc n đủ lớn (n≥30)")

    # 2) Phương sai Session_Duration
    add("Phương sai Session_Duration", "σ²", "Chi-bình phương", s2x, var_cis(s2x, n), n,
        "X ~ chuẩn (nhạy với vi phạm giả thiết chuẩn)")
    sd_ci = {k: (np.sqrt(lo), np.sqrt(hi)) for k, (lo, hi) in var_cis(s2x, n).items()}
    add("Độ lệch chuẩn Session_Duration", "σ", "Chi-bình phương (căn bậc hai)", np.sqrt(s2x), sd_ci, n,
        "Như trên")

    # 3) Tỷ lệ Male (Wald)
    cond_p = (n * p_hat >= 5) and (n * (1 - p_hat) >= 5)
    se_p = np.sqrt(p_hat * (1 - p_hat) / n)
    add("Tỷ lệ Gender = Male", "p", "Xấp xỉ chuẩn (Wald)", p_hat, sym_cis(p_hat, se_p, "z"), n,
        f"n·p̂≥5 và n(1−p̂)≥5: {'thỏa' if cond_p else 'KHÔNG thỏa'}")

    # 4) So sánh Male vs Female
    y1, y2 = y[male], y[~male]
    n1, n2 = len(y1), len(y2)
    m1, m2 = sample_mean(y1), sample_mean(y2)
    v1, v2 = sample_var(y1), sample_var(y2)
    ratio_cis = ratio_var_cis(v1, v2, n1, n2)
    add("Tỷ số phương sai Calories (Male/Female)", "σ₁²/σ₂²", "F-Fisher", v1 / v2, ratio_cis, n1 + n2,
        "2 mẫu độc lập, mỗi tổng thể ~ chuẩn")
    lo_r, hi_r = ratio_cis["Hai phía"]
    equal_var = lo_r <= 1 <= hi_r  # KTC chứa 1 -> không bác bỏ σ1² = σ2²
    d = m1 - m2
    # Cả hai phương án; chọn theo kết quả KTC tỷ số phương sai
    sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)
    se_pool = np.sqrt(sp2 * (1 / n1 + 1 / n2))
    se_w = np.sqrt(v1 / n1 + v2 / n2)
    df_w = se_w**4 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    pool_cis = sym_cis(d, se_pool, "t", n1 + n2 - 2)
    welch_cis = sym_cis(d, se_w, "t", df_w)
    chosen = pool_cis if equal_var else welch_cis
    chosen_name = "t gộp (σ₁²=σ₂²)" if equal_var else "t Welch (σ₁²≠σ₂²)"
    add("Hiệu 2 kỳ vọng Calories (Male − Female)", "μ₁−μ₂", chosen_name, d, chosen, n1 + n2,
        "Đã kiểm tra tỷ số phương sai bằng KTC F; n1, n2 lớn")
    other = welch_cis if equal_var else pool_cis
    other_name = "t Welch (đối chiếu)" if equal_var else "t gộp (đối chiếu)"
    add("Hiệu 2 kỳ vọng Calories (Male − Female)", "μ₁−μ₂", other_name, d, {"Hai phía": other["Hai phía"]},
        n1 + n2, "Chỉ để đối chiếu")

    # 5) Hiệu 2 tỷ lệ: tỷ lệ buổi tập đốt ≥ HIGH_CAL calo
    pm, pf = sample_prop(y1 >= HIGH_CAL), sample_prop(y2 >= HIGH_CAL)
    se_d = np.sqrt(pm * (1 - pm) / n1 + pf * (1 - pf) / n2)
    cond_2p = min(n1 * pm, n1 * (1 - pm), n2 * pf, n2 * (1 - pf)) >= 5
    add(f"Hiệu 2 tỷ lệ buổi tập Calories ≥ {HIGH_CAL:.0f} (Male − Female)", "p₁−p₂", "Xấp xỉ chuẩn (Wald)",
        pm - pf, sym_cis(pm - pf, se_d, "z"), n1 + n2,
        f"n·p̂ và n(1−p̂) mỗi nhóm ≥5: {'thỏa' if cond_2p else 'KHÔNG thỏa'}")

    res = pd.DataFrame(ROWS)
    res.to_csv(TABLES_DIR / "02_confidence_intervals.csv", index=False, encoding="utf-8-sig")

    # ---------------- Console ----------------
    pd.set_option("display.width", 200, "display.max_columns", 20, "display.max_colwidth", 40)
    print(point.to_string(index=False))
    print(res.drop(columns=["Điều kiện áp dụng"]).round(4).to_string(index=False))
    print(f"\nn_male={n1}, n_female={n2}, σ₁²=σ₂²? {equal_var}")

    # ---------------- Báo cáo (Markdown + LaTeX) ----------------
    two = res[res["Loại KTC"] == "Hai phía"].drop(columns=["Loại KTC", "Điều kiện áp dụng", "Phương pháp"])
    one = res[res["Loại KTC"] != "Hai phía"][["Chỉ tiêu", "Loại KTC", "Cận dưới", "Cận trên"]]
    md = f"""# Chương 2. Ước lượng điểm và ước lượng khoảng

## 2.1. Ước lượng điểm

Với mẫu ngẫu nhiên $X_1,\\dots,X_n$ từ $N(\\mu,\\sigma^2)$:

- Phương pháp mô-men (MoM): $\\hat\\mu=\\bar X$, $\\hat\\sigma^2_{{MoM}}=\\frac1n\\sum(X_i-\\bar X)^2$.
- Phương pháp hợp lý cực đại (MLE): cho cùng kết quả $\\hat\\mu=\\bar X$, $\\hat\\sigma^2_{{MLE}}=\\frac1n\\sum(X_i-\\bar X)^2$ (chệch); ước lượng không chệch là $S^2=\\frac1{{n-1}}\\sum(X_i-\\bar X)^2$.
- Tỷ lệ (Bernoulli): MoM và MLE đều là $\\hat p=\\frac{{\\text{{số quan sát thỏa}}}}{{n}}$.

{md_table(point)}

## 2.2. Khoảng tin cậy {CONF}% (α = {ALPHA})

**Công thức và điều kiện áp dụng**

| Tham số | Khoảng tin cậy hai phía | Điều kiện |
|---|---|---|
| $\\mu$ ($\\sigma$ chưa biết) | $\\bar X\\pm t_{{n-1;1-\\alpha/2}}\\,S/\\sqrt n$ | tổng thể chuẩn hoặc $n\\ge30$ |
| $\\sigma^2$ | $\\left(\\frac{{(n-1)S^2}}{{\\chi^2_{{n-1;1-\\alpha/2}}}},\\frac{{(n-1)S^2}}{{\\chi^2_{{n-1;\\alpha/2}}}}\\right)$ | tổng thể chuẩn |
| $p$ | $\\hat p\\pm z_{{1-\\alpha/2}}\\sqrt{{\\hat p(1-\\hat p)/n}}$ | $n\\hat p\\ge5$, $n(1-\\hat p)\\ge5$ |
| $\\sigma_1^2/\\sigma_2^2$ | $\\left(\\frac{{S_1^2/S_2^2}}{{F_{{n_1-1,n_2-1;1-\\alpha/2}}}},\\frac{{S_1^2/S_2^2}}{{F_{{n_1-1,n_2-1;\\alpha/2}}}}\\right)$ | 2 mẫu độc lập, chuẩn |
| $\\mu_1-\\mu_2$ ($\\sigma_1^2=\\sigma_2^2$) | $\\bar X_1-\\bar X_2\\pm t_{{n_1+n_2-2;1-\\alpha/2}}S_p\\sqrt{{1/n_1+1/n_2}}$ | $S_p^2=\\frac{{(n_1-1)S_1^2+(n_2-1)S_2^2}}{{n_1+n_2-2}}$ |
| $\\mu_1-\\mu_2$ ($\\sigma_1^2\\ne\\sigma_2^2$) | $\\bar X_1-\\bar X_2\\pm t_{{\\nu;1-\\alpha/2}}\\sqrt{{S_1^2/n_1+S_2^2/n_2}}$ | $\\nu$ theo Welch–Satterthwaite |
| $p_1-p_2$ | $\\hat p_1-\\hat p_2\\pm z_{{1-\\alpha/2}}\\sqrt{{\\frac{{\\hat p_1\\hat q_1}}{{n_1}}+\\frac{{\\hat p_2\\hat q_2}}{{n_2}}}}$ | mỗi nhóm $n\\hat p,n\\hat q\\ge5$ |

Khoảng một phía: thay $\\alpha/2$ bằng $\\alpha$ và chỉ lấy một cận.

**Kết quả (hai phía)**

{md_table(two)}

**Kết quả (một phía)**

{md_table(one)}

**Chọn phương pháp so sánh 2 kỳ vọng.** Khoảng tin cậy {CONF}% cho $\\sigma_1^2/\\sigma_2^2$ là ({lo_r:.4f}; {hi_r:.4f}) nên
{'chứa 1 → không bác bỏ $\\sigma_1^2=\\sigma_2^2$, dùng t gộp.' if equal_var else 'không chứa 1 → phương sai khác nhau, dùng t Welch.'}

## 2.3. Ý nghĩa mức tin cậy {CONF}%

Mức tin cậy {CONF}% **không** có nghĩa là "xác suất tham số nằm trong khoảng cụ thể vừa tính là {CONF}%" (tham số là hằng số chưa biết, khoảng cụ thể hoặc chứa hoặc không chứa nó). Ý nghĩa theo **tần suất**: nếu lặp lại việc lấy mẫu cỡ $n$ và dựng khoảng bằng cùng một quy trình rất nhiều lần thì khoảng {CONF}% các khoảng thu được sẽ chứa tham số thật.
"""
    (SECTIONS_DIR / "02_chap2.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()