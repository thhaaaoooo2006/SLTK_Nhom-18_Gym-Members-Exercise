# BỘ SLIDE THUYẾT TRÌNH BÀI TẬP LỚN SUY LUẬN THỐNG KÊ (MI3031) - NHÓM 18
**Đề tài**: Suy luận thống kê trên dữ liệu tập luyện gym  
**Sinh viên thực hiện**:  
- **Nguyễn Văn Nam Khánh** - 202419069  
- **Nguyễn Thị Thảo** - 202419101  
**Đơn vị**: Đại học Bách khoa Hà Nội  

---

## Slide 1: Bìa thuyết trình
- **Tên đề tài**: SUY LUẬN THỐNG KÊ TRÊN DỮ LIỆU TẬP LUYỆN GYM
- **Sinh viên thực hiện**:
  - Nguyễn Văn Nam Khánh - 202419069
  - Nguyễn Thị Thảo - 202419101
- **Đơn vị**: Đại học Bách khoa Hà Nội
- **Thời gian**: Tháng 11 Năm 2026

---

## 1. Tổng quan đề tài và bộ dữ liệu
- **Mục tiêu nghiên cứu**:
  - Phân tích các yếu tố ảnh hưởng đến lượng calo tiêu thụ (`Calories_Burned`).
  - Đánh giá tác động của thời lượng tập (`Session_Duration`), loại bài tập (`Workout_Type`) và giới tính (`Gender`).
- **Tổng quan bộ dữ liệu Gym Members Exercise**:
  - Quy mô mẫu: $n = 973$ thành viên phòng gym.
  - Gồm 15 biến (12 biến định lượng, 3 biến định tính).
  - Độ toàn vẹn dữ liệu: 100% sạch (0 giá trị khuyết, 0 bản ghi trùng).
- **Phân loại biến trọng tâm**:
  - Biến phụ thuộc ($Y$): `Calories_Burned` (kcal).
  - Biến độc lập ($x$): `Session_Duration` (giờ).
  - Biến phân loại: `Gender`, `Workout_Type`, `Experience_Level`.
  - Biến sinh lý: `Avg_BPM`, `Max_BPM`, `Weight`, `BMI`.

---

## 2. Chương 1: mẫu ngẫu nhiên và cơ sở toán học
- **Cơ sở lý thuyết mẫu ngẫu nhiên và thống kê mẫu**:
  - **Mẫu ngẫu nhiên**: $W_X = (X_1, X_2, \dots, X_n)$ kích thước $n$ gồm các biến ngẫu nhiên độc lập có cùng phân phối xác suất với biến ngẫu nhiên gốc $X$. Mẫu cụ thể (thể hiện): $W_x = (x_1, x_2, \dots, x_n)$.
  - **Trung bình mẫu**: $\overline{X} = \frac{1}{n} \sum_{i=1}^n X_i$, $E(\overline{X}) = \mu$ (ước lượng không chệch), $V(\overline{X}) = \frac{\sigma^2}{n}$. Giá trị quan sát: $\overline{x} = \frac{1}{n}\sum_{i=1}^n x_i$.
  - **Phương sai mẫu và phương sai mẫu hiệu chỉnh**:
    - Phương sai mẫu: $\widetilde{S}^2 = \frac{1}{n} \sum_{i=1}^n (X_i - \overline{X})^2$, $E(\widetilde{S}^2) = \frac{n-1}{n}\sigma^2$ (ước lượng chệch).
    - Phương sai mẫu hiệu chỉnh: $S^2 = \frac{n}{n-1}\widetilde{S}^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \overline{X})^2$, $E(S^2) = \sigma^2$ (ước lượng không chệch). Giá trị quan sát: $s^2 = \frac{1}{n-1}\sum_{i=1}^n (x_i - \overline{x})^2$.
  - **Tần suất mẫu**: $\widehat{P} = \frac{Y}{n}$ ($Y \sim B(n, p)$), $E(\widehat{P}) = p, V(\widehat{P}) = \frac{p(1-p)}{n}$. Giá trị quan sát: $f = \frac{k}{n}$ (hoặc $\widehat{p} = \frac{y}{n}$).
