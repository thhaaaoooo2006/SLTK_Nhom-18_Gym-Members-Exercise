# BỘ SLIDE THUYẾT TRÌNH BÀI TẬP LỚN SUY LUẬN THỐNG KÊ (MI3031) - NHÓM 18
**Đề tài**: Nghiên cứu và Suy diễn thống kê trên dữ liệu tập luyện Gym (*Gym Members Exercise Tracking*)  
**Thành viên thực hiện**:  
- **Nguyễn Thị Thảo** (MSSV: 202419101)  
- **Nguyễn Văn Nam Khánh** (MSSV: 202419069)  
**Đơn vị**: Viện Toán ứng dụng và Tin học (SAMI), Đại học Bách khoa Hà Nội  

---

## Slide 1: Bìa thuyết trình
- **Tiêu đề**: BÁO CÁO BÀI TẬP LỚN MÔN SUY LUẬN THỐNG KÊ (MI3031)
- **Tên đề tài**: Phân tích Suy luận Thống kê trên bộ dữ liệu Gym Members Exercise Tracking
- **Nhóm sinh viên thực hiện**: Nhóm 18 (Nguyễn Thị Thảo & Nguyễn Văn Nam Khánh)
- **Học kỳ**: 2026.1 — Trường Công nghệ Thông tin & Truyền thông / Viện SAMI - ĐHBK Hà Nội

---

## Slide 2: Mục tiêu nghiên cứu & Tổng quan dữ liệu (Người trình bày: Thảo)
- **Mục tiêu nghiên cứu**:
  - Áp dụng hệ thống lý thuyết ước lượng, kiểm định giả thuyết tham số & phi tham số, ANOVA và hồi quy tuyến tính.
  - Phân tích mối quan hệ giữa lượng calo tiêu thụ (`Calories_Burned`) với thời lượng buổi tập (`Session_Duration`), loại hình bài tập (`Workout_Type`) và giới tính (`Gender`).
- **Tổng quan bộ dữ liệu**:
  - Quy mô: $n = 973$ thành viên phòng gym, theo dõi 15 biến (12 biến định lượng, 3 biến định tính).
  - Chất lượng dữ liệu: Đạt độ toàn vẹn 100% (0 missing values, 0 duplicate rows).

---

## Slide 3: Chương 1 - Cơ sở toán học Mẫu ngẫu nhiên (Người trình bày: Thảo)
- **Mẫu ngẫu nhiên (Random Sample)**: $(X_1, X_2, \dots, X_n)$ là các biến ngẫu nhiên độc lập cùng phân phối ($iid$) theo $F(x)$ của tổng thể.
- **Trung bình mẫu**: $\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$ là ước lượng không chệch, vững cho $\mu$.
- **Phương sai mẫu hiệu chỉnh**:
  $$S^2 = \frac{1}{n - 1} \sum_{i=1}^n (X_i - \bar{X})^2$$
  *Điều kiện bắt buộc*: Chia cho bậc tự do $n - 1$ thay vì $n$ để $E(S^2) = \sigma^2$ (loại bỏ độ chệch).
- **Tần suất mẫu**: $\hat{p} = \frac{k}{n}$, ước lượng không chệch cho tỷ lệ tổng thể $p$.
- **Kiểm định ngoại lai**: Áp dụng hàng rào IQR Tukey $[Q_1 - 1.5 IQR, Q_3 + 1.5 IQR]$, giữ nguyên toàn bộ 973 mẫu vì phản ánh thể lực thực tế của vận động viên.

---

