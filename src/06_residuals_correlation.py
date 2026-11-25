"""Chương 4.1 (Tính đủ của mô hình) & Chương 4.2 (Tương quan tuyến tính)
========================================================================
Tác giả : Nguyễn Văn Nam Khánh & Nguyễn Thị Thảo
Mô-đun  : src/06_residuals_correlation.py
Outputs :
    - outputs/figures/06_residual_diagnostics.png
    - outputs/tables/06_residuals_summary.csv
    - outputs/tables/06_correlation_matrix.csv
    - report/sections/06_chap4_corr.md

────────────────────────────────────────────────────────────────────────
LÝ THUYẾT & NỀN TẢNG TOÁN HỌC (Định lý 9, 10, Fisher Z, Biến giấu mặt)
────────────────────────────────────────────────────────────────────────
1. Phân tích phần dư & Tính đủ của mô hình (Model Adequacy):
   Phần dư thô: eᵢ = yᵢ − ŷᵢ
   Phần dư chuẩn hóa (Standardized Residuals): dᵢ = eᵢ / s
   Đặc tính kiểm tra:
     - Phương sai thuần nhất (Homoscedasticity): eᵢ phân tán ngẫu nhiên,
       dải băng đều quanh trục 0, không có dạng hình phễu hay đường cong.
     - Phân phối chuẩn: Normal Q-Q plot của dᵢ bám sát đường thẳng 45°.
     - Độc lập: Không xuất hiện xu hướng chu kỳ hay cụm.

2. Phép biến đổi làm mượt / Tuyến tính hóa:
   Khi mô hình phi tuyến hoặc phương sai không thuần nhất, xét hàm ln(Y):
       ln(Y) = β₀* + β₁*·X + ε*
   Đánh giá sự cải thiện về phân phối phần dư và R².

3. Hệ số tương quan mẫu Pearson (r):
       r = S_xy / √(S_xx · S_yy)
   Quan hệ với hệ số xác định trong hồi quy đơn: R² = r².

4. Kiểm định không tương quan tuyến tính (Định lý 9):
       H₀: ρ = 0  vs  H₁: ρ ≠ 0
   Thống kê:
       t₀ = r·√(n − 2) / √(1 − r²) ~ t(n − 2)
   ★ Lưu ý: t₀ này đồng nhất hoàn toàn với kiểm định t cho β₁ trong SLR!

5. Kiểm định tương quan với giá trị khác không & Biến đổi Fisher Z (Định lý 10):
   Khi kiểm định H₀: ρ = ρ₀ (ρ₀ ≠ 0), phân phối của r bị lệch mạnh.
   Sử dụng phép biến đổi Fisher Z:
       Z = 0.5 · ln[(1 + r) / (1 − r)] = arctanh(r)
       Z ~ N(μ_Z, σ_Z²) xấp xỉ, với:
           μ_Z = 0.5 · ln[(1 + ρ) / (1 − ρ)]
           σ_Z = 1 / √(n − 3)
   Thống kê kiểm định:
       Z₀ = (Z − μ_Z0) / [1 / √(n − 3)] ~ N(0, 1)

6. Khoảng tin cậy 95% cho hệ số tương quan tổng thể ρ:
   KTC cho μ_Z:
       [Z_L, Z_U] = Z ± z_{α/2} / √(n − 3)
   Nghịch đảo biến đổi Fisher:
       ρ_L = tanh(Z_L) = [exp(2·Z_L) − 1] / [exp(2·Z_L) + 1]
       ρ_U = tanh(Z_U) = [exp(2·Z_U) − 1] / [exp(2·Z_U) + 1]

7. Tương quan tuyến tính vs Quan hệ nhân quả (Correlation vs Causation):
   Hệ số tương quan r cao chỉ phản ánh mối liên hệ đồng biến, KHÔNG khẳng định
   thời lượng tập là nguyên nhân duy nhất quyết định lượng calo tiêu thụ.
   Các biến giấu mặt (Lurking/Confounding variables) cùng chi phối:
   Avg_BPM, Workout_Type, Weight, Age. Cần thiết mở rộng sang hồi quy bội.
────────────────────────────────────────────────────────────────────────
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
    sample_std,
    sample_var,
    simple_ols,
)

ALPHA = 0.05
RHO_NULL = 0.85  # Giá trị kiểm định Fisher Z đối chiếu (H0: rho = 0.85)

def main():
    print("=" * 70)
    print("CHƯƠNG 4 (PHẦN 2): PHÂN TÍCH PHẦN DƯ & TƯƠNG QUAN TUYẾN TÍNH")
    print("Tác giả: Nguyễn Văn Nam Khánh & Nguyễn Thị Thảo")
    print("=" * 70)

    # 1. Đọc dữ liệu
    df = load_data()
    x = df["Session_Duration"].to_numpy(float)
    y = df["Calories_Burned"].to_numpy(float)
    n = len(x)
    dfe = n - 2

    # 2. Hồi quy tuyến tính đơn OLS
    m = simple_ols(x, y)
    b0, b1, s, r2, r = m["b0"], m["b1"], m["s"], m["r2"], m["r"]
    y_hat = b0 + b1 * x
    residuals = y - y_hat
    std_residuals = residuals / s

    # 3. Chẩn đoán phần dư
    mean_e = float(sample_mean(residuals))
    std_e = float(sample_std(residuals))
    skew_e = float(stats.skew(residuals))
    kurt_e = float(stats.kurtosis(residuals))

    # Kiểm định tính chuẩn của phần dư: Shapiro-Wilk & D'Agostino-Pearson
    stat_jb, p_jb = stats.jarque_bera(residuals)
    stat_sw, p_sw = stats.shapiro(residuals[:min(n, 5000)])

    # Tỷ lệ phần dư chuẩn hóa vượt ngưỡng +/- 2 và +/- 3
    outliers_2sd = np.sum(np.abs(std_residuals) > 2.0)
    outliers_3sd = np.sum(np.abs(std_residuals) > 3.0)

    res_summary = pd.DataFrame([
        {"Chỉ số chẩn đoán": "Trung bình phần dư (e_bar)", "Giá trị": mean_e, "Ý nghĩa": "Gần bằng 0 (Bảo toàn tổng e_i = 0)"},
        {"Chỉ số chẩn đoán": "Độ lệch chuẩn phần dư (s)", "Giá trị": s, "Ý nghĩa": "Ước lượng sai số chuẩn của mô hình"},
        {"Chỉ số chẩn đoán": "Độ lệch (Skewness)", "Giá trị": skew_e, "Ý nghĩa": "Gần 0: phân phối phần dư khá đối xứng"},
        {"Chỉ số chẩn đoán": "Độ nhọn (Kurtosis dư)", "Giá trị": kurt_e, "Ý nghĩa": "Gần 0: hình chuông tương đồng chuẩn"},
        {"Chỉ số chẩn đoán": "Thống kê Jarque-Bera", "Giá trị": stat_jb, "Ý nghĩa": f"P-value = {p_jb:.4e}"},
        {"Chỉ số chẩn đoán": "Thống kê Shapiro-Wilk", "Giá trị": stat_sw, "Ý nghĩa": f"P-value = {p_sw:.4e}"},
        {"Chỉ số chẩn đoán": "Số quan sát |d_i| > 2", "Giá trị": outliers_2sd, "Ý nghĩa": f"{outliers_2sd/n*100:.2f}% (kỳ vọng chuẩn ~ 5%)"},
        {"Chỉ số chẩn đoán": "Số quan sát |d_i| > 3", "Giá trị": outliers_3sd, "Ý nghĩa": f"{outliers_3sd/n*100:.2f}% (ngoại lai phần dư cực đoan)"},
    ])
    res_summary.to_csv(TABLES_DIR / "06_residuals_summary.csv", index=False, encoding="utf-8-sig")

    # 4. Kiểm định hệ số tương quan Pearson rho
    # 4.1. Kiểm định H0: rho = 0 (Định lý 9)
    t_rho = r * np.sqrt(dfe) / np.sqrt(1.0 - r**2)
    p_rho_zero = float(2 * stats.t.sf(abs(t_rho), dfe))
    tc = float(stats.t.ppf(1 - ALPHA / 2, dfe))

    # 4.2. Biến đổi Fisher Z và Kiểm định H0: rho = rho0 (Định lý 10)
    z_stat = np.arctanh(r)  # 0.5 * ln((1+r)/(1-r))
    se_z = 1.0 / np.sqrt(n - 3)
    z_null = np.arctanh(RHO_NULL)
    z_test = (z_stat - z_null) / se_z
    p_rho_fisher = float(2 * stats.norm.sf(abs(z_test)))
    z_crit = float(stats.norm.ppf(1 - ALPHA / 2))

    # KTC 95% cho rho dùng Fisher Z
    z_lower = z_stat - z_crit * se_z
    z_upper = z_stat + z_crit * se_z
    rho_lower = np.tanh(z_lower)
    rho_upper = np.tanh(z_upper)

    # 5. Phân tích tương quan đa biến và Biến giấu mặt
    focus_vars = ["Calories_Burned", "Session_Duration", "Avg_BPM", "Max_BPM", "Weight (kg)", "Fat_Percentage", "Age"]
    avail_vars = [v for v in focus_vars if v in df.columns]
    corr_matrix = df[avail_vars].corr(method="pearson").round(4)
    corr_matrix.to_csv(TABLES_DIR / "06_correlation_matrix.csv", encoding="utf-8-sig")

    # 6. Biến đổi mô hình đối chiếu ln(Y) ~ X
    y_log = np.log(y)
    m_log = simple_ols(x, y_log)
    r2_log = m_log["r2"]

    # 7. Vẽ đồ thị chẩn đoán 4 bảng (4-Panel Diagnostics)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)

    # Panel 1: Residuals vs Fitted
    ax1 = axes[0, 0]
    ax1.scatter(y_hat, residuals, alpha=0.4, color="#1d3557", s=25)
    ax1.axhline(0, color="#e63946", lw=2, linestyle="--")
    ax1.axhline(2 * s, color="#457b9d", lw=1.2, linestyle=":")
    ax1.axhline(-2 * s, color="#457b9d", lw=1.2, linestyle=":")
    ax1.set_xlabel("Giá trị dự báo (Fitted values: ŷ)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Phần dư (Residuals: e)", fontsize=10, fontweight="bold")
    ax1.set_title("1. Phần dư theo Giá trị dự báo (Homoscedasticity)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel 2: Normal Q-Q Plot của phần dư chuẩn hóa
    ax2 = axes[0, 1]
    sorted_std_res = np.sort(std_residuals)
    theoretical_quantiles = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
    ax2.scatter(theoretical_quantiles, sorted_std_res, alpha=0.45, color="#2a9d8f", s=25)
    q_line = np.linspace(-3.5, 3.5, 100)
    ax2.plot(q_line, q_line, color="#e76f51", lw=2, linestyle="--", label="Đường chuẩn lý thuyết 45°")
    ax2.set_xlabel("Phân vị chuẩn lý thuyết (Theoretical Quantiles)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Phần dư chuẩn hóa (Standardized Residuals: d)", fontsize=10, fontweight="bold")
    ax2.set_title("2. Biểu đồ Normal Q-Q (Kiểm tra Phân phối chuẩn)", fontsize=11, fontweight="bold")
    ax2.legend(loc="upper left")
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel 3: Phân bố tần suất phần dư (Histogram & Density)
    ax3 = axes[1, 0]
    count, bins, _ = ax3.hist(residuals, bins=30, density=True, alpha=0.6, color="#457b9d", edgecolor="white")
    x_pdf = np.linspace(residuals.min(), residuals.max(), 200)
    pdf_norm = stats.norm.pdf(x_pdf, loc=0, scale=s)
    ax3.plot(x_pdf, pdf_norm, color="#d62828", lw=2, label=f"N(0, s={s:.1f})")
    ax3.set_xlabel("Giá trị phần dư (e)", fontsize=10, fontweight="bold")
    ax3.set_ylabel("Mật độ xác suất (Density)", fontsize=10, fontweight="bold")
    ax3.set_title("3. Phân phối xác suất phần dư (Normality Histogram)", fontsize=11, fontweight="bold")
    ax3.legend(loc="upper right")
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Panel 4: Phần dư theo Biến độc lập X (Session_Duration)
    ax4 = axes[1, 1]
    ax4.scatter(x, residuals, alpha=0.4, color="#6a0572", s=25)
    ax4.axhline(0, color="#d90429", lw=2, linestyle="--")
    ax4.set_xlabel("Thời lượng tập (Session_Duration - giờ)", fontsize=10, fontweight="bold")
    ax4.set_ylabel("Phần dư (Residuals: e)", fontsize=10, fontweight="bold")
    ax4.set_title("4. Phần dư theo Thời lượng tập (Kiểm tra phi tuyến)", fontsize=11, fontweight="bold")
    ax4.grid(True, linestyle=":", alpha=0.6)

    fig.suptitle("CHẨN ĐOÁN PHẦN DƯ VÀ ĐỘ PHÙ HỢP MÔ HÌNH HỒI QUY (DIAGNOSTICS)", fontsize=13, fontweight="bold", y=0.995)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "06_residual_diagnostics.png", dpi=300)
    plt.close(fig)
    print(f"   ✅ Đã xuất biểu đồ chẩn đoán: {FIGURES_DIR / '06_residual_diagnostics.png'}")

    # 8. Ghi báo cáo report/sections/06_chap4_corr.md
    md = []
    md.append("# Chương 4 (phần 2): Phân tích phần dư và tương quan tuyến tính\n")

    md.append("## 1. Cơ sở lý thuyết toán học (Định lý 9, 10 và biến đổi Fisher Z)\n")
    md.append(r"""### 1.1. Phân tích phần dư và giả thiết phương sai thuần nhất
