"""
FaceMesh Loader - Load MediaPipe FaceMesh model
"""


class FaceMeshLoader:
    def __init__(self, model_path):
        """
        Args:
            model_path: đường dẫn đến model FaceMesh
        """
        self.model_path = model_path
        self.model = None
    
    def load(self):
        """Load model"""
        pass
    
    def get_landmarks(self, frame):
        """
        Lấy landmarks khuôn mặt
        
        Args:
            frame: numpy array ảnh
            
        Returns:
            Danh sách landmarks (mắt, miệng, mũi, ...)
        """
        pass
