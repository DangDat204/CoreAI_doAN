"""
Alert Manager - Quản lý cảnh báo
- Phát âm thanh
- Hiển thị text đỏ
- Lưu ảnh cảnh báo
"""


class AlertManager:
    def __init__(self):
        self.active_alerts = []
    
    def alert_drowsiness(self, frame, timestamp):
        """Cảnh báo tài xế ngủ gật"""
        pass
    
    def alert_no_seatbelt(self, frame, timestamp):
        """Cảnh báo không đeo dây an toàn"""
        pass
    
    def alert_unusual_occupancy(self, frame, timestamp):
        """Cảnh báo số người bất thường"""
        pass
    
    def play_sound(self, alert_type):
        """Phát âm thanh cảnh báo"""
        pass
    
    def save_screenshot(self, frame, alert_type):
        """Lưu ảnh cảnh báo"""
        pass
