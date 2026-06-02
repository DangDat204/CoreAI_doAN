"""
Driver State Model - Trạng thái realtime tài xế
"""


class DriverState:
    def __init__(self):
        self.eye_closed = False
        self.sleepy = False
        self.yawning = False
        self.head_pose = None  # Góc đầu (pitch, yaw, roll)
        self.face_landmarks = None
        self.ear = 0.0  # Eye Aspect Ratio
        self.mar = 0.0  # Mouth Aspect Ratio