- **Phân phối mẫu**:
  - Khi kích thước mẫu lớn ($n = 973 \ge 30$), theo Định lý giới hạn trung tâm:
    - Thống kê $Z = \frac{\overline{X} - \mu}{S/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$.
    - Thống kê $T = \frac{\overline{X} - \mu}{S/\sqrt{n}} \sim t(n-1)$.
    - Thống kê $\frac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$.

---

## 3. Thống kê mô tả thực nghiệm ($n = 973$)
| Biến số | Trung bình ($\bar{x}$) | Độ lệch chuẩn ($s$) | Trung vị | Min | Max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Calories_Burned` (kcal) | 905.42 | 272.64 | 893.00 | 285.00 | 1650.00 |
| `Session_Duration` (giờ) | 1.256 | 0.343 | 1.25 | 0.50 | 2.00 |
| `Avg_BPM` (nhịp/phút) | 143.44 | 15.23 | 143.00 | 120.00 | 170.00 |
| `Weight` (kg) | 73.09 | 15.00 | 72.80 | 40.00 | 115.00 |
- Tỷ lệ giới tính: Nam chiếm 52.52% ($k = 511$, $f = 52.52\%$).
- Loại bài tập: Cardio ($k = 251$, $f = 25.80\%$), HIIT ($k = 247$, $f = 25.39\%$), Strength (24.77%), Yoga (24.05%).
*(Toàn bộ các hàm thống kê được nhóm tự cài đặt trong mô-đun `src/stats_utils.py`)*

---

## 4. Chương 2: ước lượng điểm và khoảng tin cậy 95%
- **Phương pháp ước lượng điểm**:
  - Phương pháp mô men và hợp lý cực đại cho $\mu$: $\hat{\mu} = \bar{x} = 905.42$ kcal.
  - Phương pháp hợp lý cực đại cho $\sigma^2$: $\hat{\sigma}^2 = \frac{1}{n}\sum (x_i - \bar{x})^2$ (chệch dưới). Nhân $\frac{n}{n-1}$ thu được $s^2 = 0.1177$ (hiệu chỉnh không chệch).
- **Diễn giải tần suất độ tin cậy 95%**: Lặp lại việc lấy mẫu độc lập 973 người vô hạn lần thì 95% các khoảng tin cậy tính được sẽ chứa đúng tham số thực của tổng thể.
- **Kết quả khoảng tin cậy 95% hai phía**:
  - $\mu_{\text{Calories}}$: $[888.27, 922.57]$ (phân phối Student $t$, bậc tự do $972$).
  - $\sigma^2_{\text{Duration}}$: $[0.1079, 0.1289]$ (phân phối $\chi^2$, bậc tự do $972$).
  - $\sigma_{\text{Duration}}$: $[0.3284, 0.3590]$ (căn bậc hai khoảng tin cậy $\sigma^2$).
  - $p_{\text{Male}}$: $[0.4938, 0.5566]$ (xấp xỉ phân phối chuẩn tắc $Z$).
  - $\mu_1 - \mu_2$ (Nam -- Nữ): $[48.47, 115.95]$ (hai phương sai chưa biết, khác nhau).
  - $p_1 - p_2$ (Calo $\ge 1000$): $[0.0735, 0.1912]$ (xấp xỉ chuẩn tắc $Z$).

---

## 5. Chương 3: kiểm định tham số và 3 cách tiếp cận
- **Quy trình 5 bước kiểm định**: (1) Cặp giả thuyết $H_0/H_1$ $\rightarrow$ (2) Mức ý nghĩa $\alpha = 0.05$ $\rightarrow$ (3) Tiêu chuẩn kiểm định $\rightarrow$ (4) Tính giá trị quan sát, $P$-giá trị $\rightarrow$ (5) Kết luận.
- **Tính nhất quán của 3 cách tiếp cận**:
  1. *Cách 1 (Miền bác bỏ)*: Giá trị quan sát rơi vào miền bác bỏ $W_\alpha$.
  2. *Cách 2 ($P$-giá trị)*: $P\text{-giá trị} \le \alpha = 0.05$.
  3. *Cách 3 (Đối chiếu khoảng tin cậy)*: Giá trị giả định $\theta_0$ không thuộc khoảng tin cậy 95% tương ứng.
- **Bảng tổng hợp kết luận kiểm định ($\alpha = 0.05$)**:
  - $H_0: \mu = 900$: Không bác bỏ $H_0$ ($t_0 = 0.620, P = 0.5352$).
  - $H_0: \sigma^2 = 0.10$: Bác bỏ $H_0$ ($k_0^2 = 1143.77, P = 0.0002$).
  - $H_0: p = 0.50$: Không bác bỏ $H_0$ ($z_0 = 1.571, P = 0.1162$).
  - $H_0: \sigma_1^2 = \sigma_2^2$: Bác bỏ $H_0$ ($f_0 = 1.318, P = 0.0025 \rightarrow \sigma_1^2 \ne \sigma_2^2$).
  - $H_0: \mu_1 = \mu_2$: Bác bỏ $H_0$ ($t_0 = 4.781, P = 2.01 \times 10^{-6} \rightarrow$ Nam đốt calo cao hơn).

---

## 6. Chương 3: phân tích phương sai một nhân tố và phi tham số
- **Phân tích phương sai một nhân tố**:
  - Cặp giả thuyết: $H_0: \mu_{\text{Cardio}} = \mu_{\text{HIIT}} = \mu_{\text{Strength}} = \mu_{\text{Yoga}}$.
  - Bảng phân tích biến thiên:
    - Nhân tố (giữa các nhóm): $SS_F = 1.48 \times 10^6$ (bậc tự do 3), $MS_F = 493,760$, thống kê $F_0 = 6.7644$.
    - Sai số (trong nội bộ): $SS_E = 7.08 \times 10^7$ (bậc tự do 969), $MS_E = 73,035$.
  - Tiêu chuẩn kiểm định: $F_0 = \frac{MS_F}{MS_E} = 6.7644 > f_{0.05; 3; 969} = 2.6141$ ($P\text{-giá trị} = 0.00016$).
  - $\rightarrow$ **Bác bỏ $H_0$**: Loại bài tập có ảnh hưởng thực sự đến lượng calo tiêu thụ.
- **Kiểm định phi tham số Chi-bình phương**:
  - *Sự phù hợp của phân phối xác suất (chuẩn)*:
    - `Session_Duration`: $k_0^2 = 2.4578, P = 0.9303 > 0.05$.
    - `Calories_Burned`: $k_0^2 = 5.2140, P = 0.6338 > 0.05$.
    - $\rightarrow$ Phù hợp với phân phối chuẩn.
  - *Kiểm định tính độc lập*:
    - Bảng tiếp biến $2 \times 3$, bậc tự do $(2-1)(3-1) = 2$.
    - $k_0^2 = 0.0128 < \chi^2_{0.05; 2} = 5.9915$ ($P = 0.9936$).
    - $\rightarrow$ Không bác bỏ $H_0$: Giới tính và cấp độ kinh nghiệm độc lập nhau.

---

## 7. Chương 4.1: hồi quy tuyến tính đơn
- **Mô hình hồi quy tuyến tính đơn**: $Y = \beta_0 + \beta_1 x + \varepsilon$, với $\varepsilon \sim \mathcal{N}(0, \sigma^2)$.
- **Phương trình hồi quy mẫu (bình phương bé nhất)**:
  $$\hat{y} = -1.4465 + 721.7860 \cdot x$$
  - Hệ số xác định $R^2 = 0.8247$: Thời lượng tập giải thích $82.47\%$ biến thiên lượng calo.
  - Hệ số góc $\hat{\beta}_1 = 721.79$ ($P\text{-giá trị} < 10^{-15}$): Mỗi giờ tập tăng đốt thêm 721.8 kcal.
- **Mối liên hệ tương đương giữa kiểm định $T_0$ và $F_0$**:
  $$T_0^2 = \left(\frac{\hat{\beta}_1}{s / \sqrt{S_{xx}}}\right)^2 = \frac{\hat{\beta}_1^2 S_{xx}}{s^2} = \frac{MSR}{MSE} = F_0$$
  Thực nghiệm: $T_0^2 = 67.5920^2 = 4568.6744 = F_0$.

---

## 8. Khoảng tin cậy so với khoảng dự đoán và ý nghĩa hệ số chặn
- **So sánh dải khoảng tin cậy và dải dự đoán**:
  - Khoảng tin cậy cho phản hồi trung bình $E(Y|x_0)$:
    $$\hat{y}_0 \pm t_{\alpha/2}(n-2) \cdot s \sqrt{\frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$
  - Khoảng dự đoán cho cá thể mới $y_0$:
    $$\hat{y}_0 \pm t_{\alpha/2}(n-2) \cdot s \sqrt{\mathbf{1} + \frac{1}{n} + \frac{(x_0 - \bar{x})^2}{S_{xx}}}$$
  - Khoảng dự đoán luôn rộng hơn vì chứa thêm số hạng "$+1$", biểu diễn phương sai sai số tự nhiên của cá thể mới: $V(y_0 - \hat{y}_0) = V(\hat{y}_0) + \sigma^2$.
- **Ý nghĩa thực tế và toán học của hệ số chặn $\hat{\beta}_0 = -1.45$**:
  - *Về thực tế*: Dữ liệu không có buổi tập nào 0 giờ ($x \in [0.5, 2.0]$). Ngoại suy tại $x=0$ không mang ý nghĩa thực tiễn.
  - *Về toán học*: $\hat{\beta}_0$ là mỏ neo toán học bắt buộc để:
    1. Đảm bảo tổng phần dư $\sum e_i = 0$.
    2. Buộc đường hồi quy đi qua trọng tâm $(\bar{x}, \bar{y})$.
    3. Giữ phân rã tổng bình phương $SST = SSR + SSE$.

---

## 9. Chương 4.2: phân tích phần dư và hệ số tương quan
- **Chẩn đoán phần dư ($e_i = y_i - \hat{y}_i$)**:
  - Kỳ vọng sai số $E(e_i) \approx 0$, hệ số bất đối xứng $-0.02$, hệ số nhọn $0.05$.
  - Phương sai sai số đồng nhất (thuần nhất).
  - Đồ thị xác suất bám sát đường phân phối chuẩn.
- **Hệ số tương quan mẫu $r = 0.9081$**:
  - Kiểm định $H_0: \rho = 0$: $t_0 = 67.592$ ($P\text{-giá trị} < 10^{-15}$).
  - Biến đổi Fisher: $U = \frac{1}{2}\ln \frac{1+r}{1-r} = \text{arctanh}(r) = 1.5167$.
  - Kiểm định $H_0: \rho = 0.85$: $Z_0 = \frac{U - U_0}{\sqrt{1/(n-3)}} = 8.1633 \rightarrow$ Bác bỏ.
  - Khoảng tin cậy 95% cho hệ số tương quan $\rho$: $[0.8965, 0.9185]$.

---

## 10. Trả lời câu hỏi trọng tâm: tương quan và nhân quả
- **Nguyên lý cốt lõi**: *"Tương quan không đồng nghĩa với nhân quả"*. Mặc dù hệ số $r = 0.9081$ rất cao, thời lượng tập không phải nguyên nhân duy nhất quyết định lượng calo tiêu thụ.
- **Các yếu tố cùng chi phối**:
  1. *Cường độ gắng sức tim mạch (`Avg_BPM`, `Max_BPM`)*: Người tập ở nhịp tim 160 BPM tiêu thụ calo vượt trội so với nhịp tim 110 BPM trong cùng thời gian tập.
  2. *Khối lượng cơ thể (`Weight`)*: Thể trọng lớn đòi hỏi tiêu hao công năng cơ học lớn hơn.
  3. *Loại bài tập (`Workout_Type`)*: HIIT và Cardio đốt cháy calo trên mỗi phút tập cao hơn nhiều so với Yoga.
- **Định hướng phát triển**: Mở rộng sang mô hình **Hồi quy tuyến tính bội** để kiểm soát đồng thời tác động của nhiều biến giải thích.

---

## 11. Tổng kết
- **Sản phẩm hoàn thành**:
  - `main.py`: Chạy tuần tự 6 mô-đun và kiểm tra chéo tự động trong 25 giây.
  - Báo cáo toàn văn: `BaoCao_SLTK_Nhom18.pdf`.
  - Slide thuyết trình Beamer: `Slide_ThuyetTrinh_Nhom18.pdf`.
  - Mã nguồn và tài liệu lưu trữ đầy đủ trong thư mục dự án.
- **Kết quả thực nghiệm chính**:
  - *Mẫu và ước lượng*: Kích thước $n=973$; ước lượng điểm và khoảng tin cậy 95% vững chắc cho kỳ vọng, phương sai, tỷ lệ.
  - *Kiểm định và phân tích phương sai*: Bác bỏ tính đồng nhất calo theo loại bài tập ($F_0 = 6.7644$, $P < 0.001$).
  - *Hồi quy và tương quan*: $R^2 = 82.47\%$, hệ số tương quan mẫu $r = 0.9081$, mở rộng sang hồi quy tuyến tính bội.

---

## 12. Thank you
- **THANK YOU!**
- Cảm ơn thầy cô và các bạn đã chú ý lắng nghe!
