"""
YOLO Loader - Load YOLO ONNX model
"""


class YOLOLoader:
    def __init__(self, model_path):
        """
        Args:
            model_path: đường dẫn đến file .onnx
        """
        self.model_path = model_path
        self.model = None
    
    def load(self):
        """Load model"""
        pass
    
    def infer(self, frame):
        """
        Chạy inference
        
        Args:
            frame: numpy array ảnh
            
        Returns:
            Detections
        """
        pass
