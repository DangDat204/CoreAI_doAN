"""
Face Landmarks - Lấy landmark mắt/mũi/miệng từ FaceMesh
"""


class FaceLandmarks:
    def __init__(self):
        pass
    
    def get_landmarks(self, frame, face_bbox):
        """
        Lấy landmarks khuôn mặt
        
        Args:
            frame: numpy array ảnh
            face_bbox: bbox khuôn mặt [x1, y1, x2, y2]
            
        Returns:
            Danh sách landmarks {
                'left_eye': [...],
                'right_eye': [...],
                'mouth': [...],
                ...
            }
        """
        pass
