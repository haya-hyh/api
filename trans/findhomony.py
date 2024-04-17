import cv2
import numpy as np

# im1 = cv2.imread(‘left.jpg’)
# im2 = cv2.imread(‘right.jpg’)

src_points = np.array([[581.12255588855454545454545777557, 297], [1053.4545, 173], [1041, 895], [558, 827]])
dst_points = np.array([[571.0, 257], [963.0, 333], [965, 801.1234567895865565645], [557, 827]])

H, _ = cv2.findHomography(src_points, dst_points)
src_float = src_points.astype(np.float32)
dst_float = dst_points.astype(np.float32)
T = cv2.getPerspectiveTransform(src_float, dst_float)

print("homography :",H)
print("transform :",T)
print(np.dot(H,np.array([800,200,1])))


# 两个函数得到的结果一样或相近，但是perspectiveTransform函数对输入要求float32,多次测试感觉findHomography更准确