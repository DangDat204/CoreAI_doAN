"""
Person Detector - Detect người bằng YOLO ONNX
Nhận output thô từ YOLOLoader, postprocess (NMS + filter) → list[Detection]
"""

import numpy as np
import cv2

from src.loaders.yolo_loader import YOLOLoader
from src.models.detection import Detection
from src.config import settings


# Index của class "person" trong COCO dataset (YOLOv8 mặc định train trên COCO)
PERSON_CLASS_ID = 0


class PersonDetector:
    def __init__(
        self,
        model_path: str = settings.YOLO_PERSON_MODEL,
        confidence_threshold: float = settings.PERSON_CONFIDENCE,
        iou_threshold: float = 0.45,
        min_size: int = settings.MIN_DETECTION_SIZE,
    ):
        """
        Args:
            model_path:           đường dẫn file .onnx
            confidence_threshold: ngưỡng confidence để giữ detection (default 0.5)
            iou_threshold:        ngưỡng IoU cho NMS (default 0.45)
            min_size:             kích thước bbox tối thiểu (px), bỏ bbox quá nhỏ
        """
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.min_size = min_size

        self._loader = YOLOLoader(model_path)
        self._loader.load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(self, frame: np.ndarray) -> list[Detection]:
        """
        Detect người trong frame.

        Args:
            frame: ảnh BGR dạng numpy array (H, W, 3)

        Returns:
            Danh sách Detection chứa bbox người đã qua NMS
        """
        # 1. Chạy YOLO inference, nhận output thô + thông số scale/pad
        raw_output, scale_x, scale_y, pad_x, pad_y = self._loader.infer(frame)

        # 2. Postprocess: parse → filter → NMS
        detections = self._postprocess(raw_output, scale_x, scale_y, pad_x, pad_y)

        return detections

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _postprocess(
        self,
        raw_output: np.ndarray,
        scale_x: float,
        scale_y: float,
        pad_x: int,
        pad_y: int,
    ) -> list[Detection]:
        """
        Parse output thô của YOLOv8 ONNX → list[Detection].

        YOLOv8 export ONNX shape: (1, 4 + num_classes, num_anchors)
          - 4 đầu: cx, cy, w, h (trong tọa độ input model)
          - Còn lại: score từng class

        Args:
            raw_output: numpy array (1, 4+num_classes, num_anchors)
            scale_x/y:  tỉ lệ scale ảnh gốc / kích thước letterbox thực
            pad_x/y:    padding đã thêm khi letterbox

        Returns:
            list[Detection] đã lọc class person và áp NMS
        """
        # Bỏ batch dim → (4+num_classes, num_anchors)
        output = raw_output[0]

        # Transpose → (num_anchors, 4+num_classes)
        output = output.T  # shape: (num_anchors, 4+num_classes)

        boxes_cxcywh = output[:, :4]           # cx, cy, w, h
        class_scores = output[:, 4:]           # shape: (num_anchors, num_classes)

        # Lấy confidence = max score qua các class
        confidences = class_scores[:, PERSON_CLASS_ID]  # chỉ lấy class person

        # Filter theo confidence threshold
        mask = confidences >= self.confidence_threshold
        if not mask.any():
            return []

        boxes_cxcywh = boxes_cxcywh[mask]
        confidences = confidences[mask]

        # cx, cy, w, h (trong tọa độ input model) → x1, y1, x2, y2 (ảnh gốc)
        boxes_xyxy = self._cxcywh_to_xyxy(boxes_cxcywh, scale_x, scale_y, pad_x, pad_y)

        # Bỏ bbox quá nhỏ
        boxes_xyxy, confidences = self._filter_small(boxes_xyxy, confidences)
        if len(boxes_xyxy) == 0:
            return []

        # NMS
        indices = self._nms(boxes_xyxy, confidences, self.iou_threshold)

        # Tạo list Detection
        result = []
        for i in indices:
            bbox = boxes_xyxy[i].tolist()   # [x1, y1, x2, y2]
            conf = float(confidences[i])
            result.append(Detection(bbox=bbox, confidence=conf, class_name="person"))

        return result

    def _cxcywh_to_xyxy(
        self,
        boxes: np.ndarray,
        scale_x: float,
        scale_y: float,
        pad_x: int,
        pad_y: int,
    ) -> np.ndarray:
        """
        Chuyển (cx, cy, w, h) trong tọa độ input model
        về (x1, y1, x2, y2) trong tọa độ ảnh gốc.
        """
        cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]

        x1 = (cx - w / 2 - pad_x) * scale_x
        y1 = (cy - h / 2 - pad_y) * scale_y
        x2 = (cx + w / 2 - pad_x) * scale_x
        y2 = (cy + h / 2 - pad_y) * scale_y

        return np.stack([x1, y1, x2, y2], axis=1)

    def _filter_small(
        self, boxes: np.ndarray, confidences: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Bỏ các bbox có chiều rộng hoặc chiều cao nhỏ hơn min_size."""
        w = boxes[:, 2] - boxes[:, 0]
        h = boxes[:, 3] - boxes[:, 1]
        mask = (w >= self.min_size) & (h >= self.min_size)
        return boxes[mask], confidences[mask]

    @staticmethod
    def _nms(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float) -> list[int]:
        """
        Non-Maximum Suppression bằng cv2.dnn.NMSBoxes.

        Args:
            boxes:         numpy array (N, 4) dạng [x1, y1, x2, y2]
            scores:        numpy array (N,)
            iou_threshold: ngưỡng IoU

        Returns:
            Danh sách index được giữ lại
        """
        # cv2.dnn.NMSBoxes yêu cầu format [x, y, w, h]
        boxes_xywh = boxes.copy()
        boxes_xywh[:, 2] = boxes[:, 2] - boxes[:, 0]  # w
        boxes_xywh[:, 3] = boxes[:, 3] - boxes[:, 1]  # h

        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes_xywh.tolist(),
            scores=scores.tolist(),
            score_threshold=0.0,    # đã filter trước rồi
            nms_threshold=iou_threshold,
        )

        if len(indices) == 0:
            return []

        # cv2 trả về shape (N, 1) hoặc (N,) tùy version
        return indices.flatten().tolist()
