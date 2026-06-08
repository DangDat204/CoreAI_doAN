"""
Debug nhanh: xem model THỰC SỰ thấy gì ở conf thấp,
vẽ bbox lên ảnh để kiểm tra trực quan.

Chạy từ thư mục gốc:
    python tests/debug_seatbelt.py
    python tests/debug_seatbelt.py --image data/driver_images/ten_anh.jpg
"""

import sys, os, argparse, cv2
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ultralytics import YOLO
from src.config import settings

# ── Cấu hình ──────────────────────────────────────────────────────────────
CONF_LEVELS = [0.1, 0.25, 0.4]   # Thử nhiều ngưỡng từ thấp → cao
OUT_DIR     = "data/debug_output" # Ảnh kết quả sẽ lưu ở đây
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load model ────────────────────────────────────────────────────────────
print(f"[DEBUG] Load model: {settings.YOLO_SEATBELT_MODEL}")
model = YOLO(settings.YOLO_SEATBELT_MODEL)
print(f"[DEBUG] Classes: {model.names}\n")

# ── Chọn ảnh ─────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--image", type=str, default=None)
args = parser.parse_args()

if args.image:
    image_paths = [args.image]
else:
    folder = "data/driver_images"
    image_paths = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ] if os.path.exists(folder) else []

if not image_paths:
    print("[LỖI] Không tìm thấy ảnh. Dùng --image path/to/anh.jpg")
    sys.exit(1)

# ── Vẽ màu theo class ─────────────────────────────────────────────────────
COLOR = {
    "seatbelt":    (0, 200, 0),    # Xanh lá
    "no-seatbelt": (0, 0, 220),    # Đỏ
}

# ── Chạy debug ───────────────────────────────────────────────────────────
for img_path in image_paths:
    img = cv2.imread(img_path)
    if img is None:
        print(f"[LỖI] Không đọc được: {img_path}")
        continue

    base = os.path.splitext(os.path.basename(img_path))[0]
    print(f"{'='*60}")
    print(f"Ảnh: {os.path.basename(img_path)}  ({img.shape[1]}x{img.shape[0]}px)")

    for conf_thresh in CONF_LEVELS:
        results = model(img, conf=conf_thresh, verbose=False)

        # Gom tất cả detections
        detections = []
        for r in results:
            for box in r.boxes:
                cls_id   = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf_val = float(box.conf[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                detections.append((cls_name, conf_val, x1, y1, x2, y2))

        print(f"\n  [conf >= {conf_thresh}] → {len(detections)} detection(s):")

        # Vẽ bbox lên bản copy ảnh
        canvas = img.copy()
        for cls_name, conf_val, x1, y1, x2, y2 in detections:
            icon   = "✅" if cls_name == "seatbelt" else "❌"
            color  = COLOR.get(cls_name, (128, 128, 128))
            label  = f"{cls_name} {conf_val:.2f}"
            print(f"    {icon} {label}  bbox=[{x1},{y1},{x2},{y2}]")

            # Vẽ hình chữ nhật
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)

            # Nền text
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(canvas, (x1, y1 - 22), (x1 + tw + 4, y1), color, -1)
            cv2.putText(canvas, label, (x1 + 2, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if not detections:
            print(f"    (không thấy gì)")

        # Lưu ảnh debug
        out_name = f"{base}_conf{int(conf_thresh*100)}.jpg"
        out_path = os.path.join(OUT_DIR, out_name)
        cv2.imwrite(out_path, canvas)
        print(f"    → Lưu ảnh: {out_path}")

print(f"\n✅ Xong! Xem ảnh debug trong: {OUT_DIR}/")
