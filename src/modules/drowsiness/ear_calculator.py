"""
EAR Calculator - Tính Eye Aspect Ratio
EAR thấp lâu => ngủ gật
"""


class EARCalculator:
    @staticmethod
    def calculate_ear(eye_landmarks):
        """
        Tính Eye Aspect Ratio
        
        Args:
            eye_landmarks: điểm 6 mắt
            
        Returns:
            EAR value (0.0 - 1.0)
        """
        pass
    
    @staticmethod
    def is_eyes_closed(ear, threshold=0.2):
        """
        Kiểm tra mắt có đóng hay không
        
        Args:
            ear: Eye Aspect Ratio
            threshold: ngưỡng
            
        Returns:
            True nếu mắt đóng
        """
        return ear < threshold
