"""
Seatbelt Checker - Lớp trung gian kiểm tra dây an toàn cho Pipeline.

Nhiệm vụ: nhận frame + bbox người từ pipeline,
gọi SeatbeltDetector, rồi trả kết quả gọn gàng về.
"""

from src.modules.detection.seatbelt_detector import SeatbeltDetector
from src.config import settings


class SeatbeltChecker:
    def __init__(self):
        """
        Khởi tạo SeatbeltChecker, load model YOLO một lần duy nhất.
        """
        self.detector = SeatbeltDetector(
            model_path=settings.YOLO_SEATBELT_MODEL,
            confidence=settings.SEATBELT_CONFIDENCE,   # ← fix: dùng đúng ngưỡng seatbelt
        )

    def check(self, frame, person_bbox) -> dict:
        """
        Kiểm tra người trong bbox có đeo dây an toàn không.

        Args:
            frame:       numpy array ảnh gốc (BGR)
            person_bbox: [x1, y1, x2, y2] vùng chứa người cần kiểm tra

        Returns:
            dict gồm:
                - has_seatbelt (bool):  True = có đeo dây
                - class_name  (str):   "seatbelt" hoặc "no-seatbelt"
                - confidence  (float): độ tin cậy
                - bbox        (list):  tọa độ dây trong ảnh gốc
        """
        return self.detector.detect(frame, person_bbox)

    def check_all(self, frame, person_bboxes: list) -> list[dict]:
        """
        Kiểm tra dây an toàn cho nhiều người cùng lúc.

        Args:
            frame:         numpy array ảnh gốc
            person_bboxes: danh sách các bbox [[x1,y1,x2,y2], ...]

        Returns:
            Danh sách kết quả, mỗi phần tử tương ứng với 1 người trong bboxes
        """
        return [self.detector.detect(frame, bbox) for bbox in person_bboxes]
