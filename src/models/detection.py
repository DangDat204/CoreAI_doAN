"""
Detection Model - Dữ liệu object được detect
"""


class Detection:
    def __init__(self, bbox, confidence, class_name):
        """
        Args:
            bbox: [x1, y1, x2, y2]
            confidence: độ tin cậy
            class_name: tên class (person, seatbelt, ...)
        """
        self.bbox = bbox
        self.confidence = confidence
        self.class_name = class_name
    
    def get_area(self):
        """Tính diện tích bbox"""
        x1, y1, x2, y2 = self.bbox
        return (x2 - x1) * (y2 - y1)
