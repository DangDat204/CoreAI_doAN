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


def test_detector_raw(image_paths: list[str]):
    """Test SeatbeltDetector.detect_raw() — quét toàn bộ ảnh, không cần bbox người."""
    print("\n=== TEST 1: SeatbeltDetector.detect_raw() ===")

    detector = SeatbeltDetector()

    for path in image_paths:
        print(f"\n[Ảnh]: {os.path.basename(path)}")
        img = cv2.imread(path)
        if img is None:
            print(f"  [LỖI] Không đọc được ảnh.")
            continue

        results = detector.detect_raw(img)

        if not results:
            print("  → Không detect được gì trong ảnh.")
        else:
            for i, r in enumerate(results):
                status = "✅ Đeo dây" if r["has_seatbelt"] else "❌ Không đeo dây"
                print(f"    [{i+1}] {status}  |  class: {r['class_name']}  |  conf: {r['confidence']}  |  bbox: {r['bbox']}")


def test_checker_with_bbox(image_paths: list[str]):
    """Test SeatbeltChecker.check() — giả lập pipeline gọi với bbox người."""
    print("\n=== TEST 2: SeatbeltChecker.check() với person_bbox ===")

    checker = SeatbeltChecker()
    for path in image_paths:
        print(f"\n[Ảnh]: {os.path.basename(path)}")
        img = cv2.imread(path)
        if img is None:
            print(f"  [LỖI] Không đọc được ảnh.")
            continue
            
        # Giả lập bbox bao trọn cả ảnh vì ta đang dùng ảnh raw
        h, w = img.shape[:2]
        full_bbox = [0, 0, w, h]

        result = checker.check(img, full_bbox)

        status = "✅ Đeo dây" if result["has_seatbelt"] else "❌ Không đeo dây"
        print(f"    Kết quả: {status}")
        print(f"    Chi tiết: {result}")


def find_test_images() -> list[str]:
    folder = "data/driver_images"

    if not os.path.exists(folder):
        return []

    # Quét tất cả ảnh jpg, jpeg, png
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    # Sắp xếp tự nhiên (numerical sort) để 10.png đứng sau 9.jpg thay vì đứng sau 1.png
    def extract_number(filename):
        name = os.path.splitext(filename)[0]
        if name.isdigit():
            return (0, int(name))
        return (1, name)

    files.sort(key=extract_number)

    return [os.path.join(folder, f) for f in files]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Seatbelt Detector")
    parser.add_argument("--image", type=str, default=None, help="Đường dẫn ảnh test")
    args = parser.parse_args()

    # Chọn ảnh test
    if args.image:
        image_paths = [args.image]
    else:
        image_paths = find_test_images() 

    if not image_paths:
        print("[LỖI] Không tìm thấy ảnh nào trong data/driver_images/")
        print("       Hãy bỏ ảnh vào đó hoặc dùng:")
        print("       python tests/test_seatbelt.py --image path/to/anh.jpg")
        sys.exit(1)

    print(f"Dùng {len(image_paths)} ảnh để test.")

    # Test 1: Quét toàn ảnh (không cần bbox)
    test_detector_raw(image_paths)

    # Test 2: Giả lập pipeline gọi với bbox = cả ảnh
    test_checker_with_bbox(image_paths)
