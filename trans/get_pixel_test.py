import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.image import imread

def select_points_and_transform(image_path, H,pix_coor):
    """
    选择点并将其转换为经纬度坐标
    
    参数：
    image_path: str，图像文件路径
    H: numpy数组，转换矩阵
    
    返回值：
    wld_coordinates_select: list，选定点的经纬度坐标列表
    """
    # 读取图像
    img = imread(image_path)
    fig, ax = plt.subplots(figsize=(32, 24))
    ax.imshow(img)
    plt.title("Select your points")
    plt.axis('on')
    pix_coor = np.append(pix_coor, [pix_coor[0]], axis=0)
    plt.plot(pix_coor[:, 0], pix_coor[:, 1], marker='o', color='blue', linestyle='-',linewidth=1)
    wld_coordinates_select = []

    # 创建一个 UTM 到 WGS84 经纬度的转换器
    transformer_t = Transformer.from_crs("epsg:32649", "epsg:4326")    

    test_coor_wld = []
    for x,y in pix_coor:
        pix_coor_1 = np.dot(H, np.array([x, y, 1]))
        pix_coor_2 = pix_coor_1[:2] / pix_coor_1[2]
        lat, lon = transformer_t.transform(pix_coor_2[0], pix_coor_2[1])
        test_coor_wld.append((lon,lat))
    print(test_coor_wld)

    while True:
        choice = input("是否继续选择点？(yes/no): ")
        if choice.lower() == "no":
            break
        print("请点击图像选择一个点")
        point = plt.ginput(1, show_clicks=True)
        x, y = point[0]

        # 将像素点坐标转换为UTM坐标
        utm_coord = np.dot(H, np.array([x, y, 1]))
        utm_coord = utm_coord[:2] / utm_coord[2]

        lat, lon = transformer_t.transform(utm_coord[0], utm_coord[1])
        wld_coordinates_select.append((lon,lat))
        
        # 在图上标记点并显示坐标
        ax.plot(x, y, 'ro', markersize=5)  # 在图上标点
        ax.text(x, y, f'({lat:.6f}, {lon:.6f})', fontsize=8, color='black', ha='right')  # 在点旁边添加坐标文本
        print("坐标:",lat,lon)
        plt.draw()
    plt.show()
    
    
    for x,y in pix_coor:
      utm_coord_ = np.dot(H, np.array([x, y, 1]))
      utm_coord_ = utm_coord_[:2] / utm_coord_[2]
      print(utm_coord_)
    return wld_coordinates_select
# def select_points_and_transform(image_path, H):
#     """
#     选择点并将其转换为经纬度坐标
    
#     参数：
#     image_path: str，图像文件路径
#     H: numpy数组，转换矩阵
    
#     返回值：
#     wld_coordinates_select: list，选定点的经纬度坐标列表
#     """
#     # 读取图像
#     img = imread(image_path)
#     fig, ax = plt.subplots(figsize=(8, 6))
#     ax.imshow(img)
#     plt.title("Select your points")
#     plt.axis('on')

#     wld_coordinates_select = []

#     # 创建一个 UTM 到 WGS84 经纬度的转换器
#     transformer_t = Transformer.from_crs("epsg:32649", "epsg:4326")
#     while True:
#         choice = input("是否继续选择点？(yes/no): ")
#         if choice.lower() == "no":
#             break
#         print("请点击图像选择一个点")
#         point = plt.ginput(1, show_clicks=True)
#         x, y = point[0]

#         # 将像素点坐标转换为UTM坐标
#         utm_coord = np.dot(H, np.array([x, y, 1]))
#         utm_coord = utm_coord[:2] / utm_coord[2]

#         lat, lon = transformer_t.transform(utm_coord[0], utm_coord[1])
#         wld_coordinates_select.append((lon,lat))

#     plt.close()
#     return wld_coordinates_select

# 示例用法
# image_path = input("请输入要打开的图片路径：")
# H = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # 这里仅作为示例，你需要提供实际的转换矩阵
# wld_coordinates_select = select_points_and_transform(image_path, H)
# print("所有选点坐标经纬度:")
# for i, coord in enumerate(wld_coordinates_select):
#     print(f"点{i+1}: {coord}")
