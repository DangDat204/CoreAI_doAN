"""
Embedding Extractor - Trích xuất vector embedding khuôn mặt
face -> vector 512 chiều
"""


class EmbeddingExtractor:
    def __init__(self):
        pass
    
    def extract(self, frame, face_bbox):
        """
        Trích xuất embedding từ khuôn mặt
        
        Args:
            frame: numpy array ảnh
            face_bbox: bbox khuôn mặt [x1, y1, x2, y2]
            
        Returns:
            Vector 512 chiều
        """
        pass
