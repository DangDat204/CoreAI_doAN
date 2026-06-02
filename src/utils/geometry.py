"""
Geometry - Hàm toán học hình học
Khoảng cách điểm, góc đầu, ...
"""

import numpy as np


class Geometry:
    @staticmethod
    def euclidean_distance(p1, p2):
        """Tính khoảng cách Euclidean"""
        return np.linalg.norm(np.array(p1) - np.array(p2))
    
    @staticmethod
    def cosine_similarity(v1, v2):
        """Tính cosine similarity"""
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    @staticmethod
    def bbox_iou(box1, box2):
        """Tính Intersection over Union"""
        pass
    
    @staticmethod
    def compute_head_pose(landmarks):
        """Tính góc đầu"""
        pass
