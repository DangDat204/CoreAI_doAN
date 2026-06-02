"""
Chạy realtime webcam
"""

import cv2
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.pipeline import AIPipeline
from utils.logger import Logger


def main():
    logger = Logger("webcam_runner")
    logger.info("Starting webcam pipeline...")
    
    pipeline = AIPipeline()
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Chạy pipeline
            result = pipeline.run(frame)
            
            # Hiển thị
            cv2.imshow("Core AI - Webcam", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        logger.error(f"Error: {e}")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Webcam pipeline stopped")


if __name__ == "__main__":
    main()
