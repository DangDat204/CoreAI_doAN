"""
UI Overlay - Hiển thị thông tin lên frame
FPS, trạng thái ngủ gật, dây an toàn, số người, ...
"""


class UIOverlay:
    @staticmethod
    def add_fps(frame, fps):
        """Thêm FPS"""
        pass
    
    @staticmethod
    def add_drowsiness_indicator(frame, is_sleepy):
        """Thêm chỉ báo ngủ gật"""
        pass
    
    @staticmethod
    def add_seatbelt_status(frame, has_seatbelt):
        """Thêm trạng thái dây an toàn"""
        pass
    
    @staticmethod
    def add_people_count(frame, count):
        """Thêm số lượng người"""
        pass
    
    @staticmethod
    def render(frame, data):
        """
        Render toàn bộ UI overlay
        
        Args:
            frame: numpy array ảnh
            data: dữ liệu cần hiển thị
            
        Returns:
            Frame có UI overlay
        """
        pass
