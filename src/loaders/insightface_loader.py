"""
InsightFace Loader - Load InsightFace model
"""


class InsightFaceLoader:
    def __init__(self, model_path):
        """
        Args:
            model_path: đường dẫn đến model InsightFace
        """
        self.model_path = model_path
        self.model = None
    
    def load(self):
        """Load model"""
        pass
    
    def extract_embedding(self, frame, bbox):
        """
        Trích xuất embedding từ khuôn mặt
        
        Args:
            frame: numpy array ảnh
            bbox: [x1, y1, x2, y2]
            
        Returns:
            Vector embedding 512 chiều
        """
        pass