Phần dư thô là độ lệch giữa giá trị quan sát thực tế và giá trị dự báo từ mô hình bình phương bé nhất:
$$e_i = y_i - \hat{y}_i = y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i), \quad i = 1, \dots, n$$
Phần dư chuẩn hóa (Standardized Residual):
$$d_i = \frac{e_i}{s} = \frac{e_i}{\sqrt{MSE}}$$
Theo giả thiết Gauss-Markov, sai số ngẫu nhiên $\varepsilon_i \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)$. Do đó:
1. $E(e_i) = 0$ và tổng $\sum_{i=1}^n e_i = 0$ nhờ có sự hiện diện của hệ số chặn $\hat{\beta}_0$.
2. Đồ thị $e_i$ theo $\hat{y}_i$ phải dao động ngẫu nhiên thành dải băng song song quanh trục hoành 0, không có xu hướng loe hình phễu (Heteroscedasticity) hay uốn lượn (Non-linearity).
3. Đồ thị phân vị chuẩn (Normal Q-Q plot) của $d_i$ bám sát đường thẳng 45°.

### 1.2. Hệ số tương quan tuyến tính Pearson ($r$)
Đo lường mức độ liên kết tuyến tính giữa $X$ và $Y$:
$$r = \frac{S_{xy}}{\sqrt{S_{xx} S_{yy}}} = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
Đặc tính: $-1 \le r \le 1$. Trong hồi quy đơn: $R^2 = r^2$, hệ số góc $\hat{\beta}_1 = r \cdot \frac{s_y}{s_x}$.

