"""
Test Seatbelt Detection
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from modules.detection.seatbelt_detector import SeatbeltDetector


class TestSeatbeltDetector(unittest.TestCase):
    def setUp(self):
        self.detector = SeatbeltDetector()
    
    def test_seatbelt_detector_initialization(self):
        """Test khởi tạo seatbelt detector"""
        self.assertIsNotNone(self.detector)
    
    def test_seatbelt_detection(self):
        """Test detect dây an toàn"""
        # TODO: Implement test
        pass


if __name__ == "__main__":
    unittest.main()
