# Chương 4.1 — Hồi quy tuyến tính đơn (Mô hình & Suy luận)

## 1. Cơ sở lý thuyết & Mô hình toán học

### 1.1. Phương trình mô hình và Giả thiết 1

Mô hình Hồi quy tuyến tính đơn tổng thể:
$$Y = \beta_0 + \beta_1 X + \varepsilon$$

trong đó:
- $Y$: Biến phụ thuộc (`Calories_Burned`, lượng calo tiêu thụ, kcal).
- $X$: Biến độc lập (`Session_Duration`, thời lượng tập luyện, giờ).
- $\beta_0$: Hệ số chặn (intercept).
- $\beta_1$: Hệ số góc (slope) — độ dốc thể hiện mức thay đổi trung bình của $Y$ khi $X$ tăng 1 đơn vị.
- $\varepsilon$: Sai số ngẫu nhiên thỏa mãn **Giả thiết 1 (Gauss-Markov)**:
  1. $E(\varepsilon_i) = 0$ với mọi $i = 1, \ldots, n$.
  2. $Var(\varepsilon_i) = \sigma^2$ (phương sai thuần nhất, homoscedasticity).
  3. $Cov(\varepsilon_i, \varepsilon_j) = 0$ với mọi $i \neq j$ (sai số độc lập).
  4. $\varepsilon_i \sim N(0, \sigma^2)$ độc lập cùng phân phối.

### 1.2. Phương pháp ước lượng Bình phương nhỏ nhất (OLS - Định lý 1)

Cực tiểu hóa hàm mục tiêu:
$$L(\beta_0, \beta_1) = \sum_{i=1}^{n} (y_i - \beta_0 - \beta_1 x_i)^2$$

Nghiệm OLS:
$$\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}$$
$$\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$$

Theo Định lý Gauss-Markov, $\hat{\beta}_0$ và $\hat{\beta}_1$ là các **ước lượng tuyến tính không chệch tốt nhất (BLUE)**.

### 1.3. Phân phối xác suất của ước lượng và ước lượng phương sai sai số (Định lý 3 & 4)

- $\hat{\beta}_1 \sim N\left(\beta_1, \frac{\sigma^2}{S_{xx}}\right)$, suy ra $se(\hat{\beta}_1) = \frac{s}{\sqrt{S_{xx}}}$.
- $\hat{\beta}_0 \sim N\left(\beta_0, \sigma^2 \left[\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}\right]\right)$, suy ra $se(\hat{\beta}_0) = s \sqrt{\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}}$.
- Ước lượng không chệch cho $\sigma^2$:
  $$s^2 = MSE = \frac{SSE}{n - 2} = \frac{S_{yy} - \hat{\beta}_1 S_{xy}}{n - 2}$$
  và $\frac{(n-2)s^2}{\sigma^2} \sim \chi^2(n - 2)$, độc lập với $\hat{\beta}_0, \hat{\beta}_1$.

## 2. Kết quả ước lượng mô hình thực nghiệm

- **Phương trình hồi quy OLS**:
$$\widehat{\text{Calories\_Burned}} = -1.4465 + 721.7860 \times \text{Session\_Duration}$$
- Hệ số chặn: $\hat{\beta}_0 = -1.4465$ (se = 13.9074)
- Hệ số góc: $\hat{\beta}_1 = 721.7860$ (se = 10.6786)
- Hệ số xác định: $R^2 = 0.8247$ (82.47%)
- Hệ số tương quan: $r = 0.9081$ (tương quan tuyến tính đồng biến rất mạnh)
- Độ lệch chuẩn phần dư: $s = 114.2044$ kcal

### Bảng tổng hợp các chỉ số mô hình

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| Cỡ mẫu (n) | 973 | Số quan sát thành viên phòng gym |
| Hệ số chặn (β̂₀) | -1.4465 | se = 13.9074, KTC 95%: [-28.74, 25.85] |
| Hệ số góc (β̂₁) | 721.7860 | se = 10.6786, KTC 95%: [700.83, 742.74] |
| Hệ số xác định (R²) | 0.8247 | 82.47% biến thiên calo giải thích bởi thời lượng tập |
| Hệ số tương quan (r) | 0.9081 | Tương quan tuyến tính đồng biến rất mạnh |
| Độ lệch chuẩn phần dư (s) | 114.2044 | Độ biến thiên không được giải thích bởi mô hình |
| Thống kê t (t₀) | 67.5920 | t_crit = 1.9624, P < 10⁻¹⁵ (Bác bỏ H₀) |
| Thống kê F (F₀) | 4568.6744 | F_crit = 3.8511, P < 10⁻¹⁵ (F₀ = t₀²) |

