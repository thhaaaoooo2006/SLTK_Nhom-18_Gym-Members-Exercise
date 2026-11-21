# Chương 1 — Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)

## 1. Cơ sở lý thuyết

### 1.1. Mẫu ngẫu nhiên (Random Sample)

Cho $X$ là biến ngẫu nhiên có hàm phân phối $F(x)$ chưa biết.
Bộ $n$ quan sát $X_1, X_2, \ldots, X_n$ được gọi là **mẫu ngẫu nhiên** kích thước $n$
nếu chúng là $n$ biến ngẫu nhiên **độc lập** và có **cùng phân phối** với $X$ (i.i.d.).

### 1.2. Hàm thống kê (Statistic)

Mọi hàm $T = g(X_1, \ldots, X_n)$ **không chứa tham số chưa biết** được gọi là hàm thống kê.

### 1.3. Trung bình mẫu (Sample Mean)

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

$\bar{x}$ là ước lượng không chệch, vững và hiệu quả cho kỳ vọng $\mu$.

### 1.4. Phương sai mẫu hiệu chỉnh (Sample Variance, ddof = 1)

$$S^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

Chia cho $(n - 1)$ thay vì $n$ để $S^2$ là ước lượng **không chệch** cho $\sigma^2$.
Đại lượng $(n - 1)$ gọi là **bậc tự do** (degrees of freedom).

### 1.5. Độ lệch chuẩn mẫu hiệu chỉnh

$$S = \sqrt{S^2}$$

### 1.6. Tần suất mẫu (Sample Proportion)

$$\hat{p} = \frac{k}{n}$$

trong đó $k$ là số phần tử trong mẫu thỏa sự kiện $A$.

## 2. Mô tả bối cảnh

Bộ dữ liệu "Gym Members Exercise Tracking" ghi lại thông tin tập luyện
của 973 thành viên phòng gym, bao gồm các chỉ số thể chất, sinh lý
(nhịp tim, lượng calo đốt cháy), thói quen tập luyện (loại bài tập,
tần suất, thời lượng) và trình độ kinh nghiệm. Mục tiêu nghiên cứu là
áp dụng các phương pháp suy luận thống kê (ước lượng, kiểm định, hồi quy)
để phân tích mối quan hệ giữa thời lượng tập (Session_Duration) và lượng
calo tiêu thụ (Calories_Burned), cũng như so sánh sự khác biệt theo
giới tính (Gender), loại bài tập (Workout_Type) và trình độ kinh nghiệm
(Experience_Level).

## 3. Phân loại biến

### Biến định lượng (Numerical)

| Tên biến | Kiểu | Mô tả |
|---|---|---|
| `Age` | Rời rạc | Tuổi (năm) |
| `Weight (kg)` | Liên tục | Cân nặng (kg) |
| `Height (m)` | Liên tục | Chiều cao (m) |
| `Max_BPM` | Rời rạc | Nhịp tim tối đa (bpm) |
| `Avg_BPM` | Rời rạc | Nhịp tim trung bình (bpm) |
| `Resting_BPM` | Rời rạc | Nhịp tim khi nghỉ (bpm) |
| `Session_Duration` | Liên tục | Thời lượng buổi tập (giờ) |
| `Calories_Burned` | Liên tục | Lượng calo tiêu thụ (kcal) |
| `Fat_Percentage` | Liên tục | Tỷ lệ mỡ cơ thể (%) |
| `Water_Intake (liters)` | Liên tục | Lượng nước uống (lít/ngày) |
| `Workout_Frequency` | Rời rạc | Tần suất tập (ngày/tuần) |
| `BMI` | Liên tục | Chỉ số BMI |

### Biến phân loại (Categorical)

| Tên biến | Kiểu | Các giá trị |
|---|---|---|
| `Gender` | Danh nghĩa | Male, Female |
| `Workout_Type` | Danh nghĩa | Cardio, HIIT, Strength, Yoga |
| `Experience_Level` | Thứ bậc | 1 (Beginner), 2 (Intermediate), 3 (Advanced) |

## 4. Kiểm tra chất lượng dữ liệu

- **Kích thước mẫu**: n = 973 quan sát, 15 biến
- **Giá trị thiếu**: 0 (không có)
- **Hàng trùng lặp**: 0

### Kiểm tra ngoại lai (IQR)

