"""
YOLO Loader - Load và chạy inference YOLO ONNX model
Sử dụng onnxruntime để chạy model .onnx export từ YOLOv8
"""

import numpy as np
import onnxruntime as ort
import cv2


class YOLOLoader:
    def __init__(self, model_path: str, input_size: tuple = (640, 640)):
        """
        Args:
            model_path: đường dẫn đến file .onnx
            input_size:  kích thước ảnh đầu vào model (width, height), mặc định 640x640
        """
        self.model_path = model_path
        self.input_size = input_size  # (width, height)
        self.session = None
        self.input_name = None
        self.output_names = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self):
        """Load ONNX model vào onnxruntime session"""
        providers = self._get_providers()
        self.session = ort.InferenceSession(self.model_path, providers=providers)

        # Lấy tên input / output để dùng khi infer
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]

    def infer(self, frame: np.ndarray) -> np.ndarray:
        """
        Chạy inference trên một frame.

        Args:
            frame: ảnh BGR dạng numpy array (H, W, 3)

        Returns:
            output: numpy array thô từ model, shape (1, num_classes+4, num_anchors)
                    Cần postprocess bên ngoài (NMS, filter class, ...)
        """
        if self.session is None:
            raise RuntimeError("Model chưa được load. Hãy gọi load() trước.")

        # 1. Preprocess
        blob, (scale_x, scale_y), (pad_x, pad_y) = self._preprocess(frame)

        # 2. Inference
        outputs = self.session.run(self.output_names, {self.input_name: blob})

        # 3. Trả về output thô kèm thông số scale/pad để postprocess bên ngoài
        #    outputs[0] shape: (1, 4+num_classes, num_anchors) — format YOLOv8 ONNX
        return outputs[0], scale_x, scale_y, pad_x, pad_y

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _preprocess(self, frame: np.ndarray):
        """
        Letterbox resize + normalize ảnh về [0, 1], shape (1, 3, H, W).

        Returns:
            blob:           numpy array shape (1, 3, input_h, input_w), dtype float32
            (scale_x, scale_y): tỉ lệ scale từ ảnh gốc → input model
            (pad_x, pad_y):     số pixel padding (để tính lại tọa độ gốc sau này)
        """
        input_w, input_h = self.input_size
        orig_h, orig_w = frame.shape[:2]

        # --- Letterbox: giữ aspect ratio, thêm padding ---
        scale = min(input_w / orig_w, input_h / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)

        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Tạo canvas xám (114 là giá trị mặc định YOLO dùng)
        canvas = np.full((input_h, input_w, 3), 114, dtype=np.uint8)
        pad_x = (input_w - new_w) // 2
        pad_y = (input_h - new_h) // 2
        canvas[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized

        # BGR → RGB, normalize về [0, 1]
        rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        blob = rgb.astype(np.float32) / 255.0

        # HWC → CHW → NCHW
        blob = np.transpose(blob, (2, 0, 1))[np.newaxis, ...]  # (1, 3, H, W)

        # scale_x, scale_y để tính lại bbox về tọa độ ảnh gốc
        scale_x = orig_w / (input_w - 2 * pad_x)
        scale_y = orig_h / (input_h - 2 * pad_y)

        return blob, (scale_x, scale_y), (pad_x, pad_y)

    @staticmethod
    def _get_providers() -> list:
        """
        Tự động chọn provider phù hợp:
        - Nếu có GPU CUDA → dùng CUDAExecutionProvider
        - Fallback về CPU
        """
        available = ort.get_available_providers()
        if "CUDAExecutionProvider" in available:
            return ["CUDAExecutionProvider", "CPUExecutionProvider"]
        return ["CPUExecutionProvider"]
