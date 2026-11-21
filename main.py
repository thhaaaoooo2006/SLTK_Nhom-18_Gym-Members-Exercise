"""
Main pipeline execution script for MI3031 - Group 18 Final Report
Project: Gym Members Exercise Tracking Analysis
"""

import subprocess
import sys
from pathlib import Path

# Danh sách các script thực thi tuần tự theo tiến trình nghiên cứu
SRC_SCRIPTS = [
    "01_eda_chap1.py",
    "02_estimation_chap2.py",
    "03_hypothesis_parametric.py",
    "04_anova_nonparametric.py",
    "05_simple_regression.py",
    "06_residuals_correlation.py",
]


def run_pipeline() -> None:
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src"

    print("=" * 70)
    print("BÁO CÁO CUỐI KỲ — SUY LUẬN THỐNG KÊ (MI3031) — NHÓM 18")
    print("Bắt đầu thực thi tuần tự toàn bộ pipeline phân tích dữ liệu...")
    print("=" * 70)

    for script_name in SRC_SCRIPTS:
        script_path = src_dir / script_name
        print(f"\n[EXEC] Đang chạy: src/{script_name}...")

        if not script_path.exists():
            print(f"[ERROR] Không tìm thấy file: {script_path}")
            sys.exit(1)

        result = subprocess.run([sys.executable, str(script_path)], cwd=str(base_dir))
        if result.returncode != 0:
            print(f"[FAIL] Script src/{script_name} dừng với mã lỗi: {result.returncode}")
            sys.exit(result.returncode)

        print(f"[DONE] Hoàn thành: src/{script_name}")

    print("\n" + "=" * 70)
    print("HOÀN THÀNH TOÀN BỘ QUY TRÌNH PHÂN TÍCH THÀNH CÔNG!")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