| Biến | Q1 | Q3 | IQR | Cận dưới | Cận trên | Số ngoại lai | % ngoại lai |
|---|---|---|---|---|---|---|---|
| Age | 28.00 | 49.00 | 21.00 | -3.50 | 80.50 | 0 | 0.00 |
| Weight (kg) | 58.10 | 86.00 | 27.90 | 16.25 | 127.85 | 9 | 0.92 |
| Height (m) | 1.62 | 1.80 | 0.18 | 1.35 | 2.07 | 0 | 0.00 |
| Max_BPM | 170.00 | 190.00 | 20.00 | 140.00 | 220.00 | 0 | 0.00 |
| Avg_BPM | 131.00 | 156.00 | 25.00 | 93.50 | 193.50 | 0 | 0.00 |
| Resting_BPM | 56.00 | 68.00 | 12.00 | 38.00 | 86.00 | 0 | 0.00 |
| Session_Duration | 1.04 | 1.46 | 0.42 | 0.41 | 2.09 | 0 | 0.00 |
| Calories_Burned | 720.00 | 1076.00 | 356.00 | 186.00 | 1610.00 | 10 | 1.03 |
| Fat_Percentage | 21.30 | 29.30 | 8.00 | 9.30 | 41.30 | 0 | 0.00 |
| Water_Intake (liters) | 2.20 | 3.10 | 0.90 | 0.85 | 4.45 | 0 | 0.00 |
| Workout_Frequency | 3.00 | 4.00 | 1.00 | 1.50 | 5.50 | 0 | 0.00 |
| BMI | 20.11 | 28.56 | 8.45 | 7.44 | 41.23 | 25 | 2.57 |

**Quyết định**: Giữ nguyên dữ liệu gốc — các ngoại lai đều là giá trị sinh lý thực tế hợp lệ và mẫu đủ lớn (n = 973).

## 5. Bảng thống kê mô tả

*Các giá trị được tính bằng hàm tự cài đặt trong `src/stats_utils.py`*

| Biến | n | x̄ (trung bình) | S² (phương sai HC) | S (độ lệch chuẩn) | Min | Q1 | Median | Q3 | Max |
|---|---|---|---|---|---|---|---|---|---|
| Age | 973 | 38.6835 | 148.3750 | 12.1809 | 18.0000 | 28.0000 | 40.0000 | 49.0000 | 59.0000 |
| Weight (kg) | 973 | 73.8547 | 449.7581 | 21.2075 | 40.0000 | 58.1000 | 70.0000 | 86.0000 | 129.9000 |
| Height (m) | 973 | 1.7226 | 0.0163 | 0.1277 | 1.5000 | 1.6200 | 1.7100 | 1.8000 | 2.0000 |
| Max_BPM | 973 | 179.8839 | 132.8414 | 11.5257 | 160.0000 | 170.0000 | 180.0000 | 190.0000 | 199.0000 |
| Avg_BPM | 973 | 143.7667 | 205.7819 | 14.3451 | 120.0000 | 131.0000 | 143.0000 | 156.0000 | 169.0000 |
| Resting_BPM | 973 | 62.2230 | 53.6858 | 7.3271 | 50.0000 | 56.0000 | 62.0000 | 68.0000 | 74.0000 |
| Session_Duration | 973 | 1.2564 | 0.1177 | 0.3430 | 0.5000 | 1.0400 | 1.2600 | 1.4600 | 2.0000 |
| Calories_Burned | 973 | 905.4224 | 74333.3965 | 272.6415 | 303.0000 | 720.0000 | 893.0000 | 1076.0000 | 1783.0000 |
| Fat_Percentage | 973 | 24.9768 | 39.1803 | 6.2594 | 10.0000 | 21.3000 | 26.2000 | 29.3000 | 35.0000 |
| Water_Intake (liters) | 973 | 2.6266 | 0.3602 | 0.6002 | 1.5000 | 2.2000 | 2.6000 | 3.1000 | 3.7000 |
| Workout_Frequency | 973 | 3.3217 | 0.8337 | 0.9130 | 2.0000 | 3.0000 | 3.0000 | 4.0000 | 5.0000 |
| BMI | 973 | 24.9121 | 44.3673 | 6.6609 | 12.3200 | 20.1100 | 24.1600 | 28.5600 | 49.8400 |

## 6. Tần suất mẫu (biến phân loại)

| Biến | Giá trị | Số lượng (k) | p̂ = k/n |
|---|---|---|---|
| Gender | Female | 462 | 0.4748 |
| Gender | Male | 511 | 0.5252 |
| Workout_Type | Cardio | 255 | 0.2621 |
| Workout_Type | HIIT | 221 | 0.2271 |
| Workout_Type | Strength | 258 | 0.2652 |
| Workout_Type | Yoga | 239 | 0.2456 |
| Experience_Level | 1 | 376 | 0.3864 |
| Experience_Level | 2 | 406 | 0.4173 |
| Experience_Level | 3 | 191 | 0.1963 |
