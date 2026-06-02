"""
Drowsiness Detector - Logic cuối cùng detect ngủ gật
Nếu EAR thấp 20 frame liên tiếp => ngủ gật
"""


class DrowsinessDetector:
    def __init__(self, frame_limit=20, ear_threshold=0.2):
        self.frame_limit = frame_limit
        self.ear_threshold = ear_threshold
        self.closed_eye_frames = 0
    
    def detect(self, ear):
        """
        Detect ngủ gật dựa trên EAR
        
        Args:
            ear: Eye Aspect Ratio
            
        Returns:
            True nếu ngủ gật, False nếu tỉnh
        """
        if ear < self.ear_threshold:
            self.closed_eye_frames += 1
        else:
            self.closed_eye_frames = 0
        
        return self.closed_eye_frames >= self.frame_limit
