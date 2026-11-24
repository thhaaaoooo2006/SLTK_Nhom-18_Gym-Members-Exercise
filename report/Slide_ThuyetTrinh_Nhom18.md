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

## Slide 2: Mục tiêu nghiên cứu và Tổng quan dữ liệu (Người trình bày: Thảo)
- **Mục tiêu nghiên cứu**:
  - Áp dụng hệ thống lý thuyết ước lượng, kiểm định giả thuyết tham số và phi tham số, ANOVA và hồi quy tuyến tính.
  - Phân tích mối quan hệ giữa lượng calo tiêu thụ (`Calories_Burned`) với thời lượng buổi tập (`Session_Duration`), loại hình bài tập (`Workout_Type`) và giới tính (`Gender`).
- **Tổng quan bộ dữ liệu**:
  - Quy mô: $n = 973$ thành viên phòng gym, theo dõi 15 biến (12 biến định lượng, 3 biến định tính).
  - Chất lượng dữ liệu: Đạt độ toàn vẹn 100% (0 giá trị khuyết, 0 bản ghi trùng).

---

## Slide 3: Chương 1 - Mẫu ngẫu nhiên và các đặc trưng mẫu (Người trình bày: Thảo)
- **Mẫu ngẫu nhiên**: $W_X = (X_1, X_2, \dots, X_n)$ kích thước $n$ lập từ biến ngẫu nhiên gốc $X$, gồm $n$ biến ngẫu nhiên độc lập có cùng phân phối xác suất với $X$. Mẫu cụ thể (thể hiện): $W_x = (x_1, x_2, \dots, x_n)$.
- **Trung bình mẫu**: $\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$, $E(\bar{X}) = \mu, V(\bar{X}) = \frac{\sigma^2}{n}$. Giá trị quan sát: $\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$.
- **Phương sai mẫu và Phương sai mẫu hiệu chỉnh**:
  - Phương sai mẫu: $\widetilde{S}^2 = \frac{1}{n} \sum_{i=1}^n (X_i - \bar{X})^2$, $E(\widetilde{S}^2) = \frac{n-1}{n}\sigma^2$.
  - Phương sai mẫu hiệu chỉnh: $S^2 = \frac{n}{n-1}\widetilde{S}^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar{X})^2$, $E(S^2) = \sigma^2$ (ước lượng không chệch cho $\sigma^2$). Giá trị quan sát: $s^2 = \frac{1}{n-1}\sum_{i=1}^n (x_i - \bar{x})^2$.
- **Tần suất mẫu**: $\widehat{P} = \frac{Y}{n}$ ($Y$ là số lần xuất hiện biến cố trong $n$ phép thử), $E(\widehat{P}) = p, V(\widehat{P}) = \frac{p(1-p)}{n}$. Giá trị quan sát: $\hat{p} = \frac{y}{n}$.
- **Phân phối mẫu khi $X \sim \mathcal{N}(\mu, \sigma^2)$**:
  - $U = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim \mathcal{N}(0, 1)$ (khi $\sigma^2$ đã biết).
  - $T = \frac{\bar{X} - \mu}{S/\sqrt{n}} \sim \mathcal{T}(n-1)$ (khi $\sigma^2$ chưa biết).
  - $\frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$.

---

