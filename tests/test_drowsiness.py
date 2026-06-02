"""
Test Drowsiness Detection
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from modules.drowsiness.drowsiness_detector import DrowsinessDetector


class TestDrowsinessDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DrowsinessDetector(frame_limit=20, ear_threshold=0.2)
    
    def test_normal_eyes_open(self):
        """Test mắt mở bình thường"""
        result = self.detector.detect(0.5)
        self.assertFalse(result)
    
    def test_eyes_closed_below_threshold(self):
        """Test mắt đóng dưới ngưỡng"""
        # Mắt đóng 20 frame liên tiếp
        for _ in range(20):
            result = self.detector.detect(0.1)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
