"""
Chạy test bằng video
"""

import cv2
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.pipeline import AIPipeline
from utils.logger import Logger
from src.config.settings import INPUT_VIDEO_PATH


def main():
    logger = Logger("video_runner")
    logger.info("Starting video pipeline...")
    
    pipeline = AIPipeline()
    
    # Chọn video
    video_path = INPUT_VIDEO_PATH + "test_drive_1.mp4"
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        logger.error(f"Cannot open video: {video_path}")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Chạy pipeline
            result = pipeline.run(frame)
            
            # Hiển thị
            cv2.imshow("Core AI - Video", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        logger.error(f"Error: {e}")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Video pipeline stopped")


if __name__ == "__main__":
    main()
