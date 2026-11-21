# Chương 2. Ước lượng điểm và ước lượng khoảng

## 2.1. Ước lượng điểm

Với mẫu ngẫu nhiên $X_1,\dots,X_n$ từ $N(\mu,\sigma^2)$:

- Phương pháp mô-men (MoM): $\hat\mu=\bar X$, $\hat\sigma^2_{MoM}=\frac1n\sum(X_i-\bar X)^2$.
- Phương pháp hợp lý cực đại (MLE): cho cùng kết quả $\hat\mu=\bar X$, $\hat\sigma^2_{MLE}=\frac1n\sum(X_i-\bar X)^2$ (chệch); ước lượng không chệch là $S^2=\frac1{n-1}\sum(X_i-\bar X)^2$.
- Tỷ lệ (Bernoulli): MoM và MLE đều là $\hat p=\frac{\text{số quan sát thỏa}}{n}$.

| Tham số | MoM | MLE | Ước lượng hiệu chỉnh |
|---|---|---|---|
| μ (Calories_Burned) | 905.4224 | 905.4224 | 905.4224 |
| σ² (Calories_Burned) | 74257.0004 | 74257.0004 | 74333.3965 |
| μ (Session_Duration) | 1.2564 | 1.2564 | 1.2564 |
| σ² (Session_Duration) | 0.1176 | 0.1176 | 0.1177 |
| p (Gender = Male) | 0.5252 | 0.5252 | 0.5252 |

## 2.2. Khoảng tin cậy 95% (α = 0.05)

**Công thức và điều kiện áp dụng**

| Tham số | Khoảng tin cậy hai phía | Điều kiện |
|---|---|---|
| $\mu$ ($\sigma$ chưa biết) | $\bar X\pm t_{n-1;1-\alpha/2}\,S/\sqrt n$ | tổng thể chuẩn hoặc $n\ge30$ |
| $\sigma^2$ | $\left(\frac{(n-1)S^2}{\chi^2_{n-1;1-\alpha/2}},\frac{(n-1)S^2}{\chi^2_{n-1;\alpha/2}}\right)$ | tổng thể chuẩn |
| $p$ | $\hat p\pm z_{1-\alpha/2}\sqrt{\hat p(1-\hat p)/n}$ | $n\hat p\ge5$, $n(1-\hat p)\ge5$ |
| $\sigma_1^2/\sigma_2^2$ | $\left(\frac{S_1^2/S_2^2}{F_{n_1-1,n_2-1;1-\alpha/2}},\frac{S_1^2/S_2^2}{F_{n_1-1,n_2-1;\alpha/2}}\right)$ | 2 mẫu độc lập, chuẩn |
| $\mu_1-\mu_2$ ($\sigma_1^2=\sigma_2^2$) | $\bar X_1-\bar X_2\pm t_{n_1+n_2-2;1-\alpha/2}S_p\sqrt{1/n_1+1/n_2}$ | $S_p^2=\frac{(n_1-1)S_1^2+(n_2-1)S_2^2}{n_1+n_2-2}$ |
| $\mu_1-\mu_2$ ($\sigma_1^2\ne\sigma_2^2$) | $\bar X_1-\bar X_2\pm t_{\nu;1-\alpha/2}\sqrt{S_1^2/n_1+S_2^2/n_2}$ | $\nu$ theo Welch–Satterthwaite |
| $p_1-p_2$ | $\hat p_1-\hat p_2\pm z_{1-\alpha/2}\sqrt{\frac{\hat p_1\hat q_1}{n_1}+\frac{\hat p_2\hat q_2}{n_2}}$ | mỗi nhóm $n\hat p,n\hat q\ge5$ |

Khoảng một phía: thay $\alpha/2$ bằng $\alpha$ và chỉ lấy một cận.

**Kết quả (hai phía)**

| Chỉ tiêu | Tham số | Ước lượng điểm | Cận dưới | Cận trên | n |
|---|---|---|---|---|---|
| Kỳ vọng Calories_Burned | μ | 905.4224 | 888.2700 | 922.5748 | 973 |
| Phương sai Session_Duration | σ² | 0.1177 | 0.1079 | 0.1289 | 973 |
| Độ lệch chuẩn Session_Duration | σ | 0.3430 | 0.3284 | 0.3590 | 973 |
| Tỷ lệ Gender = Male | p | 0.5252 | 0.4938 | 0.5566 | 973 |
| Tỷ số phương sai Calories (Male/Female) | σ₁²/σ₂² | 1.3182 | 1.1024 | 1.5749 | 973 |
| Hiệu 2 kỳ vọng Calories (Male − Female) | μ₁−μ₂ | 82.2071 | 48.4674 | 115.9467 | 973 |
| Hiệu 2 kỳ vọng Calories (Male − Female) | μ₁−μ₂ | 82.2071 | 48.2331 | 116.1810 | 973 |
| Hiệu 2 tỷ lệ buổi tập Calories ≥ 1000 (Male − Female) | p₁−p₂ | 0.1324 | 0.0735 | 0.1912 | 973 |

**Kết quả (một phía)**

| Chỉ tiêu | Loại KTC | Cận dưới | Cận trên |
|---|---|---|---|
| Kỳ vọng Calories_Burned | Một phía (cận dưới) | 891.0319 | +∞ |
| Kỳ vọng Calories_Burned | Một phía (cận trên) | −∞ | 919.8129 |
| Phương sai Session_Duration | Một phía (cận dưới) | 0.1094 | +∞ |
| Phương sai Session_Duration | Một phía (cận trên) | 0.0000 | 0.1270 |
| Độ lệch chuẩn Session_Duration | Một phía (cận dưới) | 0.3307 | +∞ |
| Độ lệch chuẩn Session_Duration | Một phía (cận trên) | 0.0000 | 0.3564 |
| Tỷ lệ Gender = Male | Một phía (cận dưới) | 0.4988 | +∞ |
| Tỷ lệ Gender = Male | Một phía (cận trên) | −∞ | 0.5515 |
| Tỷ số phương sai Calories (Male/Female) | Một phía (cận dưới) | 1.1346 | +∞ |
| Tỷ số phương sai Calories (Male/Female) | Một phía (cận trên) | 0.0000 | 1.5305 |
| Hiệu 2 kỳ vọng Calories (Male − Female) | Một phía (cận dưới) | 53.9001 | +∞ |
| Hiệu 2 kỳ vọng Calories (Male − Female) | Một phía (cận trên) | −∞ | 110.5140 |
| Hiệu 2 tỷ lệ buổi tập Calories ≥ 1000 (Male − Female) | Một phía (cận dưới) | 0.0830 | +∞ |
| Hiệu 2 tỷ lệ buổi tập Calories ≥ 1000 (Male − Female) | Một phía (cận trên) | −∞ | 0.1817 |

**Chọn phương pháp so sánh 2 kỳ vọng.** Khoảng tin cậy 95% cho $\sigma_1^2/\sigma_2^2$ là (1.1024; 1.5749) nên
không chứa 1 → phương sai khác nhau, dùng t Welch.

## 2.3. Ý nghĩa mức tin cậy 95%

Mức tin cậy 95% **không** có nghĩa là "xác suất tham số nằm trong khoảng cụ thể vừa tính là 95%" (tham số là hằng số chưa biết, khoảng cụ thể hoặc chứa hoặc không chứa nó). Ý nghĩa theo **tần suất**: nếu lặp lại việc lấy mẫu cỡ $n$ và dựng khoảng bằng cùng một quy trình rất nhiều lần thì khoảng 95% các khoảng thu được sẽ chứa tham số thật.
