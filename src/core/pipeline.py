"""
Pipeline - Điều phối toàn bộ luồng xử lý AI

Luồng chính:
frame -> person detect -> tracking -> driver selection -> drowsiness -> seatbelt
"""


class AIPipeline:
    def __init__(self):
        """Khởi tạo pipeline"""
        pass
    
    def run(self, frame):
        """
        Chạy toàn bộ pipeline
        
        Args:
            frame: numpy array ảnh
            
        Returns:
            Kết quả xử lý chứa:
            - detected_persons: danh sách người detect được
            - driver: tài xế được xác định
            - is_drowsy: có ngủ gật không
            - has_seatbelt: có đeo dây an toàn không
        """
        pass
    
    def person_detect(self, frame):
        """Detect người"""
        pass
    
    def tracking(self, frame, detections):
        """Tracking người"""
        pass
    
    def select_driver(self, tracked_persons):
        """Xác định tài xế"""
        pass
    
    def detect_drowsiness(self, frame, driver):
        """Detect ngủ gật"""
        pass
    
    def detect_seatbelt(self, frame, driver):
        """Detect dây an toàn"""
        pass
