"""
Test Tracking
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from modules.tracking.tracker import Tracker


class TestTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = Tracker()
    
    def test_tracker_initialization(self):
        """Test khởi tạo tracker"""
        self.assertIsNotNone(self.tracker)
    
    def test_tracker_update(self):
        """Test cập nhật tracker"""
        # TODO: Implement test
        pass


if __name__ == "__main__":
    unittest.main()
