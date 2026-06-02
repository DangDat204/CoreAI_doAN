"""
Face Matcher - So khớp vector embedding khuôn mặt
Dùng cosine similarity để xác định xem người này là ai
"""


class FaceMatcher:
    def __init__(self):
        self.known_embeddings = {}  # {name: embedding_vector}
    
    def add_known_face(self, name, embedding):
        """
        Thêm khuôn mặt đã biết
        
        Args:
            name: tên người
            embedding: vector embedding
        """
        self.known_embeddings[name] = embedding
    
    def match(self, embedding, threshold=0.6):
        """
        So khớp embedding với danh sách đã biết
        
        Args:
            embedding: vector embedding cần match
            threshold: ngưỡng cosine similarity
            
        Returns:
            (name, similarity) hoặc (None, 0)
        """
        pass
