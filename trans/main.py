import tools as tl
import numpy as np
import cv2
import json
#------------------------------------读取基本信息--------------------------------------------------
# 从 JSON 文件读取变量
with open("data/camera.json", "r",encoding="utf-8") as json_file:
    data = json.load(json_file)

# 从读取到的 JSON 数据中获取变量
h_angle = data.get("预置位", {}).get("P", 0)
v_angle = data.get("预置位", {}).get("T", 0)
camera_h = data.get("高度（米）", 0)
camere_point_w = (data.get("经纬度", {}).get("纬度", 0),data.get("经纬度", {}).get("经度", 0))
pixel_coord = data.get("像素坐标",[])
pixel_coordinates_world = data.get("地理坐标",[])
#调整经纬度格式到维经度
pixel_coordinates_w = [[coord[1],coord[0]] for coord in pixel_coordinates_world]

#将世界坐标组转换为utm坐标--------------------------------------------------------------------------------
pixel_coordinates_utm = tl.convert_to_utm(pixel_coordinates_w)
camere_point_utm = tl.convert_to_utm(camere_point_w)

#获得转换矩阵并写入json-------------------------------------------------------------------------------------------
pixel_coord = np.array(pixel_coord)  # 转换为numpy数组
pixel_coordinates_utm_float = np.array([(float(x), float(y)) for x, y in pixel_coordinates_utm])  # 转换为numpy数组，这一步是为了防止没有去掉引号
H,_=cv2.findHomography((pixel_coord), (pixel_coordinates_utm_float))
H2,_=cv2.findHomography((pixel_coordinates_utm_float),(pixel_coord) )

# 将矩阵转换为列表形式
H_list = H.tolist()
H2_list = H2.tolist()

# 更新 JSON 数据
data["转换矩阵"] = {
    "像素坐标转utm": H_list,
    "utm转像素坐标": H2_list
}
# 将更新后的 JSON 数据写入文件
with open("data/camera.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

#计算更新后的utm坐标和转换矩阵并写入json----------------------------------------------------------------------
with open("data/newpicture.json", "r",encoding="utf-8") as json_file:
    data_new = json.load(json_file)
h_angle_new = data_new.get("朝向", {}).get("P", 0)
v_angle_new = data_new.get("朝向", {}).get("T", 0)
h_angle_c = h_angle - h_angle_new
v_angle_c = v_angle_new - v_angle
camere_point_utm_float = tuple(map(float, camere_point_utm))

pixel_coordinates_utm_float_new = tl.get_new_utmposition(camere_point_utm_float,pixel_coordinates_utm_float,h_angle_c,v_angle_c,camera_h)
pixel_coordinates_utm_float_new = np.array(pixel_coordinates_utm_float_new)
H_2,_=cv2.findHomography((pixel_coord), (pixel_coordinates_utm_float_new))
H2_2,_=cv2.findHomography( (pixel_coordinates_utm_float_new),(pixel_coord))

# 将矩阵转换为列表形式
H_list = H_2.tolist()
H2_list = H2_2.tolist()
# 读取原有的 JSON 数据
# 更新 JSON 数据
data_new["转换矩阵"] = {
    "像所坐标转utm": H_list,
    "utm转像素坐标": H2_list
}
img_path = data_new.get("图片位置",0)
# 将更新后的 JSON 数据写入文件
with open("data/newpicture.json", "w", encoding="utf-8") as json_file:
    json.dump(data_new, json_file, indent=4, ensure_ascii=False)

#测试----------------------------------------------------------------------------------------------------------------
test_result = tl.select_points_and_transform(img_path,H_2,pixel_coord)
#显示采集的信息






