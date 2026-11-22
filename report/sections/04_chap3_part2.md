# Chương 3 (Phần 2) — ANOVA 1 nhân tố & Kiểm định phi tham số

## A. ANOVA 1 nhân tố: Calories_Burned ~ Workout_Type

### Giả thiết

- $H_0$: $\mu_{Cardio} = \mu_{HIIT} = \mu_{Strength} = \mu_{Yoga}$
- $H_1$: Tồn tại ít nhất 2 kỳ vọng khác nhau

### Bảng ANOVA

| Nguồn | SS | df | MS | F |
|---|---|---|---|---|
| Nhân tố (SSF) | 211670.1103 | 3 | 70556.7034 | 0.9490 |
| Sai số (SSE) | 72040391.2812 | 969 | 74345.0890 |  |
| Tổng (SST) | 72252061.3916 | 972 |  |  |

- $F_{stat} = 0.9490$, $F_{critical} = 2.6141$, $P = 4.162395e-01$
- **Kết luận**: KHÔNG BÁC BỎ H₀

## B. Kiểm định Chi-bình phương phù hợp phân phối chuẩn

### Session_Duration

- $H_0$: Session_Duration $\sim N(\hat{\mu}, \hat{\sigma}^2)$
- $\chi^2 = 97.5213$, $df = 7$, $\chi^2_{crit} = 14.0671$, $P = 0.000000e+00$
- **Kết luận**: BÁC BỎ H₀

### Calories_Burned

- $H_0$: Calories_Burned $\sim N(\hat{\mu}, \hat{\sigma}^2)$
- $\chi^2 = 17.1432$, $df = 6$, $\chi^2_{crit} = 12.5916$, $P = 8.770972e-03$
- **Kết luận**: BÁC BỎ H₀

## C. Kiểm định Chi-bình phương tính độc lập: Gender × Experience_Level

- $H_0$: Gender và Experience_Level độc lập
- $H_1$: Gender và Experience_Level không độc lập

### Bảng chéo (Observed)

| Gender | 1 | 2 | 3 |
|---|---|---|---|
| Female | 179 | 193 | 90 |
| Male | 197 | 213 | 101 |

- $\chi^2 = 0.0128$, $df = 2$, $\chi^2_{crit} = 5.9915$, $P = 9.936014e-01$
- **Kết luận**: KHÔNG BÁC BỎ H₀

## Tổng hợp kết quả

| Kiểm định | Biến phân tích | Thống kê | df | Giá trị tới hạn | P-value | Kết luận |
|---|---|---|---|---|---|---|
| ANOVA 1 nhân tố | Calories_Burned ~ Workout_Type | F = 0.9490 | (3, 969) | F_crit = 2.6141 | 4.162395e-01 | KHÔNG BÁC BỎ H₀ |
| Chi² phù hợp chuẩn | Session_Duration ~ N(μ̂, σ̂²) | χ² = 97.5213 | 7 | χ²_crit = 14.0671 | 0.000000e+00 | BÁC BỎ H₀ |
| Chi² phù hợp chuẩn | Calories_Burned ~ N(μ̂, σ̂²) | χ² = 17.1432 | 6 | χ²_crit = 12.5916 | 8.770972e-03 | BÁC BỎ H₀ |
| Chi² tính độc lập | Gender × Experience_Level | χ² = 0.0128 | 2 | χ²_crit = 5.9915 | 9.936014e-01 | KHÔNG BÁC BỎ H₀ |
