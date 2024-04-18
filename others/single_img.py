import cv2
from pyproj import Transformer
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from matplotlib.image import imread
#------------------------------------------------------------单个图片取得像素坐标----------------------
# 获取图片路径
image_path = input("请输入要打开的图片路径：")
# 创建空数组用于保存像素坐标
pixel_coordinates1 = []
# 打开并显示图片0
try:
    img = imread(image_path)
    fig, ax = plt.subplots(figsize=(32, 24))
    ax.imshow(img)
    plt.title("Select your points")
    plt.axis('on')
    

    # 获取点的像素坐标
    while True:
        point = plt.ginput(1, timeout=0)
        if not point:
            break
        pixel_coordinates1.append(point[0])
        print("像素坐标:", point[0])

        # 在图上添加一个小点以标记所选位置
        ax.add_patch(Circle((point[0][0], point[0][1]), 2, color='r'))

        # 重新绘制图形以更新小点和连线
        plt.draw()
        # 绘制连接点的线段形成多边形
        if len(pixel_coordinates1) >= 2:
            ax.plot([pixel_coordinates1[-2][0], pixel_coordinates1[-1][0]],
                    [pixel_coordinates1[-2][1], pixel_coordinates1[-1][1]], 'r')
            
    # 保存的像素坐标
    # 删除最后一个坐标
    pixel_coordinates1 = pixel_coordinates1[:-1] 
    print("保存的像素坐标:", pixel_coordinates1)
except FileNotFoundError:
    print("找不到指定的图片文件，请确认路径是否正确。")
except Exception as e:
    print("发生错误:", e)
#----------------------------------------------------------输入对应的经纬度并转换为utm坐标-------------------------------
#x表示纬度！！！
point_N = len(pixel_coordinates1)
pixel_coordinates_w = []
pixel_coordinates_utm = []

# 东莞 WGS_1984_UTM_Zone_49N 对应 32649
transformer = Transformer.from_crs("epsg:4326", "epsg:32649") 

#----- 手动输入坐标
"""
for i in range(point_N):

    print(f"第{i+1}个坐标")
    x = float(input("请输入它的纬度："))
    y = float(input("请输入它的经度："))
    pixel_coordinates_w.append((x, y))
    utm_x, utm_y =  transformer.transform(x, y)
    utm_x = "{:.12f}".format(utm_x)
    utm_y = "{:.12f}".format(utm_y)
    pixel_coordinates_utm.append((utm_x, utm_y))
    print("手动输入的坐标:", (x, y))
    print("UTM坐标 x:", utm_x, "UTM坐标 y:", utm_y)
"""
#"""
#------ 自动读取文件并解析坐标数据

with open('single_data.txt', 'r') as file:
    lines = file.readlines()    
coordinates = ''.join(lines).replace('[', '').replace(']', '').split(',')

# 将每两个连续的字符串转换为浮点数，并组成坐标点列表
pixel_coordinates_w = []
for i in range(0, len(coordinates), 2):
    y = float(coordinates[i])
    x = float(coordinates[i + 1])
    pixel_coordinates_w.append((x, y))
# 转换坐标为UTM坐标
pixel_coordinates_utm = []
for x, y in pixel_coordinates_w:
    utm_x, utm_y = transformer.transform(x, y)  # 注意纬度在前，经度在后
    utm_x = "{:.14f}".format(utm_x)
    utm_y = "{:.14f}".format(utm_y)
    pixel_coordinates_utm.append((utm_x, utm_y))
#--------------自动部分结尾
#"""    
# 打印结果
for i, (x, y) in enumerate(pixel_coordinates_w):
    print(f"第{i+1}个坐标：")
    print("手动输入的坐标:", (x, y))
    print("UTM坐标 x:", pixel_coordinates_utm[i][0], "UTM坐标 y:", pixel_coordinates_utm[i][1])


#----------------------------------------------------------构造转换矩阵-------------------------------
# 将utm坐标系近似看成局部的世界坐标系，实际上高斯更好, 转换矩阵是三行四列的
print(pixel_coordinates1)
print(pixel_coordinates_utm)
print(pixel_coordinates_w)
# 将字符串类型的坐标值转换为浮点数类型
pixel_coordinates_utm_float = np.array([(float(x), float(y)) for x, y in pixel_coordinates_utm])
pixel_coordinates1 = np.array(pixel_coordinates1)
print("像素坐标：",pixel_coordinates1)
print("utm坐标：",pixel_coordinates_utm_float)
print("utm坐标shape：",pixel_coordinates_utm_float.shape)

# perspective_matrix = cv2.getPerspectiveTransform((pixel_coordinates1), (pixel_coordinates_utm_float))
H,_=cv2.findHomography((pixel_coordinates1), (pixel_coordinates_utm_float))
H2,_=cv2.findHomography((pixel_coordinates_utm_float),(pixel_coordinates1) )
# pixel_coordinates1 = pixel_coordinates1.astype(np.float32)
# pixel_coordinates_utm_float=pixel_coordinates_utm_float.astype(np.float32)
# P = cv2.getPerspectiveTransform((pixel_coordinates1), (pixel_coordinates_utm_float))
# 打印转换矩阵
# print("透视变换perspectivetranform的转换矩阵:",P)
print("透视变换findhomo的转换矩阵:",H)
print("透视变换findhomo的逆转换矩阵:",H2)


#----------------------------------------------------------选点并给出经纬度（check）---------------------------------
img = imread(image_path)
fig, ax = plt.subplots(figsize=(32, 24))
ax.imshow(img)
plt.title("Select your points")
plt.axis('on')

pixel_coordinates_select = []
wld_coordinates_select = []

# 创建一个 UTM 到 WGS84 经纬度的转换器
transformer_t = Transformer.from_crs("epsg:32649", "epsg:4326")
while True:
    choice = input("是否继续选择点？(yes/no): ")
    if choice.lower() == "no":
        break
    print("请点击图像选择一个点")
    point = plt.ginput(1, show_clicks=True)
    x, y = point[0]
    pixel_coordinates_select.append((x, y))

    # 将像素点坐标转换为UTM坐标

    utm_coord = np.dot(H, np.array([x, y, 1]))
    utm_coord = utm_coord[:2] / utm_coord[2]
    print("当前点的utm坐标:", utm_coord)

    
        
  
    lat, lon = transformer_t.transform(utm_coord[0], utm_coord[1])
    wld_coordinates_select.append((lon,lat))
    print("当前点的经纬度坐标:", wld_coordinates_select[-1])

    plt.plot(x, y, 'ro', markersize=1)
    ax.text(x, y, f'({lat:.6f}, {lon:.6f})', fontsize=8, color='black', ha='right')
    plt.draw()

print("所有选点坐标经纬度:")
for i, coord in enumerate(wld_coordinates_select):
    print(f"点{i+1}: {coord}")

plt.close()
