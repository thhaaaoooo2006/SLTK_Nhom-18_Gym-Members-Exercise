# Chương 1: Mẫu ngẫu nhiên và thống kê mô tả

## 1. Cơ sở lý thuyết mẫu ngẫu nhiên

### 1.1. Định nghĩa mẫu ngẫu nhiên và hàm thống kê
- **Mẫu ngẫu nhiên**: Cho $X$ là biến ngẫu nhiên có hàm phân phối tích lũy $F(x)$ đặc trưng cho tổng thể nghiên cứu. Bộ $n$ đại lượng ngẫu nhiên $(X_1, X_2, \dots, X_n)$ được gọi là một mẫu ngẫu nhiên kích thước $n$ nếu chúng độc lập với nhau và có cùng phân phối xác suất với $X$ ($iid$ - independent and identically distributed):
  $$P(X_1 \le x_1, X_2 \le x_2, \dots, X_n \le x_n) = \prod_{i=1}^n F(x_i)$$
- **Hàm thống kê**: Mọi hàm thực $T = g(X_1, X_2, \dots, X_n)$ hoàn toàn xác định từ các biến ngẫu nhiên của mẫu và không chứa bất kỳ tham số tổng thể chưa biết nào đều được gọi là một hàm thống kê.

### 1.2. Các đặc trưng mẫu cơ bản
1. **Trung bình mẫu**:
   $$\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$$
   Đặc tính: $E(\bar{X}) = \mu$, $Var(\bar{X}) = \frac{\sigma^2}{n}$. $\bar{X}$ là ước lượng không chệch, vững và tiệm cận chuẩn theo Định lý Giới hạn Trung tâm (CLT).
2. **Phương sai mẫu hiệu chỉnh**:
   $$S^2 = \frac{1}{n - 1} \sum_{i=1}^n (X_i - \bar{X})^2$$
   Việc chia cho bậc tự do $n - 1$ thay vì $n$ là điều kiện toán học bắt buộc để loại bỏ độ chệch: $E(S^2) = \sigma^2$. Nếu chia cho $n$, ước lượng sẽ bị chệch dưới với $E(S_n^2) = \frac{n-1}{n}\sigma^2$.
3. **Độ lệch chuẩn mẫu hiệu chỉnh**: $S = \sqrt{S^2}$.
4. **Tần suất mẫu**:
   $$\hat{p} = \frac{k}{n} = \frac{1}{n} \sum_{i=1}^n I_A(X_i)$$
   với $I_A$ là biến chỉ thị cá thể thuộc nhóm biến cố quan tâm. $\hat{p}$ là ước lượng không chệch cho xác suất $p$ của tổng thể.

## 2. Bối cảnh nghiên cứu và phân loại biến

Bộ dữ liệu **Gym Members Exercise Tracking** gồm $n = 973$ quan sát cá thể thành viên phòng gym, theo dõi các chỉ số sinh trắc học, thói quen tập luyện và hiệu suất tiêu thụ năng lượng:
- **Biến định lượng liên tục**: `Weight (kg)`, `Height (m)`, `Session_Duration` (giờ), `Calories_Burned` (kcal), `Fat_Percentage` (%), `Water_Intake (liters)`, `BMI`.
- **Biến định lượng rời rạc**: `Age` (năm), `Max_BPM`, `Avg_BPM`, `Resting_BPM`, `Workout_Frequency` (buổi/tuần).
- **Biến phân loại (Categorical)**: `Gender` (Male, Female), `Workout_Type` (Cardio, HIIT, Strength, Yoga), `Experience_Level` (1: Mới bắt đầu, 2: Trung cấp, 3: Nâng cao).

## 3. Kiểm tra chất lượng dữ liệu (Data Cleaning & Quality Assurance)

- **Giá trị khuyết thiếu (Missing values)**: 0 trường hợp (100% dữ liệu toàn vẹn).

- **Bản ghi trùng lặp (Duplicates)**: 0 trường hợp.

- **Kiểm định ngoại lai theo phương pháp Hàng rào IQR (Tukey's Fences)**:
  Khoảng chấp nhận giá trị hợp lệ: $[Q_1 - 1.5 \cdot IQR, \; Q_3 + 1.5 \cdot IQR]$, với $IQR = Q_3 - Q_1$.

| Biến | Số ngoại lai | Tỷ lệ ngoại lai (%) | Cận dưới IQR | Cận trên IQR |
|---|---|---|---|---|
| Age | 0 | 0.00 | -3.50 | 80.50 |
| Weight (kg) | 9 | 0.92 | 16.25 | 127.85 |
| Height (m) | 0 | 0.00 | 1.35 | 2.07 |
| Max_BPM | 0 | 0.00 | 140.00 | 220.00 |
| Avg_BPM | 0 | 0.00 | 93.50 | 193.50 |
| Resting_BPM | 0 | 0.00 | 38.00 | 86.00 |
| Session_Duration | 0 | 0.00 | 0.41 | 2.09 |
| Calories_Burned | 10 | 1.03 | 186.00 | 1610.00 |
| Fat_Percentage | 0 | 0.00 | 9.30 | 41.30 |
| Water_Intake (liters) | 0 | 0.00 | 0.85 | 4.45 |
| Workout_Frequency | 0 | 0.00 | 1.50 | 5.50 |
| BMI | 25 | 2.57 | 7.43 | 41.23 |
*Nhận định*: Các ngoại lai phát hiện ở `Calories_Burned`, `BMI` hay `Water_Intake` phản ánh độ phân tán sinh lý và cường độ vận động thực tế của các vận động viên thể hình/cường độ cao, không phải lỗi nhập liệu. Do đó, toàn bộ $973$ mẫu được giữ nguyên để bảo đảm tính khách quan.

## 4. Bảng thống kê mô tả thực nghiệm

### 4.1. Thống kê mô tả các biến định lượng

| Biến | n | x_bar | S2 | S | Min | Q1 | Median | Q3 | Max |
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

### 4.2. Tần suất mẫu các biến phân loại

| Biến | Giá trị | Số lượng (k) | p_hat |
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

*Các chỉ số trên được tính toán hoàn toàn bằng các hàm tự cài đặt từ `src/stats_utils.py`.*