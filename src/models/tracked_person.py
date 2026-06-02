"""
Tracked Person Model - Người đã được tracking
"""


class TrackedPerson:
    def __init__(self, track_id, bbox):
        """
        Args:
            track_id: ID của track
            bbox: [x1, y1, x2, y2]
        """
        self.track_id = track_id
        self.bbox = bbox
        self.is_driver = False
        self.has_seatbelt = False
        self.face_embedding = None
        self.age_group = None  # "child" or "adult"