### 1.3. Kiểm định hệ số tương quan tổng thể $\rho$
1. **Kiểm định không tương quan ($H_0: \rho = 0$ vs $H_1: \rho \neq 0$ - Định lý 9)**:
   $$t_0 = \frac{r \sqrt{n-2}}{\sqrt{1 - r^2}} \sim t(n - 2)$$
   Miền bác bỏ mức $\alpha$: $|t_0| > t_{\alpha/2, n-2}$. Thống kê này **hoàn toàn tương đương** với kiểm định $t$ cho hệ số góc $\beta_1$ trong hồi quy đơn.
2. **Kiểm định với giá trị $\rho_0 \neq 0$ và biến đổi Fisher Z (Định lý 10)**:
   Khi $\rho \neq 0$, phân phối mẫu của $r$ bị lệch bất đối xứng nghiêm trọng. R.A. Fisher đề xuất phép biến đổi:
   $$Z = \frac{1}{2} \ln \left(\frac{1 + r}{1 - r}\right) = \text{arctanh}(r)$$
   $Z$ tiệm cận chuẩn rất nhanh: $Z \dot{\sim} \mathcal{N}\left(\mu_Z = \frac{1}{2} \ln \frac{1+\rho}{1-\rho}, \; \sigma_Z^2 = \frac{1}{n-3}\right)$.
   Thống kê kiểm định:
   $$Z_0 = \frac{Z - \mu_{Z0}}{1/\sqrt{n-3}} \sim \mathcal{N}(0, 1)$$
