import cv2
import sys
import os
import time

# Thêm thư mục gốc vào sys.path để import được src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultralytics import YOLO
from src.modules.detection.seatbelt_detector import SeatbeltDetector
from src.config import settings

def main():
    # ── Load models ───────────────────────────────────────────
    print("[INFO] Khởi tạo models...")
    try:
        # Model detect người (YOLOv8n COCO — class 0 = person)
        person_model   = YOLO("yolov8n.pt")
        # Model detect dây an toàn
        seatbelt_det   = SeatbeltDetector(
            model_path=settings.YOLO_SEATBELT_MODEL,
            confidence=settings.SEATBELT_CONFIDENCE
        )
    except Exception as e:
        print(f"[LỖI] Không thể khởi tạo model: {e}")
        return

    print("[INFO] Đang mở webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[LỖI] Không thể kết nối với webcam.")
        return

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    print("\n[HƯỚNG DẪN]")
    print("- Pipeline: Detect người → Crop bbox → Detect seatbelt (giống pipeline thật)")
    print("- Bấm 'q' để thoát.\n")

    INFER_EVERY_N  = 3
    INFER_SIZE     = 640
    frame_count    = 0
    last_persons   = []   # list of [x1,y1,x2,y2] person bboxes
    last_seatbelts = []   # list of seatbelt result dicts (1 per person)
    fps_timer      = time.time()
    fps_frames     = 0
    fps            = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[LỖI] Lỗi khi đọc frame từ camera.")
            break

        frame = cv2.flip(frame, 1)
        frame_count += 1
        fps_frames  += 1

        # ── Inference mỗi N frame ────────────────────────────
        if frame_count % INFER_EVERY_N == 0:
            h, w   = frame.shape[:2]
            scale  = INFER_SIZE / w
            small  = cv2.resize(frame, (INFER_SIZE, int(h * scale)))

            # BƯỚC 1: Detect người
            p_results    = person_model(small, classes=[0], conf=0.4, verbose=False)
            last_persons = []
            for r in p_results:
                for box in r.boxes:
                    px1, py1, px2, py2 = [int(v / scale) for v in box.xyxy[0]]
                    last_persons.append([px1, py1, px2, py2])

            # BƯỚC 2: Với mỗi người → detect seatbelt trên crop bbox
            last_seatbelts = []
            for pbbox in last_persons:
                result = seatbelt_det.detect(frame, pbbox)
                last_seatbelts.append((pbbox, result))

        # ── Vẽ kết quả ───────────────────────────────────────
        for pbbox, sb_result in last_seatbelts:
            px1, py1, px2, py2 = pbbox

            # Khung người — màu xanh dương
            cv2.rectangle(frame, (px1, py1), (px2, py2), (255, 150, 0), 1)

            # Kết quả seatbelt
            if sb_result['bbox'] is not None:
                sx1, sy1, sx2, sy2 = sb_result['bbox']
                color = (0, 200, 0) if sb_result['has_seatbelt'] else (0, 0, 220)
                label = f"{sb_result['class_name']}: {sb_result['confidence']:.2f}"

                cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), color, 2)
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (sx1, sy1 - 25), (sx1 + tw + 4, sy1), color, -1)
                cv2.putText(frame, label, (sx1 + 2, sy1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            else:
                # Không detect được gì trong bbox người
                cv2.putText(frame, "? no detect", (px1, py1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)

        # Nếu không thấy người nào
        if not last_persons:
            cv2.putText(frame, "Khong thay nguoi", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

        # ── FPS ──────────────────────────────────────────────
        elapsed = time.time() - fps_timer
        if elapsed >= 1.0:
            fps        = fps_frames / elapsed
            fps_timer  = time.time()
            fps_frames = 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.imshow("Test Webcam - Pipeline (Person → Seatbelt)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Đã nhận lệnh thoát.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

