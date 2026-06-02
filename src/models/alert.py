"""
Alert Model - Dữ liệu cảnh báo
"""

from enum import Enum
from datetime import datetime


class AlertType(Enum):
    DROWSINESS = "drowsiness"
    NO_SEATBELT = "no_seatbelt"
    OCCUPANCY = "occupancy"
    FACE_NOT_FOUND = "face_not_found"


class AlertSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Alert:
    def __init__(self, alert_type, severity):
        self.alert_type = alert_type
        self.severity = severity
        self.timestamp = datetime.now()
        self.description = ""
