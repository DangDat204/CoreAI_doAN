"""
MAR Calculator - Tính Mouth Aspect Ratio
MAR cao => ngáp
"""


class MARCalculator:
    @staticmethod
    def calculate_mar(mouth_landmarks):
        """
        Tính Mouth Aspect Ratio
        
        Args:
            mouth_landmarks: điểm miệng
            
        Returns:
            MAR value (0.0 - 1.0)
        """
        pass
    
    @staticmethod
    def is_yawning(mar, threshold=0.5):
        """
        Kiểm tra có đang ngáp hay không
        
        Args:
            mar: Mouth Aspect Ratio
            threshold: ngưỡng
            
        Returns:
            True nếu đang ngáp
        """
        return mar > threshold
