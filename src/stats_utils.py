
"""Các hàm thống kê tự cài đặt (trung bình mẫu, phương sai mẫu hiệu chỉnh, độ lệch chuẩn, tần suất mẫu)

Chỉ dùng numpy/pandas để tính toán; scipy.stats chỉ dùng ở các script để tra
giá trị tới hạn và tính P-giá trị.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Đường dẫn dự án
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "gym_members_exercise_tracking.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
TABLES_DIR = ROOT / "outputs" / "tables"
FIGURES_DIR = ROOT / "outputs" / "figures"
SECTIONS_DIR = ROOT / "report" / "sections"

for _d in (TABLES_DIR, FIGURES_DIR, SECTIONS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    """Đọc dữ liệu sạch (data/processed/*.csv) nếu có, ngược lại đọc dữ liệu thô."""
    processed = sorted(PROCESSED_DIR.glob("*.csv")) if PROCESSED_DIR.exists() else []
    path = processed[0] if processed else RAW_CSV
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu: đặt file CSV vào {RAW_CSV} (hoặc data/processed/)."
        )
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    # Bộ Kaggle gốc ghi đơn vị trong tên cột -> chuẩn hóa tên dùng trong code
    df = df.rename(columns={"Session_Duration (hours)": "Session_Duration",
                            "Workout_Frequency (days/week)": "Workout_Frequency"})
    return df


# ----------------------------------------------------------------------------
# Thống kê mẫu cơ bản (tự cài đặt)
# ----------------------------------------------------------------------------
def sample_mean(x) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.sum(x) / x.size)


def sample_var(x, ddof: int = 1) -> float:
    """ddof=1: phương sai mẫu hiệu chỉnh S^2; ddof=0: phương sai mẫu (ước lượng MLE/MoM)."""
    x = np.asarray(x, dtype=float)
    return float(np.sum((x - sample_mean(x)) ** 2) / (x.size - ddof))


def sample_std(x, ddof: int = 1) -> float:
    return float(np.sqrt(sample_var(x, ddof)))


def sample_prop(indicator) -> float:
    """Tần suất mẫu p_hat = (số phần tử thỏa điều kiện) / n."""
    a = np.asarray(indicator, dtype=float)
    return float(np.sum(a) / a.size)


def sample_median(x) -> float:
    """Trung vị mẫu."""
    x = np.asarray(x, dtype=float)
    return float(np.median(x))


def sample_quantile(x, q: float) -> float:
    """Phân vị mẫu bậc q (0 ≤ q ≤ 1)."""
    x = np.asarray(x, dtype=float)
    return float(np.percentile(x, q * 100))


# ----------------------------------------------------------------------------
# EDA – Phát hiện ngoại lai bằng IQR (dùng cho Chương 1)
# ----------------------------------------------------------------------------
def detect_outliers_iqr(x, k: float = 1.5) -> dict:
    """Phát hiện ngoại lai theo quy tắc IQR.

    Ngoại lai nếu xᵢ < Q₁ − k·IQR hoặc xᵢ > Q₃ + k·IQR (mặc định k = 1.5).
    """
    x = np.asarray(x, dtype=float)
    q1 = float(np.percentile(x, 25))
    q3 = float(np.percentile(x, 75))
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    mask = (x < lower) | (x > upper)
    return {
        "Q1": q1, "Q3": q3, "IQR": iqr,
        "lower_bound": lower, "upper_bound": upper,
        "n_outliers": int(mask.sum()),
        "outlier_indices": np.where(mask)[0],
    }


def describe_series(x) -> dict:
    """Thống kê mô tả cho một chuỗi số (dùng toàn bộ hàm tự cài đặt)."""
    x = np.asarray(x, dtype=float)
    return {
        "n": x.size,
        "x_bar": sample_mean(x),
        "S2": sample_var(x, ddof=1),
        "S": sample_std(x, ddof=1),
        "min": float(np.min(x)),
        "Q1": sample_quantile(x, 0.25),
        "median": sample_median(x),
        "Q3": sample_quantile(x, 0.75),
        "max": float(np.max(x)),
    }


# ----------------------------------------------------------------------------
# ANOVA 1 nhân tố (tự cài đặt) – dùng cho Chương 3 phần 2
# ----------------------------------------------------------------------------
def one_way_anova(*groups) -> dict:
    """Phân tích phương sai 1 nhân tố (One-Way ANOVA).

    Tham số
    -------
    *groups : array-like
        Các nhóm mẫu (ít nhất 2 nhóm).

    Trả về
    ------
    dict chứa: k, N, group_n, group_mean, grand_mean,
               SSF, SSE, SST, df_F, df_E, MSF, MSE, F_stat.
    """
    groups = [np.asarray(g, dtype=float) for g in groups]
    k = len(groups)
    N = sum(g.size for g in groups)

    # Trung bình chung (Grand Mean)
    grand_mean = sample_mean(np.concatenate(groups))

    # Trung bình từng nhóm
    group_means = [sample_mean(g) for g in groups]
    group_ns = [g.size for g in groups]

    # Tổng bình phương
    # SSF (giữa các nhóm / Factor)
    ssf = sum(ni * (mi - grand_mean) ** 2 for ni, mi in zip(group_ns, group_means))
    # SSE (trong nhóm / Error)
    sse = sum(float(np.sum((g - mi) ** 2)) for g, mi in zip(groups, group_means))
    # SST (tổng)
    sst = ssf + sse

    df_f = k - 1       # bậc tự do nhân tố
    df_e = N - k       # bậc tự do sai số
    msf = ssf / df_f   # trung bình bình phương nhân tố
    mse = sse / df_e   # trung bình bình phương sai số
    f_stat = msf / mse

    return {
        "k": k, "N": N,
        "group_n": group_ns, "group_mean": group_means,
        "grand_mean": grand_mean,
        "SSF": ssf, "SSE": sse, "SST": sst,
        "df_F": df_f, "df_E": df_e,
        "MSF": msf, "MSE": mse, "F_stat": f_stat,
    }


# ----------------------------------------------------------------------------
# Kiểm định Chi-bình phương phù hợp (Goodness-of-Fit) – tự cài đặt
# ----------------------------------------------------------------------------
def chi2_goodness_of_fit(observed, expected) -> dict:
    """Kiểm định Chi-bình phương phù hợp.

    χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ

    Tham số
    -------
    observed : array-like  — tần số quan sát
    expected : array-like  — tần số kỳ vọng

    Trả về
    ------
    dict chứa: chi2_stat, df, observed, expected.
    """
    O = np.asarray(observed, dtype=float)
    E = np.asarray(expected, dtype=float)
    chi2 = float(np.sum((O - E) ** 2 / E))
    return {"chi2_stat": chi2, "df": len(O) - 1, "observed": O, "expected": E}


# ----------------------------------------------------------------------------
# Kiểm định Chi-bình phương tính độc lập – tự cài đặt
# ----------------------------------------------------------------------------
def chi2_independence(contingency_table) -> dict:
    """Kiểm định Chi-bình phương tính độc lập cho bảng chéo.

    Eᵢⱼ = (tổng hàng i × tổng cột j) / N
    χ² = Σᵢ Σⱼ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ
    df = (r − 1)(c − 1)

    Tham số
    -------
    contingency_table : 2-D array-like (bảng chéo tần số quan sát)

    Trả về
    ------
    dict chứa: chi2_stat, df, expected, observed.
    """
    O = np.asarray(contingency_table, dtype=float)
    r, c = O.shape
    row_sums = O.sum(axis=1, keepdims=True)
    col_sums = O.sum(axis=0, keepdims=True)
    N = O.sum()
    E = row_sums * col_sums / N
    chi2 = float(np.sum((O - E) ** 2 / E))
    df = (r - 1) * (c - 1)
    return {"chi2_stat": chi2, "df": df, "expected": E, "observed": O, "N": N}


# ----------------------------------------------------------------------------
# Hồi quy tuyến tính đơn (OLS) - dùng chung cho Chương 4
# ----------------------------------------------------------------------------
def simple_ols(x, y) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = x.size
    xbar, ybar = sample_mean(x), sample_mean(y)
    sxx = float(np.sum((x - xbar) ** 2))
    sxy = float(np.sum((x - xbar) * (y - ybar)))
    syy = float(np.sum((y - ybar) ** 2))
    b1 = sxy / sxx
    b0 = ybar - b1 * xbar
    y_hat = b0 + b1 * x
    resid = y - y_hat
    sse = float(np.sum(resid**2))
    s2 = sse / (n - 2)
    return {
        "n": n, "b0": b0, "b1": b1, "sxx": sxx, "sxy": sxy, "syy": syy,
        "y_hat": y_hat, "resid": resid, "sse": sse, "ssr": syy - sse,
        "s2": s2, "s": float(np.sqrt(s2)), "r2": 1 - sse / syy,
        "r": sxy / float(np.sqrt(sxx * syy)),
    }


# ----------------------------------------------------------------------------
# Tiện ích định dạng
# ----------------------------------------------------------------------------
def fmt(v, nd: int = 4) -> str:
    if isinstance(v, (float, np.floating)):
        if np.isposinf(v):
            return "+∞"
        if np.isneginf(v):
            return "−∞"
        if v != 0 and abs(v) < 10 ** (-nd):
            return f"{v:.2e}"
        return f"{v:.{nd}f}"
    return str(v)


def md_table(df: pd.DataFrame, nd: int = 4) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(fmt(r[c], nd) for c in cols) + " |")
    return "\n".join(lines)