## 3. Phân tích phương sai hồi quy (ANOVA) & Kiểm định giả thuyết

### 3.1. Bảng ANOVA hồi quy (Định lý 6)

| Nguồn biến thiên | SS | df | MS | F₀ | P-value |
|---|---|---|---|---|---|
| Hồi quy (SSR) | 59587643.6038 | 1 | 59587643.6038 | 4568.6744 | 0.0000 |
| Sai số (SSE) | 12664417.7878 | 971 | 13042.6548 |  |  |
| Tổng cộng (SST) | 72252061.3916 | 972 |  |  |  |

- $F_0 = 4568.6744 > F_{0.05; 1, 971} = 3.8511$
- $P\text{-value} = 0.000000e+00 < 0.05$ $\rightarrow$ **Bác bỏ $H_0$**.

### 3.2. Kiểm định t cho hệ số góc (Định lý 5) và Tính tương đương $t_0^2 = f_0$

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

## 4. Khoảng tin cậy & Khoảng dự đoán (Định lý 7 & 8)

### 4.1. Khoảng tin cậy 95% cho các tham số

- **Hệ số góc $\beta_1$**: [700.8303, 742.7418] kcal/giờ.
- **Hệ số chặn $\beta_0$**: [-28.7385, 25.8455] kcal.

### 4.2. So sánh Dải Khoảng tin cậy cho $E[Y|x_0]$ và Dải Dự đoán cho cá thể $y_0$
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

### 4.3. Bảng giá trị KTC và Khoảng dự đoán tại các mốc thời lượng tập tiêu biểu

| x0 (giờ) | ŷ₀ (dự báo) | se(Mean) | KTC 95% (Kỳ vọng E[Y]) | Độ rộng KTC | se(Pred) | Khoảng dự đoán 95% (Cá thể y₀) | Độ rộng KDĐ |
|---|---|---|---|---|---|---|---|
| 0.50 | 359.45 | 8.87 | [342.04, 376.85] | 34.81 | 114.55 | [134.66, 584.24] | 449.58 |
| 0.75 | 539.89 | 6.53 | [527.08, 552.71] | 25.63 | 114.39 | [315.41, 764.38] | 448.96 |
| 1.00 | 720.34 | 4.57 | [711.37, 729.31] | 17.94 | 114.30 | [496.04, 944.64] | 448.59 |
| 1.25 | 900.79 | 3.66 | [893.60, 907.97] | 14.37 | 114.26 | [676.55, 1125.02] | 448.46 |
| 1.50 | 1081.23 | 4.49 | [1072.42, 1090.05] | 17.63 | 114.29 | [856.94, 1305.52] | 448.58 |
| 1.75 | 1261.68 | 6.42 | [1249.09, 1274.27] | 25.19 | 114.38 | [1037.21, 1486.15] | 448.94 |
| 2.00 | 1442.13 | 8.74 | [1424.97, 1459.28] | 34.32 | 114.54 | [1217.35, 1666.90] | 449.54 |

## 5. Ý nghĩa thực tế của hệ số chặn $\hat{\beta}_0$

- **Về mặt thực tế**: Trong bộ dữ liệu, thời lượng buổi tập quan sát dao động từ $0.5$ đến $2.0$ giờ. Không có cá thể nào tập $0$ giờ. Việc diễn giải máy móc "tập 0 giờ tiêu thụ $-1.45$ calo" là phép ngoại suy không có căn cứ (Extrapolation) và không có ý nghĩa thực tế.
- **Về mặt toán học**: $\hat{\beta}_0$ đóng vai trò "mỏ neo" bắt buộc để:
  1. Đảm bảo tổng phần dư $\sum_{i=1}^n e_i = 0$.
  2. Đảm bảo đường hồi quy luôn đi qua điểm trọng tâm mẫu $(\bar{x}, \bar{y})$.
  3. Bảo toàn phân rã phương sai $SST = SSR + SSE$ và định nghĩa hệ số xác định $R^2 = SSR / SST$.
Nếu ép $\beta_0 = 0$ (mô hình qua gốc tọa độ), ước lượng $\hat{\beta}_1$ sẽ bị chệch nghiêm trọng và các công thức phân tích phương sai thông thường không còn hợp lệ.

## 6. Đồ thị hồi quy thực nghiệm
Đồ thị thể hiện dữ liệu quan sát, đường hồi quy OLS, dải tin cậy 95% và dải dự đoán 95% được lưu tại:
`outputs/figures/05_slr_bands.png`
