# Báo cáo cuối kỳ — Môn Suy luận thống kê (MI3031) — Nhóm 18

## 1. Thông tin thành viên nhóm & Phân công thực hiện
- **Nguyễn Thị Thảo** — MSSV: `202419101` (Owner: Chương 1, Chương 3 ANOVA & Phi tham số, Chương 4.1 Hồi quy đơn & Biên tập Báo cáo / Slide)
- **Nguyễn Văn Nam Khánh** — MSSV: `202419069` (Owner: Chương 2 Ước lượng tham số, Chương 3 Kiểm định tham số, Chương 4.2 Phần dư & Tương quan tuyến tính)
- **Đơn vị đào tạo**: Viện Toán ứng dụng và Tin học (SAMI), Đại học Bách khoa Hà Nội
- **Học kỳ**: 2026.1

---

## 2. Thông tin bộ dữ liệu nghiên cứu
- **Tên bộ dữ liệu**: Gym Members Exercise Tracking
- **Tệp dữ liệu nguồn**: `data/raw/gym_members_exercise_tracking.csv`
- **Quy mô**: 973 quan sát thành viên phòng gym, 15 biến (12 biến định lượng, 3 biến định tính)
- **Nguồn dữ liệu**: [Kaggle - Gym Members Exercise Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset)
- **Biến trọng tâm trong nghiên cứu**:
  - `Calories_Burned` ($Y$): Lượng calo tiêu thụ trong buổi tập (kcal) — biến phụ thuộc chính
  - `Session_Duration` ($X$): Thời lượng buổi tập (giờ) — biến độc lập chính
  - `Gender`: Giới tính (Male: 511, Female: 462)
  - `Workout_Type`: Loại hình bài tập (Cardio, HIIT, Strength, Yoga)
  - `Experience_Level`: Trình độ kinh nghiệm tập luyện (1: Mới, 2: Trung cấp, 3: Nâng cao)
  - `Avg_BPM`, `Max_BPM`, `Weight (kg)`, `Fat_Percentage`: Các chỉ số sinh lý can thiệp

---

## 3. Cấu trúc thư mục dự án
```text
SLTK_Nhom-18_Gym-Members-Exercise/
├── data/
│   └── raw/
│       └── gym_members_exercise_tracking.csv    # Dữ liệu gốc 973 quan sát
├── src/
│   ├── stats_utils.py               # Mô-đun hàm thống kê tự cài đặt (x_bar, S^2, S, p_hat, OLS, md_table,...)
│   ├── 01_eda_chap1.py              # Chương 1 - Mẫu ngẫu nhiên, Tiền xử lý & Thống kê mô tả
│   ├── 02_estimation_chap2.py       # Chương 2 - Ước lượng điểm (MoM, MLE) & Khoảng tin cậy 95%
│   ├── 03_hypothesis_parametric.py  # Chương 3 (Phần 1) - Kiểm định tham số 1 & 2 tổng thể
│   ├── 04_anova_nonparametric.py    # Chương 3 (Phần 2) - ANOVA 1 nhân tố & Kiểm định phi tham số Chi-bình phương
│   ├── 05_simple_regression.py      # Chương 4.1 - Hồi quy tuyến tính đơn (OLS, ANOVA, t-test, F-test, KTC & KTD)
│   └── 06_residuals_correlation.py  # Chương 4.2 - Chẩn đoán phần dư, Tương quan Pearson & Biến đổi Fisher Z
├── outputs/
│   ├── tables/                      # Bảng số liệu thống kê xuất ra dưới định dạng CSV
│   │   ├── 01_summary_stats.csv
│   │   ├── 02_confidence_intervals.csv
│   │   ├── 02_point_estimates.csv
│   │   ├── 03_error_power.csv
│   │   ├── 03_parametric_tests.csv
│   │   ├── 04_anova_chi2.csv
│   │   ├── 05_prediction_intervals.csv
│   │   ├── 05_regression_anova.csv
│   │   ├── 05_regression_coefficients.csv
│   │   ├── 05_regression_summary.csv
│   │   ├── 06_correlation_matrix.csv
│   │   └── 06_residuals_summary.csv
│   └── figures/                     # Đồ thị chất lượng cao (150 & 300 DPI)
│       ├── 05_regression_fit.png
│       ├── 05_slr_bands.png
│       └── 06_residual_diagnostics.png
├── report/
│   ├── sections/                    # Các báo cáo thành phần dưới dạng Markdown
│   │   ├── 01_chap1.md
│   │   ├── 02_chap2.md
│   │   ├── 03_chap3_part1.md
│   │   ├── 04_chap3_part2.md
│   │   ├── 05_chap4_slr.md
│   │   └── 06_chap4_corr.md
│   ├── BaoCao_SLTK_Nhom18.pdf       # Toàn văn báo cáo khoa học chính thức (Biên dịch từ LaTeX)
│   ├── BaoCao_SLTK_Nhom18.tex       # Mã nguồn LaTeX bài báo cáo
│   ├── Slide_ThuyetTrinh_Nhom18.pdf # Bộ slide thuyết trình chính thức (Biên dịch từ Beamer)
│   ├── Slide_ThuyetTrinh_Nhom18.tex # Mã nguồn Beamer slide
│   └── Slide_ThuyetTrinh_Nhom18.md  # Dàn ý chi tiết bài thuyết trình nhóm
├── main.py                          # Pipeline thực thi tuần tự từ 01 đến 06 & Kiểm tra chéo số liệu
├── README.md                        # Hướng dẫn chi tiết dự án
└── requirements.txt                 # Các thư viện phụ thuộc (numpy, pandas, scipy, matplotlib)
```

