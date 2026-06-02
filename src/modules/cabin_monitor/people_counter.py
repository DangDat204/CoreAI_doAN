"""
People Counter - Đếm số người trong xe
"""


class PeopleCounter:
    def __init__(self):
        pass
    
    def count(self, tracked_persons):
        """
        Đếm số người đã được tracking
        
        Args:
            tracked_persons: danh sách TrackedPerson
            
        Returns:
            Số lượng người
        """
        return len(tracked_persons)
