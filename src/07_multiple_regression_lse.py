"""Chương 4 (Phần 3): Hồi quy tuyến tính bội — Mục 4.3.1 & 4.3.2
================================================================
Tác giả : Nhóm 18 (Nguyễn Văn Nam Khánh & Nguyễn Thị Thảo)
Mô-đun  : src/07_multiple_regression_lse.py
Outputs :
    - outputs/tables/07_mlr_normal_equations_m1.csv
    - outputs/tables/07_mlr_coefficients.csv
    - outputs/tables/07_mlr_comparison_L.csv
    - outputs/figures/07_mlr_plane_contour.png
    - outputs/figures/07_mlr_interaction_surface.png
    - report/sections/07_chap4_mlr_lse.md

────────────────────────────────────────────────────────────────
CƠ SỞ LÝ THUYẾT (Bám sát tuyệt đối Mục 4.3.1 & 4.3.2 — Bài giảng MI3031 Chương 4)
────────────────────────────────────────────────────────────────
1. Mục 4.3.1 — Giới thiệu về mô hình hồi quy tuyến tính bội:
   - Mô hình tổng quát với k biến độc lập (biến hồi quy / biến giải thích) x_1, ..., x_k:
         Y = β_0 + Σ_{j=1}^k β_j x_j + ε                          (57)
   - Hàm hồi quy tuyến tính lý thuyết (với E(ε) = 0):
         E(Y | x_1, ..., x_k) = β_0 + Σ_{j=1}^k β_j x_j           (62)
   - β_0 là hệ số chặn; β_1, ..., β_k là các hệ số góc (các hệ số hồi quy riêng),
     biểu thị sự thay đổi kỳ vọng trong Y trên mỗi đơn vị thay đổi của x_j khi
     tất cả các biến hồi quy còn lại x_i (i ≠ j) được giữ không đổi.
   - Mô hình có hiệu ứng tương tác giữa x_1 và x_2 (thuật ngữ tích chéo x_1·x_2):
         Y = β_0 + β_1 x_1 + β_2 x_2 + β_12 x_1 x_2 + ε           (60)
     Đặt x_3 = x_1 x_2 và β_3 = β_12, đưa về mô hình hồi quy tuyến tính bội 3 biến.

2. Mục 4.3.2 — Phương pháp ước lượng bình phương nhỏ nhất:
   - Với n > k quan sát (x_{i1}, ..., x_{ik}; y_i), i = 1, ..., n:
         y_i = β_0 + Σ_{j=1}^k β_j x_{ij} + ε_i                   (63)
   - Hàm bình phương nhỏ nhất:
         L = Σ_{i=1}^n ε_i^2 = Σ_{i=1}^n (y_i - β_0 - Σ_{j=1}^k β_j x_{ij})^2  (64)
   - Cực tiểu hóa L theo β_0, β_1, ..., β_k cho hệ p = k + 1 phương trình chuẩn
     bình phương nhỏ nhất (65)–(67). Giải hệ phương trình tuyến tính bằng phương
     pháp khử Gauss để tìm ước lượng bình phương nhỏ nhất (β̂_0, β̂_1, ..., β̂_k).
────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Thêm thư mục gốc vào sys.path để import stats_utils
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.stats_utils import (
    FIGURES_DIR,
    SECTIONS_DIR,
    TABLES_DIR,
    load_data,
    md_table,
    multiple_lse_normal_equations,
    simple_ols,
)

# Cấu hình font hiển thị tiếng Việt ổn định
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Times New Roman"]
plt.rcParams["axes.unicode_minus"] = False


def _fmt_term(val: float, var_str: str) -> str:
    sign = "+" if val >= 0 else "-"
    return f"{sign} {abs(val):.4f}·{var_str}"


def _fmt_term_tex(val: float, var_str: str) -> str:
    sign = "+" if val >= 0 else "-"
    return f"{sign} {abs(val):.4f} {var_str}"


def plot_plane_and_contour(
    x1: np.ndarray,
    x2: np.ndarray,
    y: np.ndarray,
    beta: np.ndarray,
    out_path: Path,
) -> None:
    """Vẽ mặt phẳng hồi quy 3D và biểu đồ đường đồng mức hai chiều (theo Hình 15, Mục 4.3.1)."""
    b0, b1, b2 = float(beta[0]), float(beta[1]), float(beta[2])

    x1_grid = np.linspace(float(np.min(x1)), float(np.max(x1)), 40)
    x2_grid = np.linspace(float(np.min(x2)), float(np.max(x2)), 40)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    Y_hat_grid = b0 + b1 * X1 + b2 * X2

    fig = plt.figure(figsize=(13.5, 5.4), dpi=200)

    # Khung trái: Mặt phẳng hồi quy trong không gian 3 chiều (Y, x1, x2)
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.scatter(x1, x2, y, s=10, alpha=0.35, color="#1f4e79", label="Quan sát thực tế")
    surf = ax1.plot_surface(
        X1, X2, Y_hat_grid, cmap="viridis", alpha=0.65, edgecolor="none"
    )
    ax1.set_xlabel("x₁: Thời lượng (giờ)", labelpad=8, fontsize=9.5)
    ax1.set_ylabel("x₂: Nhịp tim TB (nhịp/phút)", labelpad=10, fontsize=9.5)
    ax1.set_zlabel("Y: Calo (kcal)", labelpad=6, fontsize=9.5)
    ax1.set_title("Mặt phẳng hồi quy tuyến tính bội (2 biến hồi quy)", fontsize=11, fontweight="bold")
    ax1.view_init(elev=22, azim=-128)
    ax1.set_box_aspect(None, zoom=0.84)

    # Khung phải: Biểu đồ đường đồng mức (các đường thẳng có hằng số Ê(Y))
    ax2 = fig.add_subplot(1, 2, 2)
    levels = np.arange(300, 1700, 150)
    cs = ax2.contour(X1, X2, Y_hat_grid, levels=levels, cmap="viridis", linewidths=1.8)
    ax2.clabel(cs, inline=True, fontsize=9, fmt="%.0f kcal")
    ax2.scatter(x1, x2, s=8, alpha=0.18, color="#4a5568")
    ax2.set_xlabel("x₁: Thời lượng tập (giờ)")
    ax2.set_ylabel("x₂: Nhịp tim trung bình (nhịp/phút)")
    ax2.set_title("Biểu đồ đường đồng mức của Ê(Y | x₁, x₂) (đường thẳng)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.4)

    fig.suptitle(
        f"Mô hình 1 (Mục 4.3.1): ŷ = {b0:.4f} + {b1:.4f}·x₁ + {b2:.4f}·x₂",
        fontsize=12,
        fontweight="bold",
        y=0.98,
    )
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.12, wspace=0.24)
    fig.savefig(out_path, dpi=200, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def plot_interaction_surface_and_contour(
    x1: np.ndarray,
    x2: np.ndarray,
    y: np.ndarray,
    beta: np.ndarray,
    out_path: Path,
) -> None:
    """Vẽ bề mặt hồi quy 3D và đường đồng mức cho mô hình có hiệu ứng tương tác (theo Hình 16, Mục 4.3.1)."""
    b0, b1, b2, b12 = float(beta[0]), float(beta[1]), float(beta[2]), float(beta[3])

    x1_grid = np.linspace(float(np.min(x1)), float(np.max(x1)), 40)
    x2_grid = np.linspace(float(np.min(x2)), float(np.max(x2)), 40)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    Y_hat_grid = b0 + b1 * X1 + b2 * X2 + b12 * X1 * X2

    fig = plt.figure(figsize=(13.5, 5.4), dpi=200)

    # Khung trái: Bề mặt hồi quy 3D với thuật ngữ tích chéo x1·x2
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.scatter(x1, x2, y, s=10, alpha=0.35, color="#1f4e79", label="Quan sát thực tế")
    ax1.plot_surface(
        X1, X2, Y_hat_grid, cmap="plasma", alpha=0.65, edgecolor="none"
    )
    ax1.set_xlabel("x₁: Thời lượng (giờ)", labelpad=8, fontsize=9.5)
    ax1.set_ylabel("x₂: Nhịp tim TB (nhịp/phút)", labelpad=10, fontsize=9.5)
    ax1.set_zlabel("Y: Calo (kcal)", labelpad=6, fontsize=9.5)
    ax1.set_title("Bề mặt hồi quy có hiệu ứng tương tác (x₁·x₂)", fontsize=11, fontweight="bold")
    ax1.view_init(elev=22, azim=-128)
    ax1.set_box_aspect(None, zoom=0.84)

    # Khung phải: Biểu đồ đường đồng mức hai chiều (đường cong do có tương tác)
    ax2 = fig.add_subplot(1, 2, 2)
    levels = np.arange(300, 1700, 150)
    cs = ax2.contour(X1, X2, Y_hat_grid, levels=levels, cmap="plasma", linewidths=1.8)
    ax2.clabel(cs, inline=True, fontsize=9, fmt="%.0f kcal")
    ax2.scatter(x1, x2, s=8, alpha=0.18, color="#4a5568")
    ax2.set_xlabel("x₁: Thời lượng tập (giờ)")
    ax2.set_ylabel("x₂: Nhịp tim trung bình (nhịp/phút)")
    ax2.set_title("Biểu đồ đường đồng mức của Ê(Y | x₁, x₂) (đường cong tương tác)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.4)

    fig.suptitle(
        f"Mô hình 3 (Tương tác): ŷ = {b0:.4f} {_fmt_term(b1, 'x₁')} {_fmt_term(b2, 'x₂')} {_fmt_term(b12, 'x₁x₂')}",
        fontsize=12,
        fontweight="bold",
        y=0.98,
    )
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.12, wspace=0.24)
    fig.savefig(out_path, dpi=200, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def main() -> None:
    print("=" * 74)
    print("CHƯƠNG 4 (PHẦN 3): HỒI QUY TUYẾN TÍNH BỘI — MỤC 4.3.1 & 4.3.2")
    print("Phương pháp ước lượng bình phương nhỏ nhất (Hệ phương trình chuẩn)")
    print("=" * 74)

    # 1. Đọc dữ liệu
    df = load_data()
    y = df["Calories_Burned"].to_numpy(float)
    x1 = df["Session_Duration"].to_numpy(float)   # Thời lượng tập (giờ)
    x2 = df["Avg_BPM"].to_numpy(float)            # Nhịp tim trung bình (nhịp/phút)
    x3 = df["Weight (kg)"].to_numpy(float)        # Cân nặng (kg)
    x1x2 = x1 * x2                                # Thuật ngữ tích chéo tương tác
    n = y.size

    # Đối chiếu giá trị hàm bình phương nhỏ nhất L từ hồi quy tuyến tính đơn (Mục 4.1)
    m_slr = simple_ols(x1, y)
    L_slr = float(m_slr["sse"])

    # ------------------------------------------------------------------
    # MÔ HÌNH 1: Hồi quy tuyến tính bội với k = 2 biến hồi quy (55)
    # Y = β_0 + β_1·x_1 + β_2·x_2 + ε
    # ------------------------------------------------------------------
    m1 = multiple_lse_normal_equations([x1, x2], y)
    b1 = m1["beta_hat"]
    A1, rhs1 = m1["normal_A"], m1["normal_b"]

    print("\n[Mô hình 1] Y = β₀ + β₁·x₁ + β₂·x₂ + ε  (k = 2, p = 3 phương trình chuẩn)")
    print(f"  Phương trình ước lượng: ŷ = {b1[0]:.4f} + {b1[1]:.4f}·x₁ + {b1[2]:.4f}·x₂")
    print(f"  Hàm bình phương nhỏ nhất cực tiểu L = {m1['L_min']:,.2f}")
    print(f"  Kiểm chứng đạo hàm riêng max |∂L/∂βⱼ| = {m1['max_abs_grad']:.3e}")

    # Lưu hệ p = 3 phương trình chuẩn của Mô hình 1 ra CSV
    df_norm1 = pd.DataFrame(
        {
            "Phương trình chuẩn": [
                "PT 1 (∂L/∂β₀ = 0)",
                "PT 2 (∂L/∂β₁ = 0)",
                "PT 3 (∂L/∂β₂ = 0)",
            ],
            "Hệ số β̂₀": A1[:, 0],
            "Hệ số β̂₁ (x₁)": A1[:, 1],
            "Hệ số β̂₂ (x₂)": A1[:, 2],
            "Vế phải (Σ)": rhs1,
        }
    )
    df_norm1.to_csv(TABLES_DIR / "07_mlr_normal_equations_m1.csv", index=False, encoding="utf-8-sig")

    # ------------------------------------------------------------------
    # MÔ HÌNH 2: Hồi quy tuyến tính bội với k = 3 biến hồi quy (57)
    # Y = β_0 + β_1·x_1 + β_2·x_2 + β_3·x_3 + ε
    # ------------------------------------------------------------------
    m2 = multiple_lse_normal_equations([x1, x2, x3], y)
    b2 = m2["beta_hat"]

    print("\n[Mô hình 2] Y = β₀ + β₁·x₁ + β₂·x₂ + β₃·x₃ + ε  (k = 3, p = 4 phương trình chuẩn)")
    print(
        f"  Phương trình ước lượng: ŷ = {b2[0]:.4f} + {b2[1]:.4f}·x₁ "
        f"+ {b2[2]:.4f}·x₂ + {b2[3]:.4f}·x₃"
    )
    print(f"  Hàm bình phương nhỏ nhất cực tiểu L = {m2['L_min']:,.2f}")
    print(f"  Kiểm chứng đạo hàm riêng max |∂L/∂βⱼ| = {m2['max_abs_grad']:.3e}")

    # ------------------------------------------------------------------
    # MÔ HÌNH 3: Mô hình có hiệu ứng tương tác giữa x_1 và x_2 (60)
    # Y = β_0 + β_1·x_1 + β_2·x_2 + β_12·(x_1·x_2) + ε
    # Đặt x_3 = x_1·x_2 và β_3 = β_12
    # ------------------------------------------------------------------
    m3 = multiple_lse_normal_equations([x1, x2, x1x2], y)
    b3 = m3["beta_hat"]

    print("\n[Mô hình 3 - Tương tác] Y = β₀ + β₁·x₁ + β₂·x₂ + β₁₂·x₁x₂ + ε  (k = 3, p = 4)")
    print(
        f"  Phương trình ước lượng: ŷ = {b3[0]:.4f} {_fmt_term(b3[1], 'x₁')} "
        f"{_fmt_term(b3[2], 'x₂')} {_fmt_term(b3[3], 'x₁x₂')}"
    )
    print(f"  Hàm bình phương nhỏ nhất cực tiểu L = {m3['L_min']:,.2f}")
    print(f"  Kiểm chứng đạo hàm riêng max |∂L/∂βⱼ| = {m3['max_abs_grad']:.3e}")

    # Minh họa định lượng hiệu ứng tương tác (theo tinh thần Hình 16, slide 154):
    # Thay đổi x_1 từ 0.5 giờ lên 2.0 giờ tại x_2 = 120 BPM so với x_2 = 170 BPM
    def pred_m3(v_x1: float, v_x2: float) -> float:
        return float(b3[0] + b3[1] * v_x1 + b3[2] * v_x2 + b3[3] * v_x1 * v_x2)

    dy_at_120 = pred_m3(2.0, 120.0) - pred_m3(0.5, 120.0)
    dy_at_170 = pred_m3(2.0, 170.0) - pred_m3(0.5, 170.0)
    slope_x1_at_120 = float(b3[1] + b3[3] * 120.0)
    slope_x1_at_170 = float(b3[1] + b3[3] * 170.0)
    print(
        f"  Hiệu ứng tương tác: Khi tăng x₁ từ 0.5 → 2.0 giờ:\n"
        f"    • Tại x₂ = 120 nhịp/phút: ΔÊ(Y) = +{dy_at_120:.2f} kcal (tốc độ {slope_x1_at_120:.2f} kcal/giờ)\n"
        f"    • Tại x₂ = 170 nhịp/phút: ΔÊ(Y) = +{dy_at_170:.2f} kcal (tốc độ {slope_x1_at_170:.2f} kcal/giờ)"
    )

    # Lưu bảng tổng hợp các ước lượng bình phương nhỏ nhất
    coef_rows = [
        ("Mô hình 1 (2 biến)", "β̂₀ (Hệ số chặn)", b1[0], "Hệ số chặn mặt phẳng hồi quy"),
        ("Mô hình 1 (2 biến)", "β̂₁ (Session_Duration)", b1[1], "Thay đổi kỳ vọng calo khi tăng 1 giờ tập (giữ Avg_BPM không đổi)"),
        ("Mô hình 1 (2 biến)", "β̂₂ (Avg_BPM)", b1[2], "Thay đổi kỳ vọng calo khi tăng 1 nhịp/phút (giữ Session_Duration không đổi)"),
        ("Mô hình 2 (3 biến)", "β̂₀ (Hệ số chặn)", b2[0], "Hệ số chặn siêu phẳng hồi quy"),
        ("Mô hình 2 (3 biến)", "β̂₁ (Session_Duration)", b2[1], "Hệ số hồi quy riêng của Session_Duration (giữ Avg_BPM, Weight không đổi)"),
        ("Mô hình 2 (3 biến)", "β̂₂ (Avg_BPM)", b2[2], "Hệ số hồi quy riêng của Avg_BPM (giữ Session_Duration, Weight không đổi)"),
        ("Mô hình 2 (3 biến)", "β̂₃ (Weight (kg))", b2[3], "Hệ số hồi quy riêng của Weight (giữ Session_Duration, Avg_BPM không đổi)"),
        ("Mô hình 3 (Tương tác)", "β̂₀ (Hệ số chặn)", b3[0], "Hệ số chặn bề mặt hồi quy có tương tác"),
        ("Mô hình 3 (Tương tác)", "β̂₁ (Session_Duration)", b3[1], "Hệ số góc bậc nhất của Session_Duration"),
        ("Mô hình 3 (Tương tác)", "β̂₂ (Avg_BPM)", b3[2], "Hệ số góc bậc nhất của Avg_BPM"),
        ("Mô hình 3 (Tương tác)", "β̂₁₂ (x₁·x₂)", b3[3], "Hệ số thuật ngữ tích chéo (hiệu ứng tương tác giữa x₁ và x₂)"),
    ]
    df_coefs = pd.DataFrame(coef_rows, columns=["Mô hình", "Tham số", "Ước lượng bình phương nhỏ nhất", "Ý nghĩa"])
    df_coefs.to_csv(TABLES_DIR / "07_mlr_coefficients.csv", index=False, encoding="utf-8-sig")

    # Lưu bảng so sánh hàm bình phương nhỏ nhất cực tiểu L
    comp_rows = [
        ("Hồi quy đơn (Mục 4.1)", 1, 2, L_slr, 0.0, 0.0),
        (
            "Mô hình 1: x₁, x₂ (Mục 4.3)",
            2,
            3,
            m1["L_min"],
            (L_slr - m1["L_min"]) / L_slr * 100.0,
            m1["max_abs_grad"],
        ),
        (
            "Mô hình 2: x₁, x₂, x₃ (Mục 4.3)",
            3,
            4,
            m2["L_min"],
            (L_slr - m2["L_min"]) / L_slr * 100.0,
            m2["max_abs_grad"],
        ),
        (
            "Mô hình 3: x₁, x₂, x₁x₂ (Tương tác)",
            3,
            4,
            m3["L_min"],
            (L_slr - m3["L_min"]) / L_slr * 100.0,
            m3["max_abs_grad"],
        ),
    ]
    df_comp = pd.DataFrame(
        comp_rows,
        columns=[
            "Mô hình",
            "Số biến hồi quy (k)",
            "Số PT chuẩn (p = k+1)",
            "Hàm bình phương nhỏ nhất L",
            "Mức giảm L so với hồi quy đơn (%)",
            "Sai số đạo hàm riêng max |∂L/∂βⱼ|",
        ],
    )
    df_comp.to_csv(TABLES_DIR / "07_mlr_comparison_L.csv", index=False, encoding="utf-8-sig")

    # 2. Vẽ 2 biểu đồ mặt phẳng / bề mặt 3D và đường đồng mức (theo Hình 15 & Hình 16)
    fig1_path = FIGURES_DIR / "07_mlr_plane_contour.png"
    fig2_path = FIGURES_DIR / "07_mlr_interaction_surface.png"
    plot_plane_and_contour(x1, x2, y, b1, fig1_path)
    plot_interaction_surface_and_contour(x1, x2, y, b3, fig2_path)
    print(f"\nĐã lưu biểu đồ:\n  - {fig1_path}\n  - {fig2_path}")

    # 3. Xuất phần báo cáo Markdown (report/sections/07_chap4_mlr_lse.md)
    md_lines = [
        "# Chương 4 (phần 3): Hồi quy tuyến tính bội (Mục 4.3.1 và 4.3.2)",
        "",
        "## 1. Giới thiệu về mô hình hồi quy tuyến tính bội (Mục 4.3.1)",
        "",
        "Trong hồi quy tuyến tính đơn (Mục 4.1), mô hình chỉ xét một biến độc lập $x$ (`Session_Duration`), dễ dẫn đến vi phạm giả thiết về sai số ngẫu nhiên khi các yếu tố khác cũng tác động đến biến phụ thuộc $Y$ (`Calories_Burned`). Mô hình hồi quy tuyến tính bội tổng quát với $k$ biến độc lập (biến hồi quy, biến giải thích) $x_1, x_2, \\dots, x_k$ có dạng:",
        "",
        "$$Y = \\beta_0 + \\sum_{j=1}^{k} \\beta_j x_j + \\varepsilon$$",
        "",
        "trong đó $\\beta_0$ là **hệ số chặn**, $\\beta_1, \\dots, \\beta_k$ là **các hệ số góc** chưa biết (còn gọi là **các hệ số hồi quy riêng** hay **các hệ số hồi quy lý thuyết**), và $\\varepsilon$ là **sai số ngẫu nhiên** đại diện cho các yếu tố ngoài $x_1, \\dots, x_k$ có tác động đến $Y$ nhưng chưa đưa vào mô hình.",
        "",
        "Với giả thiết $E(\\varepsilon) = 0$, **hàm hồi quy tuyến tính lý thuyết** của $Y$ theo $k$ biến giải thích là:",
        "",
        "$$E(Y \\mid x_1, \\dots, x_k) = \\beta_0 + \\sum_{j=1}^{k} \\beta_j x_j$$",
        "",
        "Trong mô hình bội, hệ số hồi quy riêng $\\beta_j$ biểu thị sự thay đổi kỳ vọng (dự kiến) của biến phản hồi $Y$ trên mỗi đơn vị thay đổi của $x_j$ khi tất cả các biến hồi quy còn lại $x_i$ ($i \\ne j$) được giữ không đổi. Ngoài ra, mô hình có **hiệu ứng tương tác** giữa hai biến $x_1, x_2$ biểu diễn bởi thuật ngữ tích chéo $x_1 x_2$:",
        "",
        "$$Y = \\beta_0 + \\beta_1 x_1 + \\beta_2 x_2 + \\beta_{12} x_1 x_2 + \\varepsilon$$",
        "",
        "vẫn là một mô hình hồi quy tuyến tính bội (khi đặt $x_3 = x_1 x_2$ và $\\beta_3 = \\beta_{12}$) vì tuyến tính theo các tham số $\\beta$.",
        "",
        "## 2. Phương pháp ước lượng bình phương nhỏ nhất (Mục 4.3.2)",
        "",
        f"Với $k$ biến hồi quy và $n = {n} > k$ quan sát $(x_{{i1}}, x_{{i2}}, \\dots, x_{{ik}}; y_i)$, mỗi quan sát thỏa mãn $y_i = \\beta_0 + \\sum_{{j=1}}^k \\beta_j x_{{ij}} + \\varepsilon_i$. **Hàm bình phương nhỏ nhất** là:",
        "",
        "$$L = \\sum_{i=1}^{n} \\varepsilon_i^2 = \\sum_{i=1}^{n} \\left( y_i - \\beta_0 - \\sum_{j=1}^{k} \\beta_j x_{ij} \\right)^2$$",
        "",
        "Lấy đạo hàm riêng của $L$ theo $\\beta_0, \\beta_1, \\dots, \\beta_k$ và đặt bằng $0$ thu được hệ $p = k + 1$ **phương trình chuẩn bình phương nhỏ nhất**:",
        "",
        "$$\\begin{cases} n\\hat{\\beta}_0 + \\hat{\\beta}_1 \\sum_{i=1}^n x_{i1} + \\dots + \\hat{\\beta}_k \\sum_{i=1}^n x_{ik} = \\sum_{i=1}^n y_i \\\\ \\hat{\\beta}_0 \\sum_{i=1}^n x_{ij} + \\hat{\\beta}_1 \\sum_{i=1}^n x_{ij} x_{i1} + \\dots + \\hat{\\beta}_k \\sum_{i=1}^n x_{ij} x_{ik} = \\sum_{i=1}^n x_{ij} y_i, \\quad j = 1, \\dots, k \\end{cases}$$",
        "",
        "Nghiệm $(\\hat{\\beta}_0, \\hat{\\beta}_1, \\dots, \\hat{\\beta}_k)$ của hệ phương trình chuẩn (giải bằng phương pháp khử Gauss) là các **ước lượng bình phương nhỏ nhất** của hệ số hồi quy.",
        "",
        "## 3. Kết quả thực nghiệm trên dữ liệu phòng gym ($n = 973$)",
        "",
        "### 3.1. Hệ phương trình chuẩn bình phương nhỏ nhất của Mô hình 1 ($k = 2$, $p = 3$)",
        "",
        "Xét $Y$: `Calories_Burned` (kcal), $x_1$: `Session_Duration` (giờ), $x_2$: `Avg_BPM` (nhịp/phút).",
        "",
        md_table(df_norm1, nd=4),
        "",
        f"Giải hệ 3 phương trình chuẩn trên cho phương trình mặt phẳng hồi quy ước lượng:",
        f"$$\\hat{{y}} = {b1[0]:.4f} + {b1[1]:.4f} x_1 + {b1[2]:.4f} x_2$$",
        "",
        "### 3.2. Tổng hợp ước lượng bình phương nhỏ nhất cho các mô hình",
        "",
        md_table(df_coefs, nd=4),
        "",
        "### 3.3. So sánh giá trị cực tiểu hàm bình phương nhỏ nhất $L$",
        "",
        md_table(df_comp, nd=4),
        "",
        "### 3.4. Minh họa hiệu ứng tương tác giữa thời lượng tập và nhịp tim trung bình",
        "",
        f"Với Mô hình 3 ($\\hat{{y}} = {b3[0]:.4f} {_fmt_term_tex(b3[1], 'x_1')} {_fmt_term_tex(b3[2], 'x_2')} {_fmt_term_tex(b3[3], 'x_1 x_2')}$):",
        f"- Khi giữ nhịp tim ở mức thấp $x_2 = 120$ nhịp/phút, tăng thời lượng tập $x_1$ từ $0.5$ lên $2.0$ giờ làm lượng calo kỳ vọng tăng thêm **+{dy_at_120:.2f} kcal** (tốc độ {slope_x1_at_120:.2f} kcal/giờ).",
        f"- Khi giữ nhịp tim ở mức cao $x_2 = 170$ nhịp/phút, cùng mức tăng $x_1$ từ $0.5$ lên $2.0$ giờ làm lượng calo kỳ vọng tăng thêm **+{dy_at_170:.2f} kcal** (tốc độ {slope_x1_at_170:.2f} kcal/giờ).",
        "- Điều này thể hiện rõ bản chất **hiệu ứng tương tác**: tác động của việc thay đổi $x_1$ phụ thuộc vào mức độ của biến $x_2$, và các đường đồng mức trên mặt phẳng $(x_1, x_2)$ bị uốn cong thay vì là đường thẳng.",
        "",
        "## 4. Đồ thị mặt phẳng, bề mặt hồi quy và đường đồng mức",
        "",
        "![Mặt phẳng hồi quy và đường đồng mức Mô hình 1](../../outputs/figures/07_mlr_plane_contour.png)",
        "",
        "![Bề mặt hồi quy có tương tác và đường đồng mức Mô hình 3](../../outputs/figures/07_mlr_interaction_surface.png)",
        "",
    ]

    md_path = SECTIONS_DIR / "07_chap4_mlr_lse.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Đã xuất báo cáo Markdown: {md_path}")
    print("=" * 74)


if __name__ == "__main__":
    main()
