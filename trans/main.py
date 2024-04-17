import get_pixel_coor
import get_utm_transform
import get_new_utm
import get_pixel_test
import cv2
import numpy as np
from pyproj import Transformer
import camera as c

h_angle = c.h_angle
v_angle = c.v_angle
camera_h = c.camera_h
camere_point_w = c.camere_point_w
#读取像素坐标组1
img_path = input("请输入要打开的图片路径：")
pixel_coord1 = get_pixel_coor.get_pixel_coordinates(img_path)


#读取像素坐标组1经纬度

#----- 自动读取坐标
with open('move_data.txt', 'r') as file:
    lines = file.readlines()
coordinates = ''.join(lines).replace('[', '').replace(']', '').split(',')

# 将每两个连续的字符串转换为浮点数，并组成坐标点列表
pixel_coordinates_w = []
for i in range(0, len(coordinates), 2):
    y = float(coordinates[i])
    x = float(coordinates[i + 1])
    pixel_coordinates_w.append((x, y))
print(pixel_coordinates_w)

#将世界坐标组1转换为utm坐标
pixel_coordinates_utm = get_utm_transform.convert_to_utm(pixel_coordinates_w)

#获得转换矩阵
pixel_coord1 = np.array(pixel_coord1)  # 转换为numpy数组
pixel_coordinates_utm_float = np.array([(float(x), float(y)) for x, y in pixel_coordinates_utm])  # 转换为numpy数组

print(type(pixel_coord1))
print(type(pixel_coordinates_utm))
print(pixel_coord1)
print(pixel_coordinates_utm)

H,_=cv2.findHomography((pixel_coord1), (pixel_coordinates_utm_float))
H2,_=cv2.findHomography((pixel_coordinates_utm_float),(pixel_coord1) )


lat,lon = camere_point_w
transformer = Transformer.from_crs("epsg:4326", "epsg:32649") 
x,y = transformer.transform(lat, lon)
camere_point_utm=(x,y)

pixel_coordinates_utm_float_2 = []
pixel_coordinates_utm_float_2 = get_new_utm.get_new_utmposition(camere_point_utm,pixel_coordinates_utm_float,h_angle,camera_h,v_angle)
pixel_coordinates_utm_float_2_np = np.array(pixel_coordinates_utm_float_2)
H_2,_=cv2.findHomography((pixel_coord1), (pixel_coordinates_utm_float_2_np))
H2_2,_=cv2.findHomography( (pixel_coordinates_utm_float_2_np),(pixel_coord1))


img_path_2 = input("请输入要打开的图片2路径：")
test_coord_w = get_pixel_test.select_points_and_transform(img_path_2,H_2,pixel_coord1)
print(test_coord_w)