## Slide 4: Bảng Thống kê Mô tả Thực nghiệm (Người trình bày: Thảo)
| Biến số | Trung bình ($\bar{x}$) | Độ lệch chuẩn ($s$) | Trung vị | Min | Max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Calories_Burned` (kcal) | 905.42 | 272.64 | 893.00 | 285.00 | 1650.00 |
| `Session_Duration` (giờ) | 1.256 | 0.343 | 1.25 | 0.50 | 2.00 |
| `Avg_BPM` (nhịp/phút) | 143.44 | 15.23 | 143.00 | 120.00 | 170.00 |
| `Weight` (kg) | 73.09 | 15.00 | 72.80 | 40.00 | 115.00 |
- Tỷ lệ giới tính: Nam chiếm 52.52% ($y = 511$, $\hat{p} = 52.52\%$).
- Loại bài tập: Cardio ($y = 251$, $\hat{p} = 25.80\%$), HIIT ($y = 247$, $\hat{p} = 25.39\%$), Strength (24.77%), Yoga (24.05%).
*(Các đại lượng được tính trên mẫu cụ thể theo đúng công thức đặc trưng mẫu lý thuyết)*

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

## Slide 7: Chương 3 - ANOVA một nhân tố và kiểm định phi tham số (Người trình bày: Thảo)
- **Phân tích phương sai một nhân tố (ANOVA)**:
  - Cặp giả thuyết: $H_0: \mu_1 = \mu_2 = \mu_3 = \mu_4$ đối với $H_1$: Tồn tại ít nhất 2 kỳ vọng khác nhau ($k = 4$ mức loại bài tập; $n = 973$).
  - Bảng phân tích phương sai:
    - Do nhân tố: $SSF = 1,481,280.95$ (bậc tự do $k-1 = 3$), $MSF = SSF/3 = 493,760.32$.
    - Sai số: $SSE = 70,770,775.14$ (bậc tự do $n-k = 969$), $MSE = SSE/969 = 73,034.86$.
    - Tổng biến thiên: $SST = SSF + SSE = 72,252,056.09$ (bậc tự do $n-1 = 972$).
  - Tiêu chuẩn kiểm định: $F_0 = \frac{MSF}{MSE}$, giá trị quan sát $f_0 = 6.7644$.
  - Miền bác bỏ: $W_\alpha = (f_{\alpha; k-1; n-k}; +\infty) = (f_{0.05; 3; 969}; +\infty) = (2.6141; +\infty)$.
  - Vì $f_0 = 6.7644 \in W_\alpha$ ($P = 0.00016 < 0.05$) $\rightarrow$ **Bác bỏ $H_0$**: Loại bài tập có tác động thực sự đến lượng calo tiêu thụ.
- **Kiểm định phi tham số Khi-bình phương**:
  - *Kiểm định giả thuyết về phân phối của biến ngẫu nhiên*:
    - Tiêu chuẩn kiểm định: $\chi^2 = \sum_{i=1}^k \frac{(n_i - n P_i)^2}{n P_i}$.
    - `Session_Duration`: Giá trị quan sát $\chi_0^2 = 2.4578, P = 0.9303 > 0.05$.
    - `Calories_Burned`: Giá trị quan sát $\chi_0^2 = 5.2140, P = 0.6338 > 0.05$.
    - $\rightarrow$ Chưa có cơ sở bác bỏ $H_0$: Cả hai đều phù hợp rất tốt với phân phối chuẩn!
  - *Kiểm định tính độc lập giữa hai dấu hiệu định tính*:
    - Cặp giả thuyết: $H_0$: `Gender` và `Experience_Level` độc lập.
    - Bảng tiếp biến $h \times k = 2 \times 3$, bậc tự do $(h-1)(k-1) = 2$.
    - Tiêu chuẩn: $\chi^2 = n\left(\sum_{i=1}^h \sum_{j=1}^k \frac{n_{ij}^2}{n_i m_j} - 1\right)$.
    - Miền bác bỏ: $W_{0.05} = (\chi^2_{0.05; 2}; +\infty) = (5.9915; +\infty)$.
    - Giá trị quan sát: $\chi_0^2 = 0.0128 \notin W_{0.05}$ ($P = 0.9936$). Chưa có cơ sở bác bỏ $H_0$: Giới tính và cấp độ kinh nghiệm độc lập nhau.

---

## Slide 8: Chương 4.1 - Hồi quy Tuyến tính Đơn và Phương pháp Bình phương Nhỏ nhất (Người trình bày: Thảo)
- **Mô hình hồi quy tuyến tính đơn biến**: $Y = \beta_0 + \beta_1 x + \varepsilon$, trong đó sai số ngẫu nhiên $\varepsilon \sim \mathcal{N}(0, \sigma^2)$.
- **Hàm hồi quy mẫu (thực nghiệm)**: $\hat{y} = -1.4465 + 721.7860 \cdot x$
  - Hệ số góc $\hat{\beta}_1 = 721.79$: Mỗi giờ tập tăng thêm làm tăng trung bình $721.8$ kcal đốt cháy ($P < 10^{-15}$).
  - Hệ số xác định $R^2 = 0.8247$: $82.47\%$ biến thiên lượng calo được giải thích bởi thời lượng tập.
- **Kiểm định hệ số góc và mối liên hệ tương đương $t_0^2 = f_0$**:
  - Tiêu chuẩn $T_0 = \frac{B_1 - 0}{S/\sqrt{S_{xx}}}$ và Tiêu chuẩn $F_0 = \frac{MSR}{MSE}$:
  $$t_0^2 = \left(\frac{\hat{\beta}_1}{s/\sqrt{S_{xx}}}\right)^2 = \frac{\hat{\beta}_1^2 S_{xx}}{s^2} = \frac{SSR / 1}{SSE / (n-2)} = \frac{MSR}{MSE} = f_0$$
  - Thực nghiệm: $t_0^2 = 67.5920^2 = 4568.6744 = f_0 \in W_{0.05}$. Hai kiểm định tương đương hoàn toàn!
- **Đồ thị minh họa**: Đường hồi quy mẫu, khoảng tin cậy 95% cho phản hồi trung bình $\mu_{Y|x_0}$ và khoảng dự đoán 95% cho quan sát mới $y_0$.

---

## Slide 9: Khoảng tin cậy, khoảng dự đoán và ý nghĩa hệ số chặn (Người trình bày: Thảo)
- **Khoảng tin cậy và khoảng dự đoán**:
  - Khoảng tin cậy cho phản hồi trung bình $\mu_{Y|x_0}$ (Định lý 7):
    $$\hat{y}_0 \pm t_{\alpha/2, n-2} \cdot s \sqrt{\frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$
  - Khoảng dự đoán cho một quan sát tương lai $y_0$ tại $x_0$ (Định lý 8):
    $$\hat{y}_0 \pm t_{\alpha/2, n-2} \cdot s \sqrt{\mathbf{1} + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$
  - *Giải thích độ rộng*: Biến ngẫu nhiên $\widehat{Y}_0 - Y_0$ có kỳ vọng 0 và phương sai:
    $$\sigma^2_{\widehat{Y}_0 - Y_0} = \sigma^2 \left[1 + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}\right]$$
    Khoảng dự đoán luôn rộng hơn do chứa thêm số hạng 1 phản ánh phương sai của sai số ngẫu nhiên $\varepsilon_0$ của chính quan sát tương lai ($\sigma^2_{\varepsilon_0} = \sigma^2$).
- **Ý nghĩa của hệ số chặn $\hat{\beta}_0 = -1.45$**:
  - *Về thực tế*: Hệ số chặn chỉ có ý nghĩa khi biến độc lập nhận giá trị 0. Do thời lượng tập trong mẫu $x \in [0.5, 2.0]$ giờ (không ai tập 0 giờ), việc ngoại suy tại $x=0$ không mang ý nghĩa thực tế.
  - *Về vai trò kỹ thuật trong mô hình*:
    1. Giúp xác định đúng bản chất mối quan hệ (tránh áp đặt đi qua gốc tọa độ).
    2. Đảm bảo tổng phần dư $\sum e_i = 0$ và đường hồi quy đi qua $(\bar{x}, \bar{y})$.
    3. Đảm bảo ý nghĩa của hệ số xác định $R^2$ và phân rã $SST = SSR + SSE$.

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
