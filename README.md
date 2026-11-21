# Báo cáo cuối kỳ — Môn Suy luận thống kê (MI3031) — Nhóm 18

## 1. Thông tin thành viên nhóm
- **Nguyễn Thị Thảo** — MSSV: `202419101`
- **Nguyễn Văn Nam Khánh** — MSSV: `202419069`

---

## 2. Thông tin bộ dữ liệu
- **Tên bộ dữ liệu**: Gym Members Exercise Tracking
- **Tệp dữ liệu**: `gym_members_exercise_tracking.csv`
- **Quy mô**: 973 quan sát, 15 biến
- **Nguồn dữ liệu**: [Kaggle - Gym Members Exercise Dataset](https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset)
- **Biến trọng tâm trong nghiên cứu**:
  - `Calories_Burned` (Y): Lượng calo tiêu thụ (biến phụ thuộc chính)
  - `Session_Duration` (X1): Thời lượng buổi tập (giờ/phút)
  - `Gender`: Giới tính
  - `Workout_Type`: Loại hình bài tập (Cardio, HIIT, Strength, Yoga,...)
  - `Experience_Level`: Mức độ kinh nghiệm (1, 2, 3)

---

## 3. Cấu trúc thư mục dự án
```text
SLTK_Nhom-18_Gym-Members-Exercise/
├── data/
│   └── raw/
│       └── .gitkeep
├── src/
│   ├── stats_utils.py               # Các hàm thống kê tự cài đặt (trung bình mẫu, phương sai mẫu hiệu chỉnh, độ lệch chuẩn, tần suất mẫu)
│   ├── 01_eda_chap1.py              # Chương 1 - Tiền xử lý & Thống kê mô tả
│   ├── 02_estimation_chap2.py       # Chương 2 - Ước lượng điểm & Khoảng tin cậy 95%
│   ├── 03_hypothesis_parametric.py  # Chương 3 - Kiểm định tham số 1 & 2 tổng thể
│   ├── 04_anova_nonparametric.py    # Chương 3 - ANOVA 1 nhân tố & Kiểm định Chi-bình phương
│   ├── 05_simple_regression.py      # Chương 4.1 - Hồi quy tuyến tính đơn (OLS, t-test, F-test, KTC & khoảng dự đoán)
│   └── 06_residuals_correlation.py  # Chương 4.1 & 4.2 - Phân tích phần dư & Tương quan tuyến tính
├── outputs/
│   ├── tables/
│   │   └── .gitkeep
│   └── figures/
│       └── .gitkeep
├── report/
│   └── sections/
│       └── .gitkeep
├── .gitignore
├── main.py                          # Khung gọi tuần tự các script trong src/
├── README.md                        # Tài liệu hướng dẫn dự án
└── requirements.txt                 # Các thư viện phụ thuộc
```

---

## 4. Nguyên tắc cài đặt
- **Tự cài đặt toán học & thống kê**: Tự cài đặt toàn bộ công thức thống kê từ đầu bằng `numpy` và `pandas` (được định nghĩa trong `src/stats_utils.py` và các module tương ứng).
- **Phạm vi sử dụng thư viện**: Chỉ sử dụng `scipy.stats` để tra giá trị tới hạn (phân phối chuẩn $z$, phân phối Student $t$, phân phối Chi-bình phương $\chi^2$, phân phối Fisher $F$) và tính $P$-giá trị (P-value).

---

## 5. Hướng dẫn chạy chương trình
1. **Cài đặt môi trường và các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Thực thi toàn bộ quy trình phân tích**:
   ```bash
   python main.py
   ```

---

## 6. Quy trình làm việc với Git & GitHub
- **Quy tắc nhánh chính**: **Tuyệt đối không push trực tiếp lên nhánh `main`**.
- **Quy trình tạo tính năng**:
  1. Tạo nhánh riêng theo từng mục công việc, ví dụ:
     - `feat/chap1-eda`
     - `feat/chap2-estimation`
     - `feat/chap3-hypothesis`
     - `feat/chap4-regression`
  2. Hoàn thành công việc, kiểm tra kết quả và push nhánh lên GitHub.
  3. Mở **Pull Request (PR)** hướng về nhánh `main`.
  4. Thành viên còn lại tiến hành **Review**, trao đổi và **Approve & Merge** sau khi đã kiểm tra kỹ lưỡng.