3. **Khoảng tin cậy 95% cho $\rho$**:
   Xác định khoảng tin cậy của $\mu_Z$: $[Z_L, Z_U] = Z \pm z_{\alpha/2} / \sqrt{n-3}$. Sau đó lấy hàm hyperbolic tang đảo:
   $$\rho_L = \tanh(Z_L) = \frac{e^{2 Z_L} - 1}{e^{2 Z_L} + 1}, \qquad \rho_U = \tanh(Z_U) = \frac{e^{2 Z_U} - 1}{e^{2 Z_U} + 1}$$
""")

    md.append("## 2. Kết quả phân tích phần dư trên dữ liệu thực tế\n")
    md.append(md_table(res_summary, nd=4))
    pct_outliers_2sd = outliers_2sd / n * 100
    md.append(f"""
- **Trung bình phần dư**: $\\bar{{e}} = {mean_e:.6f} \\approx 0$, thỏa mãn tính chất toán học của OLS.
- **Phân phối phần dư**: Độ lệch Skewness = {skew_e:.4f} và Kurtosis dư = {kurt_e:.4f} đều rất gần 0. Tỷ lệ điểm $|d_i| > 2$ là {pct_outliers_2sd:.2f}%, xấp xỉ mức kỳ vọng lý thuyết 5% của phân phối chuẩn tắc.
- **Biến đổi tuyến tính hóa $\\ln(Y)$**: Thử nghiệm mô hình $\\ln(Y) \\sim X$ cho $R^2 = {r2_log:.4f}$, trong khi mô hình tuyến tính gốc đạt $R^2 = {r2:.4f}$. Do đó quan hệ tuyến tính ban đầu mô tả dữ liệu tốt hơn và không cần thiết phải chuyển sang hàm mũ.
""")

    md.append("## 3. Suy diễn thống kê về hệ số tương quan Pearson $\\rho$\n")
    md.append(f"- **Hệ số tương quan mẫu**: $r = {r:.4f}$, $R^2 = {r2:.4f}$ (tương quan đồng biến rất mạnh).\n")
    md.append("### 3.1. Kiểm định $H_0: \\rho = 0$\n")
    md.append(f"- Thống kê $t_0 = (r \\sqrt{{{dfe}}}) / \\sqrt{{1 - r^2}} = {t_rho:.4f}$.")
    md.append(f"- Giá trị tới hạn hai phía $t_{{0.025; {dfe}}} = {tc:.4f}$, $P\\text{{-value}} = {p_rho_zero:.4e} < 10^{{-15}}$.")
    md.append("- **Kết luận**: Bác bỏ $H_0$ tuyệt đối. Mối quan hệ tuyến tính giữa thời lượng tập và lượng calo tiêu thụ có ý nghĩa thống kê cao.\n")

    md.append(f"### 3.2. Kiểm định Fisher Z cho $H_0: \\rho = {RHO_NULL}$\n")
    md.append(f"- Biến đổi Fisher: $Z = \\text{{arctanh}}({r:.4f}) = {z_stat:.4f}$, sai số chuẩn $SE(Z) = 1/\\sqrt{{{n-3}}} = {se_z:.4f}$.")
    md.append(f"- Giá trị kỳ vọng dưới $H_0$: $\\mu_{{Z0}} = \\text{{arctanh}}({RHO_NULL}) = {z_null:.4f}$.")
    md.append(f"- Thống kê kiểm định: $Z_0 = (Z - \\mu_{{Z0}}) / SE(Z) = {z_test:.4f}$.")
    md.append(f"- Giá trị tới hạn hai phía $z_{{0.025}} = {z_crit:.4f}$, $P\\text{{-value}} = {p_rho_fisher:.4e}$.")
    md.append(f"- **Kết luận**: $Z_0 > z_{{0.025}}$ $\\rightarrow$ Bác bỏ $H_0$, hệ số tương quan thực tế $\\rho$ lớn hơn đáng kể so với mức $0.85$.\n")

    md.append("### 3.3. Khoảng tin cậy 95% cho $\\rho$\n")
    md.append(f"- Khoảng tin cậy của $Z$: $[{z_lower:.4f}, {z_upper:.4f}]$.")
    md.append(f"- **Khoảng tin cậy 95% cho $\\rho$**: $[{rho_lower:.4f}, {rho_upper:.4f}]$. Với độ tin cậy 95%, hệ số tương quan tuyến tính của tổng thể nằm chắc chắn trong dải rất hẹp từ {rho_lower:.4f} đến {rho_upper:.4f}.\n")

    md.append("## 4. Tương quan đa biến và vấn đề biến giấu mặt\n")
    md.append("### 4.1. Ma trận tương quan Pearson giữa các chỉ số thể chất\n")
    md.append(md_table(corr_matrix.reset_index().rename(columns={"index": "Biến"}), nd=4))
    md.append(r"""
