"""
FPS Calculator - Tính FPS realtime
"""

import time


class FPSCounter:
    def __init__(self):
        self.prev_time = 0
        self.fps = 0
    
    def update(self):
        """Cập nhật FPS"""
        current_time = time.time()
        if self.prev_time != 0:
            self.fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
    
    def get_fps(self):
        """Lấy FPS hiện tại"""
        return self.fps
