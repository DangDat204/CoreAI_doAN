"""
Image Utils - Hàm xử lý ảnh
resize, crop, normalize, ...
"""

import cv2
import numpy as np


class ImageUtils:
    @staticmethod
    def resize(frame, width, height):
        """Resize ảnh"""
        return cv2.resize(frame, (width, height))
    
    @staticmethod
    def crop(frame, bbox):
        """Cắt ảnh theo bbox"""
        x1, y1, x2, y2 = bbox
        return frame[y1:y2, x1:x2]
    
    @staticmethod
    def normalize(frame):
        """Chuẩn hóa ảnh"""
        return frame.astype(np.float32) / 255.0
    
    @staticmethod
    def denormalize(frame):
        """Denormalize ảnh"""
        return (frame * 255).astype(np.uint8)
