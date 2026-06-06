"""
Test Person Detector - Chạy realtime qua webcam
Nhấn Q để thoát
"""

import sys
import cv2
from pathlib import Path

# Thêm thư mục gốc project vào path để import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modules.detection.person_detector import PersonDetector


def main():
    print("[INFO] Đang khởi tạo PersonDetector...")
    detector = PersonDetector()
    print("[INFO] Load model xong! Mở webcam...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Không mở được webcam!")
        return

    print("[INFO] Webcam OK. Nhấn Q để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Không đọc được frame!")
            break

        # --- Detect người ---
        detections = detector.detect(frame)

        # --- Vẽ kết quả lên frame ---
        for d in detections:
            x1, y1, x2, y2 = map(int, d.bbox)
            conf = d.confidence

            # Vẽ bounding box màu xanh lá
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Nhãn confidence
            label = f"person {conf:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            # Nền nhãn
            cv2.rectangle(frame,
                          (x1, y1 - label_size[1] - 8),
                          (x1 + label_size[0] + 4, y1),
                          (0, 255, 0), -1)
            # Chữ nhãn
            cv2.putText(frame, label, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # --- Hiển thị số người detect được ---
        count_text = f"Persons detected: {len(detections)}"
        cv2.putText(frame, count_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.imshow("Person Detection Test - Nhan Q de thoat", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Đã dừng.")


if __name__ == "__main__":
    main()
