"""
State Manager - Bộ nhớ realtime của hệ thống
Lưu trữ trạng thái:
- Tài xế hiện tại
- Có đeo dây an toàn không
- Đang ngủ gật không
- Số người trong xe
"""


class StateManager:
    def __init__(self):
        self.current_driver = None
        self.driver_has_seatbelt = False
        self.driver_is_sleepy = False
        self.people_count = 0
        self.tracked_persons = {}
    
    def update_driver(self, driver_id):
        """Cập nhật tài xế hiện tại"""
        self.current_driver = driver_id
    
    def update_seatbelt_status(self, driver_id, has_seatbelt):
        """Cập nhật trạng thái dây an toàn"""
        if self.current_driver == driver_id:
            self.driver_has_seatbelt = has_seatbelt
    
    def update_drowsiness(self, driver_id, is_sleepy):
        """Cập nhật trạng thái ngủ gật"""
        if self.current_driver == driver_id:
            self.driver_is_sleepy = is_sleepy
    
    def update_people_count(self, count):
        """Cập nhật số người trong xe"""
        self.people_count = count