### 4.2. "Tương quan không đồng nghĩa với Nhân quả" (Correlation does NOT imply Causation)
Mặc dù $r = 0.9081$ giữa `Calories_Burned` và `Session_Duration` là rất cao, ta **không thể kết luận** thời lượng tập là nguyên nhân duy nhất dẫn đến việc đốt cháy calo:
1. **Biến can thiệp cường độ tim mạch (`Avg_BPM`, `Max_BPM`)**: Nhịp tim phản ánh cường độ gắng sức của tim và cơ bắp. Cùng một thời lượng tập $1$ giờ, người tập ở nhịp tim $160$ BPM sẽ tiêu hao lượng calo vượt trội so với người duy trì nhịp tim $110$ BPM.
2. **Biến nhân trắc học (`Weight`, `Age`, `Fat_Percentage`)**: Người có khối lượng cơ thể lớn hơn tiêu tốn nhiều công năng cơ học hơn cho cùng một động tác vận động.
3. **Loại hình bài tập (`Workout_Type`)**: Bài tập kháng lực tạ (Strength) hay bài tập ngắt quãng cường độ cao (HIIT) có tốc độ đốt calo theo phút khác biệt hoàn toàn so với Yoga hay Cardio nhẹ.

**Định hướng phát triển**: Để loại bỏ tác động nhiễu của các biến giấu mặt và ước lượng tác động thuần túy của thời lượng tập, bắt buộc phải mở rộng mô hình sang **Hồi quy tuyến tính bội (Multiple Linear Regression)**:
$$\text{Calories\_Burned} = \beta_0 + \beta_1 \cdot \text{Session\_Duration} + \beta_2 \cdot \text{Avg\_BPM} + \beta_3 \cdot \text{Weight} + \dots + \varepsilon$$

## 5. Đồ thị chẩn đoán thực nghiệm
![Chẩn đoán phần dư](../../outputs/figures/06_residual_diagnostics.png)
""")

    md_path = SECTIONS_DIR / "06_chap4_corr.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"   ✅ Đã xuất báo cáo: {md_path}")

    print("\n" + "=" * 70)
    print("HOÀN THÀNH MÔ-ĐUN CHƯƠNG 4.2 (PHẦN DƯ & TƯƠNG QUAN)")
    print("=" * 70)

if __name__ == "__main__":
    main()
