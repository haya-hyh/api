import cv2
import numpy as np

def get_perspective_transform(pixel_coordinates, utm_coordinates):
    """
    计算透视变换矩阵
    
    参数：
    pixel_coordinates: list，像素坐标组，每个元素是一个二元元组 (x, y)
    utm_coordinates: list，UTM坐标组，每个元素是一个二元元组 (x, y)
    
    返回值：
    H: 透视变换矩阵
    """
    # 将像素坐标和UTM坐标转换为numpy数组，并转换为浮点型
    pixel_coordinates = np.array(pixel_coordinates, dtype=np.float32)
    utm_coordinates = np.array(utm_coordinates, dtype=np.float32)
    
    # 计算透视变换矩阵
    H, _ = cv2.findHomography(pixel_coordinates, utm_coordinates)
    
    return H

# 示例用法
pixel_coordinates_w = [(100, 100), (200, 200), (300, 300)]  # 像素坐标组
utm_coordinates = [(1000, 2000), (1500, 2500), (2000, 3000)]  # UTM坐标组

perspective_matrix = get_perspective_transform(pixel_coordinates_w, utm_coordinates)
print("透视变换矩阵:", perspective_matrix)
