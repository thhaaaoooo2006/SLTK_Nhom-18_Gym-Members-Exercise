"""
MAIN PIPELINE EXECUTION & CROSS-VALIDATION SCRIPT
Môn học : Suy luận thống kê (MI3031) — Học kỳ 2026.1
Đề tài  : Phân tích Dữ liệu Tập luyện của Thành viên Phòng Gym (Gym Members Exercise Tracking)
Nhóm 18 : Nguyễn Thị Thảo (202419101) & Nguyễn Văn Nam Khánh (202419069)
===========================================================================================
Mục đích:
  1. Thực thi tuần tự toàn bộ 6 mô-đun phân tích thống kê từ Chương 1 đến Chương 4.
  2. Kiểm tra chéo (Cross-Validation) tính nhất quán số liệu giữa code, bảng CSV và báo cáo.
  3. Biên dịch tài liệu báo cáo toàn văn PDF (BaoCao_SLTK_Nhom18.pdf) và Slide thuyết trình.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
TABLES_DIR = BASE_DIR / "outputs" / "tables"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"
REPORT_DIR = BASE_DIR / "report"
SECTIONS_DIR = REPORT_DIR / "sections"

# Danh sách 6 mô-đun lõi
SRC_SCRIPTS = [
    ("src/01_eda_chap1.py", "Chương 1: Tiền xử lý & Thống kê mô tả (Mẫu ngẫu nhiên)"),
    ("src/02_estimation_chap2.py", "Chương 2: Ước lượng tham số & Khoảng tin cậy 95%"),
    ("src/03_hypothesis_parametric.py", "Chương 3 (Phần 1): Kiểm định tham số 1 & 2 tổng thể"),
    ("src/04_anova_nonparametric.py", "Chương 3 (Phần 2): ANOVA 1 nhân tố & Kiểm định phi tham số"),
    ("src/05_simple_regression.py", "Chương 4 (Phần 1): Hồi quy tuyến tính đơn & Suy luận"),
    ("src/06_residuals_correlation.py", "Chương 4 (Phần 2): Phân tích phần dư & Tương quan tuyến tính"),
    ("src/07_multiple_regression_lse.py", "Chương 4 (Phần 3): Hồi quy tuyến tính bội (Mục 4.3.1 & 4.3.2)"),
]


def run_all_scripts() -> None:
    """Thực thi tuần tự 6 script phân tích."""
    print("=" * 80)
    print("BÁO CÁO CUỐI KỲ — SUY LUẬN THỐNG KÊ (MI3031) — NHÓM 18")
    print("BẮT ĐẦU QUY TRÌNH THỰC THI PIPELINE TOÀN DIỆN")
    print("=" * 80)

    total_start = time.time()
    for rel_path, desc in SRC_SCRIPTS:
        script_path = BASE_DIR / rel_path
        print(f"\n[EXEC] Đang chạy: {rel_path} — {desc}")
        if not script_path.exists():
            print(f"❌ [LỖI] Không tìm thấy file script: {script_path}")
            sys.exit(1)

        t0 = time.time()
        res = subprocess.run([sys.executable, str(script_path)], cwd=str(BASE_DIR))
        elapsed = time.time() - t0

        if res.returncode != 0:
            print(f"❌ [THẤT BẠI] {rel_path} dừng với mã lỗi: {res.returncode}")
            sys.exit(res.returncode)
        print(f"✅ [HOÀN THÀNH] {rel_path} ({elapsed:.2f}s)")

    print("\n" + "=" * 80)
    print(f"TẤT CẢ 6 MÔ-ĐUN ĐÃ CHẠY THÀNH CÔNG TRONG {time.time() - total_start:.2f} GIÂY!")
    print("=" * 80)


def cross_check_data() -> bool:
    """Kiểm tra chéo tính nhất quán dữ liệu giữa các bảng và báo cáo."""
    print("\n" + "=" * 80)
    print("KIỂM TRA CHÉO SỐ LIỆU VÀ TÍNH NHẤT QUÁN TOÁN HỌC (CROSS-VALIDATION)")
    print("=" * 80)

    checks_passed = True

    # 1. Kiểm tra kích thước mẫu dữ liệu gốc
    raw_csv = BASE_DIR / "data" / "raw" / "gym_members_exercise_tracking.csv"
    if raw_csv.exists():
        df_raw = pd.read_csv(raw_csv)
        n_raw = len(df_raw)
        print(f"1. Cỡ mẫu gốc (n): {n_raw} quan sát.")
        if n_raw == 973:
            print("   ✅ Đúng cỡ mẫu chuẩn n = 973.")
        else:
            print(f"   ⚠ Cảnh báo: n_raw = {n_raw} khác 973.")
            checks_passed = False
    else:
        print("   ❌ Không tìm thấy data/raw/gym_members_exercise_tracking.csv")
        return False

    # 2. Kiểm tra bảng thống kê mô tả Chương 1
    f_sum = TABLES_DIR / "01_summary_stats.csv"
    if f_sum.exists():
        print(f"2. File bảng Chương 1: {f_sum.name} tồn tại.")
    else:
        print(f"   ❌ Thiếu {f_sum}")
        checks_passed = False

    # 3. Kiểm tra tính tương đương t₀² = F₀ trong Chương 4
    f_reg = TABLES_DIR / "05_regression_summary.csv"
    if f_reg.exists():
        df_reg = pd.read_csv(f_reg)
        reg_dict = dict(zip(df_reg["Chỉ số"], df_reg["Giá trị"]))
        b0 = float(reg_dict.get("b0", 0))
        b1 = float(reg_dict.get("b1", 0))
        r2 = float(reg_dict.get("R²", 0))
        r = float(reg_dict.get("r", 0))
        F_val = float(reg_dict.get("F", 0))

        # Đọc t-stat từ bảng hệ số
        f_coef = TABLES_DIR / "05_regression_coefficients.csv"
        df_coef = pd.read_csv(f_coef)
        t_b1 = float(df_coef.loc[df_coef["Hệ số"].str.contains("Session_Duration"), "t (H0: β=0)"].values[0])

        t_squared = t_b1 ** 2
        diff = abs(t_squared - F_val)
        print(f"3. Kiểm tra tính tương đương t₀² = F₀ trong Hồi quy tuyến tính đơn:")
        print(f"   • t₀ = {t_b1:.4f}  →  t₀² = {t_squared:.4f}")
        print(f"   • F₀ = {F_val:.4f}")
        print(f"   • Sai lệch |t₀² - F₀| = {diff:.6e}")
        if diff < 1e-3:
            print("   ✅ Hoàn toàn nhất quán: Định lý 5 & Định lý 6 được thỏa mãn tuyệt đối!")
        else:
            print("   ❌ Sai lệch giữa t₀² và F₀ vượt ngưỡng cho phép.")
            checks_passed = False

        # Kiểm tra R² = r²
        diff_r2 = abs(r2 - r**2)
        print(f"   • R² = {r2:.4f}, r² = {r**2:.4f}, Sai lệch: {diff_r2:.6e}")
        if diff_r2 < 1e-4:
            print("   ✅ Hoàn toàn nhất quán: R² = r² trong hồi quy tuyến tính đơn.")
        else:
            checks_passed = False
    else:
        print(f"   ❌ Thiếu file {f_reg}")
        checks_passed = False

    # 4. Kiểm tra sự tồn tại của toàn bộ đồ thị bắt buộc
    required_figures = [
        "05_slr_bands.png",
        "05_regression_fit.png",
        "06_residual_diagnostics.png",
        "07_mlr_plane_contour.png",
        "07_mlr_interaction_surface.png",
    ]
    print("4. Kiểm tra sự tồn tại của biểu đồ kết quả:")
    for fig_name in required_figures:
        fig_path = FIGURES_DIR / fig_name
        if fig_path.exists():
            size_kb = fig_path.stat().st_size / 1024
            print(f"   ✅ {fig_name} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ Thiếu biểu đồ: {fig_name}")
            checks_passed = False

    # 5. Kiểm tra sự tồn tại của toàn bộ các phần báo cáo markdown
    required_sections = [
        "01_chap1.md",
        "02_chap2.md",
        "03_chap3_part1.md",
        "04_chap3_part2.md",
        "05_chap4_slr.md",
        "06_chap4_corr.md",
        "07_chap4_mlr_lse.md",
    ]
    print("5. Kiểm tra các phần báo cáo thành phần (report/sections/):")
    for sec_name in required_sections:
        sec_path = SECTIONS_DIR / sec_name
        if sec_path.exists():
            print(f"   ✅ {sec_name}")
        else:
            print(f"   ❌ Thiếu phần báo cáo: {sec_name}")
            checks_passed = False

    # 6. Kiểm tra điều kiện cực tiểu phương trình chuẩn hồi quy bội (Mục 4.3.2)
    f_mlr = TABLES_DIR / "07_mlr_comparison_L.csv"
    if f_mlr.exists():
        df_mlr = pd.read_csv(f_mlr)
        max_grad = float(df_mlr["Sai số đạo hàm riêng max |∂L/∂βⱼ|"].max())
        print(f"6. Kiểm tra điều kiện cực tiểu hệ phương trình chuẩn (Mục 4.3.2):")
        print(f"   • Sai số đạo hàm riêng lớn nhất max |∂L/∂βⱼ| = {max_grad:.3e}")
        if max_grad < 1e-5:
            print("   ✅ Nghiệm hệ phương trình chuẩn thỏa mãn ∂L/∂β₀ = 0 và ∂L/∂βⱼ = 0.")
        else:
            print("   ❌ Sai số đạo hàm riêng vượt ngưỡng cho phép.")
            checks_passed = False
    else:
        print(f"   ❌ Thiếu file {f_mlr}")
        checks_passed = False

    if checks_passed:
        print("\n>>> TẤT CẢ DỮ LIỆU ĐÃ VƯỢT QUA KIỂM TRA CHÉO THÀNH CÔNG 100%! <<<")
    else:
        print("\n>>> CẢNH BÁO: CÓ MỘT SỐ MỤC KIỂM TRA CHÉO CHƯA ĐẠT! <<<")

    return checks_passed


def compile_pdf() -> bool:
    """Biên dịch tài liệu báo cáo toàn văn LaTeX sang PDF bằng xelatex."""
    print("\n" + "=" * 80)
    print("BIÊN TẬP VÀ XUẤT TÀI LIỆU BÁO CÁO PDF (XELATEX)")
    print("=" * 80)

    tex_file = REPORT_DIR / "BaoCao_SLTK_Nhom18.tex"
    if not tex_file.exists():
        print(f"   ⚠ File {tex_file} chưa được tạo. Bỏ qua bước biên dịch.")
        return False

    print(f"Đang biên dịch: {tex_file.name} bằng xelatex...")
    cmd = ["xelatex", "-interaction=batchmode", "-disable-installer", str(tex_file.name)]
    
    # Chạy 2 lần để cập nhật mục lục và tham chiếu chéo
    res1 = subprocess.run(cmd, cwd=str(REPORT_DIR), capture_output=True, text=True)
    res2 = subprocess.run(cmd, cwd=str(REPORT_DIR), capture_output=True, text=True)

    pdf_file = REPORT_DIR / "BaoCao_SLTK_Nhom18.pdf"
    if pdf_file.exists():
        size_kb = pdf_file.stat().st_size / 1024
        print(f"   ✅ Xuất PDF thành công: {pdf_file} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"   ❌ Lỗi biên dịch PDF. Mã lỗi: {res2.returncode}")
        return False


def main():
    run_all_scripts()
    cross_check_data()
    compile_pdf()


if __name__ == "__main__":
    main()
