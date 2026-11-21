# Chương 3 (phần 1). Kiểm định giả thuyết về tham số

## 3.1. Quy trình 5 bước

1. Phát biểu $H_0$ và $H_1$ (giả thuyết hai phía hoặc một phía).
2. Chọn mức ý nghĩa $\alpha=0.05$ và thống kê kiểm định cùng phân phối của nó dưới $H_0$.
3. Tính giá trị thống kê từ mẫu.
4. Ra quyết định theo ba cách tương đương:
   - **Miền bác bỏ:** bác bỏ $H_0$ nếu thống kê rơi vào miền bác bỏ cho bởi giá trị tới hạn.
   - **P-giá trị:** bác bỏ $H_0$ nếu $P\text{-value}<\alpha$.
   - **Khoảng tin cậy:** với $H_1$ hai phía, bác bỏ $H_0$ nếu $\theta_0$ nằm ngoài khoảng tin cậy $(1-\alpha)$ của $\theta$ (với $H_1$ một phía dùng khoảng một phía).
5. Kết luận trong ngữ cảnh bài toán.

**Thống kê sử dụng:** $T=\frac{\bar X-\mu_0}{S/\sqrt n}\sim t_{n-1}$; $\chi^2=\frac{(n-1)S^2}{\sigma_0^2}\sim\chi^2_{n-1}$; $Z=\frac{\hat p-p_0}{\sqrt{p_0(1-p_0)/n}}$; $F=S_1^2/S_2^2\sim F_{n_1-1,n_2-1}$; $T=\frac{\bar X_1-\bar X_2}{\sqrt{S_p^2(1/n_1+1/n_2)}}$ (hoặc Welch); $Z=\frac{\hat p_1-\hat p_2}{\sqrt{\bar p\bar q(1/n_1+1/n_2)}}$.

Giá trị giả thuyết dùng trong bài: $\mu_0=900$, $\sigma_0^2=0.1$, $p_0=0.5$.
Kiểm định so sánh hai kỳ vọng được chọn dạng t Welch theo kết quả kiểm định $F$ về hai phương sai.

## 3.2. Kết quả

| Kiểm định | H0 | H1 | Thống kê | Giá trị thống kê | Phân phối | P-giá trị |
|---|---|---|---|---|---|---|
| 1. Kỳ vọng Calories_Burned | μ = 900 | μ ≠ 900 | T | 0.6204 | t(972.0,) | 0.5352 |
| 2. Phương sai Session_Duration | σ² = 0.1 | σ² ≠ 0.1 | χ² | 1143.7715 | chi2(972.0,) | 0.0002 |
| 3. Tỷ lệ Gender = Male | p = 0.5 | p ≠ 0.5 | Z | 1.5709 | z | 0.1162 |
| 4. So sánh 2 phương sai Calories (Male/Female) | σ₁² = σ₂² | σ₁² ≠ σ₂² | F | 1.3182 | f(510.0, 461.0) | 0.0025 |
| 5a. So sánh 2 kỳ vọng Calories (t Welch) | μ₁ = μ₂ | μ₁ ≠ μ₂ | T | 4.7814 | t(969.67,) | 2.01e-06 |
| 5b. So sánh 2 kỳ vọng Calories (t Welch) | μ₁ = μ₂ | μ₁ > μ₂ | T | 4.7814 | t(969.67,) | 1.01e-06 |
| 6. So sánh 2 tỷ lệ Calories ≥ 1000 (Male/Female) | p₁ = p₂ | p₁ ≠ p₂ | Z | 4.3455 | z | 1.39e-05 |

### Kết luận theo từng kiểm định

