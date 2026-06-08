"""
Script train lại model seatbelt detection với dataset mới.

Hướng dẫn sử dụng:
1. Tải dataset mới từ Roboflow (format: YOLOv8 PyTorch)
2. Giải nén vào thư mục data/
3. Cập nhật DATA_YAML bên dưới
4. Chạy script này

Khuyến nghị dataset:
- https://universe.roboflow.com/traffic-violations/seatbelt-detection-esut6
- https://universe.roboflow.com/recommendationsystemlivecamerafeed/seatbelt-detection-4plfy
"""

import os
from pathlib import Path
from ultralytics import YOLO

# ============================================================
# CẤU HÌNH — Chỉnh sửa các giá trị này
# ============================================================

# Đường dẫn tới file data.yaml của dataset MỚI
DATA_YAML = "data/seatbelt-detection.v4i.yolov8/data.yaml"

# Chọn 1 trong 2 chế độ:
# - "finetune": Fine-tune từ model cũ (nhanh hơn, ~20-30 epochs)
# - "scratch":  Train mới từ YOLOv8 pretrained (chậm hơn, ~100 epochs)
MODE = "finetune"

# Model cũ (dùng khi MODE = "finetune")
EXISTING_MODEL = "weights/yolo/seatbelt.pt"

# Base model cho train mới (dùng khi MODE = "scratch")
# Chọn: yolov8n.pt (nhỏ/nhanh) | yolov8s.pt | yolov8m.pt (chính xác hơn)
BASE_MODEL = "yolov8n.pt"

# ============================================================
# HYPERPARAMETERS
# ============================================================

EPOCHS      = 50      # Finetune: 30-50 | Train mới: 100-150
IMGSZ       = 640     # Kích thước ảnh train
BATCH       = 16      # Giảm xuống 8 nếu bị lỗi RAM/VRAM
LR0         = 0.001   # Learning rate ban đầu (finetune nên nhỏ)
PATIENCE    = 15      # Early stopping: dừng nếu sau N epochs không cải thiện
DEVICE      = 0       # 0 = GPU đầu tiên | "cpu" = dùng CPU

# Thư mục lưu kết quả train
OUTPUT_DIR  = "runs/train"
RUN_NAME    = "seatbelt_v2"

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print(f"  Chế độ: {MODE.upper()}")
    print(f"  Dataset: {DATA_YAML}")
    print(f"  Epochs:  {EPOCHS}")
    print("=" * 60)

    # Kiểm tra file data.yaml tồn tại
    if not os.path.exists(DATA_YAML):
        print(f"\n[LỖI] Không tìm thấy: {DATA_YAML}")
        print("  → Hãy tải dataset từ Roboflow và giải nén vào thư mục data/")
        print("  → Cập nhật biến DATA_YAML trong script này")
        return

    # Load model
    if MODE == "finetune":
        if not os.path.exists(EXISTING_MODEL):
            print(f"\n[LỖI] Không tìm thấy model cũ: {EXISTING_MODEL}")
            print("  → Đổi MODE = 'scratch' để train từ đầu")
            return
        print(f"\n[INFO] Fine-tuning từ: {EXISTING_MODEL}")
        model = YOLO(EXISTING_MODEL)
    else:
        print(f"\n[INFO] Train mới từ: {BASE_MODEL}")
        model = YOLO(BASE_MODEL)

    # Bắt đầu train
    print(f"[INFO] Bắt đầu training... Kết quả sẽ lưu vào: {OUTPUT_DIR}/{RUN_NAME}\n")
    
    results = model.train(
        data      = DATA_YAML,
        epochs    = EPOCHS,
        imgsz     = IMGSZ,
        batch     = BATCH,
        lr0       = LR0,
        patience  = PATIENCE,
        device    = DEVICE,
        project   = OUTPUT_DIR,
        name      = RUN_NAME,
        exist_ok  = True,

        # Augmentation để model robust hơn với webcam thực tế
        hsv_h     = 0.015,   # Thay đổi Hue   (giúp chịu được ánh sáng khác nhau)
        hsv_s     = 0.7,     # Thay đổi Saturation
        hsv_v     = 0.4,     # Thay đổi Brightness (quan trọng cho webcam tối)
        degrees   = 5.0,     # Xoay nhẹ
        flipud    = 0.0,     # Không lật dọc (xe không lộn ngược)
        fliplr    = 0.5,     # Lật ngang (tài xế bên trái/phải)
        mosaic    = 1.0,     # Mosaic augmentation
    )

    # Đường dẫn model best
    best_model = Path(OUTPUT_DIR) / RUN_NAME / "weights" / "best.pt"
    
    print("\n" + "=" * 60)
    print("  TRAINING HOÀN TẤT!")
    print(f"  Model tốt nhất: {best_model}")
    print("=" * 60)
    print("\n[BƯỚC TIẾP THEO]")
    print(f"  1. Copy model mới: copy {best_model} weights/yolo/seatbelt.pt")
    print(f"  2. Chạy test: python test_webcam.py")


if __name__ == "__main__":
    main()
