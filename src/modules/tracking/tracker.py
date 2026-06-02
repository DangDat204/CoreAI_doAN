"""
Tracker - ByteTrack / DeepSORT
Gán ID cho từng người để tracking liên tục
"""


class Tracker:
    def __init__(self):
        pass
    
    def update(self, frame, detections):
        """
        Cập nhật tracking
        
        Args:
            frame: numpy array ảnh
            detections: danh sách Detection
            
        Returns:
            Danh sách TrackedPerson với track_id
        """
        pass