- **1. Kỳ vọng Calories_Burned** — miền bác bỏ: T < -1.9624 hoặc T > 1.9624; P-giá trị = 0.5352; KTC (888.2700; 922.5748). Kết luận ở mức α = 0.05: **Không bác bỏ H0**.
- **2. Phương sai Session_Duration** — miền bác bỏ: χ² < 887.4932 hoặc χ² > 1060.2948; P-giá trị = 0.0002136; KTC (0.1079; 0.1289). Kết luận ở mức α = 0.05: **Bác bỏ H0**.
- **3. Tỷ lệ Gender = Male** — miền bác bỏ: Z < -1.9600 hoặc Z > 1.9600; P-giá trị = 0.1162; KTC (0.4938; 0.5566). Kết luận ở mức α = 0.05: **Không bác bỏ H0**.
- **4. So sánh 2 phương sai Calories (Male/Female)** — miền bác bỏ: F < 0.8370 hoặc F > 1.1957; P-giá trị = 0.002487; KTC (1.1024; 1.5749). Kết luận ở mức α = 0.05: **Bác bỏ H0**.
- **5a. So sánh 2 kỳ vọng Calories (t Welch)** — miền bác bỏ: T < -1.9624 hoặc T > 1.9624; P-giá trị = 2.01e-06; KTC (48.4674; 115.9467). Kết luận ở mức α = 0.05: **Bác bỏ H0**.
- **5b. So sánh 2 kỳ vọng Calories (t Welch)** — miền bác bỏ: T > 1.6464; P-giá trị = 1.005e-06; KTC (53.9001; inf). Kết luận ở mức α = 0.05: **Bác bỏ H0**.
- **6. So sánh 2 tỷ lệ Calories ≥ 1000 (Male/Female)** — miền bác bỏ: Z < -1.9600 hoặc Z > 1.9600; P-giá trị = 1.39e-05; KTC (0.0735; 0.1912). Kết luận ở mức α = 0.05: **Bác bỏ H0**.

## 3.3. Sai lầm loại I, loại II và lực kiểm định

- **Sai lầm loại I:** bác bỏ $H_0$ khi $H_0$ đúng, xác suất bằng $\alpha=0.05$.
- **Sai lầm loại II:** không bác bỏ $H_0$ khi $H_1$ đúng, xác suất $\beta$; lực kiểm định $1-\beta$.
- $\beta$ giảm khi tăng cỡ mẫu $n$, tăng $\alpha$ hoặc khi phương án đối lệch xa $H_0$.

Với kiểm định hai phía, xấp xỉ chuẩn: $1-\beta=\Phi(-z_{1-\alpha/2}+\lambda)+\Phi(-z_{1-\alpha/2}-\lambda)$ với $\lambda=d\sqrt n$ (một mẫu), $\lambda=d\sqrt{n_1n_2/(n_1+n_2)}$ (hai mẫu), $d$ là hiệu ứng chuẩn hóa.

| Kiểm định | Phương án đối cụ thể | α = P(sai lầm loại I) | β = P(sai lầm loại II) | Lực kiểm định 1−β |
|---|---|---|---|---|
| Kỳ vọng Calories (1 mẫu) | μ₁ = μ₀ + 0.1·s (hiệu ứng d=0.1) | 0.0500 | 0.1232 | 0.8768 |
| Kỳ vọng Calories (1 mẫu) | μ₁ = μ₀ + 0.2·s (hiệu ứng d=0.2) | 0.0500 | 9.40e-06 | 1.0000 |
| Kỳ vọng Calories (1 mẫu) | μ₁ = μ₀ + 0.5·s (hiệu ứng d=0.5) | 0.0500 | 0.0000 | 1.0000 |
| So sánh 2 kỳ vọng Male/Female | |μ₁−μ₂| = 0.1·s (d=0.1) | 0.0500 | 0.6560 | 0.3440 |
| So sánh 2 kỳ vọng Male/Female | |μ₁−μ₂| = 0.2·s (d=0.2) | 0.0500 | 0.1240 | 0.8760 |
| So sánh 2 kỳ vọng Male/Female | |μ₁−μ₂| = 0.5·s (d=0.5) | 0.0500 | 2.80e-09 | 1.0000 |
| Tỷ lệ Male (1 mẫu) | p₁ = p₀ + 0.03 | 0.0500 | 0.5352 | 0.4648 |
| Tỷ lệ Male (1 mẫu) | p₁ = p₀ + 0.05 | 0.0500 | 0.1220 | 0.8780 |
| Tỷ lệ Male (1 mẫu) | p₁ = p₀ + 0.1 | 0.0500 | 6.30e-06 | 1.0000 |
