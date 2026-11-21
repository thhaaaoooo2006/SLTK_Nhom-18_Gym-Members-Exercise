
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