---

## 4. Nguyên tắc cài đặt & Kiểm định lý thuyết
- **Tự cài đặt công thức toán học**: 100% các công thức trung bình mẫu, phương sai hiệu chỉnh (chia $n-1$), tần suất mẫu, hiệp phương sai, OLS, phân tích phương sai hồi quy (SSR, SSE, SST), biến đổi Fisher $Z$ đều được tự cài đặt từ đầu bằng Python/NumPy mà không dùng các hộp đen như `sklearn.linear_model`.
- **Phạm vi dùng thư viện**: Thư viện `scipy.stats` chỉ được sử dụng đúng mục đích tra cứu phân vị lý thuyết ($z, t, \chi^2, F$) và tính $P$-value.
- **Tính nhất quán của các định lý toán học**:
  - **Định lý 5 & 6 (Hồi quy tuyến tính đơn)**: Chứng minh và kiểm chứng thực nghiệm tính tương đương $t_0^2 = f_0$ ($67.5920^2 = 4568.6744$).
  - **Định lý 7 & 8**: Khoảng dự đoán cho quan sát mới luôn rộng hơn khoảng tin cậy của kỳ vọng phản hồi đúng một số hạng $+1$ do phương sai tự nhiên $\sigma^2$ của chính cá thể mới.
  - **Kiểm định tham số 3 cách**: Miền bác bỏ cổ điển, $P$-value và Khoảng tin cậy cho kết luận nhất quán 100%.

---

## 5. Hướng dẫn thực thi chương trình

### Cách 1: Chạy tự động toàn bộ Pipeline & Kiểm tra chéo
Chỉ cần thực thi duy nhất file `main.py` từ thư mục gốc của dự án:
```powershell
python main.py
```
Lệnh trên sẽ:
1. Thực thi tuần tự 6 mô-đun: `src/01_eda_chap1.py` $\rightarrow$ `src/06_residuals_correlation.py`.
2. Tự động kiểm tra chéo tính toàn vẹn cỡ mẫu ($n = 973$), đẳng thức $t_0^2 = f_0$, $R^2 = r^2$, và kiểm tra sự tồn tại của toàn bộ bảng kết quả và biểu đồ.
3. Tự động biên dịch lại tài liệu báo cáo toàn văn PDF qua XeLaTeX.

### Cách 2: Chạy độc lập từng mô-đun
Bạn có thể chạy riêng từng script theo nhu cầu:
```powershell
python src/01_eda_chap1.py              # Chương 1
python src/02_estimation_chap2.py       # Chương 2
python src/03_hypothesis_parametric.py  # Chương 3 (Phần 1)
python src/04_anova_nonparametric.py    # Chương 3 (Phần 2)
python src/05_simple_regression.py      # Chương 4.1
python src/06_residuals_correlation.py  # Chương 4.2
```

### Cách 3: Biên dịch lại tài liệu Báo cáo & Slide (LaTeX/XeLaTeX)
Để biên dịch lại file báo cáo toàn văn và slide thuyết trình:
```powershell
cd report
xelatex -interaction=batchmode -disable-installer BaoCao_SLTK_Nhom18.tex
xelatex -interaction=batchmode -disable-installer Slide_ThuyetTrinh_Nhom18.tex
```

---

## 6. Bảng kết quả tổng hợp chính của Đề tài

| STT | Nội dung nghiên cứu | Giá trị thống kê / Hệ số | Kết luận thống kê ($\alpha = 0.05$) |
| :---: | :--- | :---: | :--- |
| **1** | Kỳ vọng lượng calo đốt cháy ($\mu$) | $\bar{x} = 905.42$ kcal | KTC 95%: $[888.27, 922.57]$ kcal |
| **2** | So sánh lượng calo Nam vs Nữ | $t_W = 4.7814$ ($P = 2.01 \times 10^{-6}$) | Nam giới đốt calo cao hơn nữ giới trung bình $82.21$ kcal |
| **3** | ANOVA calo theo loại bài tập | $F = 6.7644$ ($P = 0.00016$) | Bác bỏ $H_0$; loại bài tập có ảnh hưởng thực sự (Cardio, HIIT cao nhất) |
| **4** | Phù hợp chuẩn (Session\_Duration) | $\chi^2 = 2.4578$ ($P = 0.9303$) | Dữ liệu hoàn toàn phù hợp với phân phối chuẩn |
| **5** | Tính độc lập: Giới tính $\times$ Trình độ | $\chi^2 = 0.0128$ ($P = 0.9936$) | Giới tính và Cấp độ kinh nghiệm độc lập nhau |
| **6** | Mô hình hồi quy đơn OLS | $\hat{y} = -1.45 + 721.79 \cdot x$ | $R^2 = 82.47\%$, mỗi giờ tập tăng $721.79$ kcal ($P < 10^{-15}$) |
| **7** | Tương quan Pearson ($r$) | $r = 0.9081$ | KTC 95%: $[0.8965, 0.9185]$; tương quan đồng biến rất mạnh |
