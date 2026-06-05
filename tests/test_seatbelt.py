"""
Test nhanh chức năng Seatbelt Detection.

Cách chạy (từ thư mục gốc CoreAI_doAN/):
    python tests/test_seatbelt.py
    python tests/test_seatbelt.py --image data/driver_images/ten_anh.jpg
"""

import sys
import os
import argparse
import cv2

# Để import được src/ từ thư mục gốc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.modules.detection.seatbelt_detector import SeatbeltDetector
from src.modules.cabin_monitor.seatbelt_checker import SeatbeltChecker


def test_detector_raw(image_path: str):
    """Test SeatbeltDetector.detect_raw() — quét toàn bộ ảnh, không cần bbox người."""
    print("\n=== TEST 1: SeatbeltDetector.detect_raw() ===")

    detector = SeatbeltDetector()
    img = cv2.imread(image_path)

    if img is None:
        print(f"[LỖI] Không đọc được ảnh: {image_path}")
        return

    results = detector.detect_raw(img)

    if not results:
        print("→ Không detect được gì trong ảnh.")
    else:
        for i, r in enumerate(results):
            status = "✅ Đeo dây" if r["has_seatbelt"] else "❌ Không đeo dây"
            print(f"  [{i+1}] {status}  |  class: {r['class_name']}  |  conf: {r['confidence']}  |  bbox: {r['bbox']}")


def test_checker_with_bbox(image_path: str, person_bbox: list):
    """Test SeatbeltChecker.check() — giả lập pipeline gọi với bbox người."""
    print("\n=== TEST 2: SeatbeltChecker.check() với person_bbox ===")

    checker = SeatbeltChecker()
    img = cv2.imread(image_path)

    if img is None:
        print(f"[LỖI] Không đọc được ảnh: {image_path}")
        return

    result = checker.check(img, person_bbox)

    status = "✅ Đeo dây" if result["has_seatbelt"] else "❌ Không đeo dây"
    print(f"  Kết quả: {status}")
    print(f"  Chi tiết: {result}")


def find_test_image() -> str | None:
    """Tự tìm 1 ảnh bất kỳ trong data/driver_images/ để test."""
    folder = "data/driver_images"
    if not os.path.exists(folder):
        return None
    for f in os.listdir(folder):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            return os.path.join(folder, f)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Seatbelt Detector")
    parser.add_argument("--image", type=str, default=None, help="Đường dẫn ảnh test")
    args = parser.parse_args()

    # Chọn ảnh test
    image_path = args.image or find_test_image()

    if image_path is None:
        print("[LỖI] Không tìm thấy ảnh nào trong data/driver_images/")
        print("       Hãy bỏ ảnh vào đó hoặc dùng:")
        print("       python tests/test_seatbelt.py --image path/to/anh.jpg")
        sys.exit(1)

    print(f"Dùng ảnh: {image_path}")

    # Test 1: Quét toàn ảnh (không cần bbox)
    test_detector_raw(image_path)

    # Test 2: Giả lập pipeline gọi với bbox = cả ảnh
    img_check = cv2.imread(image_path)
    h, w = img_check.shape[:2]
    full_bbox = [0, 0, w, h]
    test_checker_with_bbox(image_path, full_bbox)