## Slide 4: Bảng Thống kê Mô tả Thực nghiệm (Người trình bày: Thảo)
| Biến số | Trung bình ($\bar{x}$) | Độ lệch chuẩn ($S$) | Trung vị | Min | Max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Calories_Burned` (kcal) | 905.42 | 272.64 | 893.00 | 285.00 | 1650.00 |
| `Session_Duration` (giờ) | 1.256 | 0.343 | 1.25 | 0.50 | 2.00 |
| `Avg_BPM` (nhịp/phút) | 143.44 | 15.23 | 143.00 | 120.00 | 170.00 |
| `Weight` (kg) | 73.09 | 15.00 | 72.80 | 40.00 | 115.00 |
- Tỷ lệ giới tính: Nam chiếm 52.52% ($k = 511$), Nữ chiếm 47.48% ($k = 462$).
- Loại bài tập phân bổ đều: Cardio (25.80%), HIIT (25.39%), Strength (24.77%), Yoga (24.05%).
*(Toàn bộ các chỉ số được tính bằng mã nguồn tự cài đặt trong `src/stats_utils.py`)*

---

## Slide 5: Chương 2 - Ước lượng Điểm & Khoảng tin cậy 95% (Người trình bày: Khánh)
- **Phương pháp ước lượng điểm**:
  - MoM & MLE cho $\mu$: $\hat{\mu} = \bar{X} = 905.42$ kcal.
  - MLE cho $\sigma^2$: $\hat{\sigma}^2_{MLE} = \frac{1}{n}\sum (X_i - \bar{X})^2$ (chệch dưới). Nhân $\frac{n}{n-1}$ cho ra $S^2 = 0.1177$ không chệch.
- **Diễn giải tần suất 95%**: Lặp lại lấy mẫu ngẫu nhiên độc lập 973 thành viên một số lượng vô hạn lần thì 95% các khoảng tin cậy tính được sẽ bao trùm tham số thực của tổng thể.
- **Kết quả KTC 95% hai phía tiêu biểu**:
  - Kỳ vọng $\mu$ Calo: $[888.27, 922.57]$ ($t$-Student, $df = 972$).
  - Phương sai $\sigma^2$ Thời lượng: $[0.1079, 0.1289]$ ($\chi^2, df = 972$).
  - Hiệu 2 kỳ vọng Nam - Nữ: $[48.47, 115.95]$ ($t$-Welch do $\sigma_1^2 \neq \sigma_2^2$).
  - Hiệu 2 tỷ lệ đốt Calo $\ge 1000$: $[0.0735, 0.1912]$ (Nam vượt trội Nữ).

---

## Slide 6: Chương 3 - Kiểm định Tham số & 3 Cách Tiếp cận (Người trình bày: Khánh)
- **Quy trình 5 bước kiểm định**: Thiết lập $H_0/H_1$ $\rightarrow$ Chọn $\alpha = 0.05$ $\rightarrow$ Thống kê $T$ $\rightarrow$ Tính $t_{obs}$ & $P$-value $\rightarrow$ Kết luận.
- **3 Cách tiếp cận nhất quán tuyệt đối**:
  1. *Miền bác bỏ cổ điển*: $t_{obs} \in W_\alpha$.
  2. *$P$-value*: $P \le \alpha$.
  3. *Đối chiếu KTC*: Giá trị $\theta_0$ nằm ngoài KTC 95% tương ứng.
- **Bảng tổng hợp kết luận kiểm định ($\alpha = 0.05$)**:
  - $H_0: \mu = 900$: Không bác bỏ $H_0$ ($P = 0.5352$).
  - $H_0: \sigma^2 = 0.10$: Bác bỏ $H_0$ ($P = 0.0002$).
  - $H_0: p = 0.50$ (Nam): Không bác bỏ $H_0$ ($P = 0.1162$).
  - $H_0: \sigma_1^2 = \sigma_2^2$: Bác bỏ $H_0$ ($P = 0.0025 \rightarrow$ dùng $t$-Welch).
  - $H_0: \mu_1 = \mu_2$: Bác bỏ $H_0$ ($P = 2.01 \times 10^{-6} \rightarrow$ Nam đốt calo cao hơn Nữ).

---

## Slide 7: Chương 3 - ANOVA 1 Nhân tố & Kiểm định Phi tham số (Người trình bày: Thảo)
- **ANOVA 1 nhân tố so sánh Calories theo Workout\_Type**:
  - $H_0: \mu_{\text{Cardio}} = \mu_{\text{HIIT}} = \mu_{\text{Strength}} = \mu_{\text{Yoga}}$.
  - Phân tích phương sai: $SSF = 1,481,280.95$ ($df=3$), $SSE = 70,770,775.14$ ($df=969$).
  - Thống kê $F = 6.7644 > F_{0.05; 3, 969} = 2.6141$ ($P = 0.00016$).
  - $\rightarrow$ **Bác bỏ $H_0$**: Loại bài tập có tác động thực sự đến lượng calo tiêu thụ (Cardio và HIIT dẫn đầu).
- **Kiểm định phi tham số Chi-bình phương**:
  - *Kiểm định phù hợp phân phối chuẩn*: `Session_Duration` ($\chi^2 = 2.4578, P = 0.9303$), `Calories_Burned` ($\chi^2 = 5.2140, P = 0.6338$). Cả hai đều phù hợp rất tốt với phân phối chuẩn!
  - *Kiểm định độc lập*: `Gender` và `Experience_Level` ($\chi^2 = 0.0128, P = 0.9936$). Không bác bỏ $H_0$: Giới tính và Cấp độ kinh nghiệm hoàn toàn độc lập.

---

## Slide 8: Chương 4.1 - Hồi quy Tuyến tính Đơn OLS (Người trình bày: Thảo)
- **Phương trình OLS**: $\hat{y} = -1.4465 + 721.7860 \cdot x$
  - Hệ số góc $\hat{\beta}_1 = 721.79$: Mỗi giờ tập thêm làm tăng trung bình $721.8$ kcal đốt cháy ($P < 10^{-15}$).
  - Hệ số xác định $R^2 = 0.8247$: $82.47\%$ biến thiên lượng calo được giải thích tuyến tính bởi thời lượng tập.
- **Chứng minh tính tương đương cốt lõi $t_0^2 = f_0$**:
  $$t_0^2 = \left(\frac{\hat{\beta}_1}{s/\sqrt{S_{xx}}}\right)^2 = \frac{\hat{\beta}_1^2 S_{xx}}{s^2} = \frac{SSR}{MSE} = f_0$$
  Thực nghiệm: $t_0^2 = 67.5920^2 = 4568.6744 = f_0$. Kiểm định $t$ và $F$ cho hệ số góc là tương đương hoàn toàn!
- **Đồ thị minh họa**: Đường OLS, Dải tin cậy 95% cho $E(Y|x_0)$ và Dải dự đoán 95% cho quan sát mới $y_0$.

---

## Slide 9: So sánh KTC vs Khoảng Dự đoán & Ý nghĩa Hệ số chặn (Người trình bày: Thảo)
- **Tại sao Khoảng Dự đoán luôn rộng hơn Khoảng Tin cậy?**
  - KTC cho $E(Y|x_0)$: $\hat{y}_0 \pm t \cdot s \sqrt{\frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$
  - KTD cho quan sát mới $y_0$: $\hat{y}_0 \pm t \cdot s \sqrt{\mathbf{1} + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$
  - Số hạng **`+1`** bên trong dấu căn phản ánh độ bất định tự nhiên của chính cá thể mới: $Var(y_0 - \hat{y}_0) = Var(\hat{y}_0) + \sigma^2$.
- **Ý nghĩa thực tế và toán học của hệ số chặn $\hat{\beta}_0 = -1.45$**:
  - *Về thực tế*: Không ai tập 0 giờ ($x \in [0.5, 2.0]$). Ngoại suy $x=0$ là vô nghĩa.
  - *Về toán học*: $\hat{\beta}_0$ là mỏ neo bắt buộc để $\sum e_i = 0$, đường hồi quy qua trọng tâm mẫu $(\bar{x}, \bar{y})$ và bảo toàn phân rã $SST = SSR + SSE$.

---

## Slide 10: Chương 4.2 - Phần dư & Tương quan Tuyến tính (Người trình bày: Khánh)
- **Chẩn đoán phần dư**:
  - $E(e_i) \approx 0$, Skewness = $-0.02$, Kurtosis = $0.05$.
  - Biểu đồ Residuals vs Fitted cho thấy dải băng thuần nhất (Homoscedasticity).
  - Normal Q-Q plot bám sát đường chuẩn 45°.
- **Hệ số tương quan Pearson $r = 0.9081$**:
  - Kiểm định $H_0: \rho = 0$: $t_0 = 67.592$ ($P < 10^{-15} \rightarrow$ Bác bỏ).
  - Biến đổi Fisher $Z = \text{arctanh}(r) = 1.5167$. Kiểm định $H_0: \rho = 0.85$: $Z_0 = 8.1633$ ($P < 10^{-15} \rightarrow$ Bác bỏ).
  - Khoảng tin cậy 95% cho $\rho$: $[0.8965, 0.9185]$.

---

## Slide 11: Vấn đáp Trọng tâm: Tương quan vs Nhân quả (Người trình bày: Cả hai)
- **Nguyên lý vàng**: *Tương quan không đồng nghĩa với Nhân quả (Correlation does NOT imply Causation)*.
- Thời lượng tập không phải nguyên nhân duy nhất quyết định lượng calo đốt cháy.
- **Các biến giấu mặt (Confounding Variables) cùng chi phối**:
  1. *Cường độ tim mạch (`Avg_BPM`, `Max_BPM`)*: Cùng 1 giờ tập, người nhịp tim 160 BPM đốt calo gấp 1.5 lần người nhịp tim 110 BPM.
  2. *Khối lượng cơ thể (`Weight`)*: Người nặng cân hơn tốn nhiều công cơ học hơn.
  3. *Loại bài tập (`Workout_Type`)*: HIIT đốt calo mỗi phút cao hơn Yoga.
- **Giải pháp**: Bắt buộc mở rộng sang mô hình **Hồi quy tuyến tính bội (Multiple Regression)** để kiểm soát đồng thời các biến can thiệp.

---

## Slide 12: Tổng kết Nghiệm thu Dự án & Q&A
- **Sản phẩm bài tập lớn hoàn thành**:
  - `main.py`: Chạy tự động toàn bộ 6 mô-đun và kiểm tra chéo trong 25 giây.
  - Toàn văn báo cáo khoa học PDF: `report/BaoCao_SLTK_Nhom18.pdf` (2.4 MB).
  - Slide thuyết trình Beamer PDF: `report/Slide_ThuyetTrinh_Nhom18.pdf` (2.3 MB).
  - GitHub Repository hoàn chỉnh, chuẩn mực.
- **Lời cảm ơn**: Cảm ơn Thầy Cô và các bạn đã theo dõi bài báo cáo của Nhóm 18!
