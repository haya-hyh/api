from pyproj import Transformer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.image import imread
import math

#读取图片点击位置的像素坐标并通过转换矩阵转换为经纬度
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

#转换经纬度坐标到utm
def convert_to_utm(pixel_coordinates_w, from_crs="epsg:4326", to_crs="epsg:32649"):
    """
    将像素坐标转换为UTM坐标
    
    参数：
    参数1：WGS84地理坐标系统 对应 4326 
    参数2：坐标系WKID 东莞市 WGS_1984_UTM_Zone_49N 对应 32649    
    pixel_coordinates_w: list，像素坐标组，每个元素是一个二元元组 (x, y)
    from_crs: str，输入坐标系，默认为WGS84 (EPSG:4326)
    to_crs: str，输出坐标系，默认为UTM Zone 49N (EPSG:32649)
    
    返回值：
    pixel_coordinates_utm: list，UTM坐标组，每个元素是一个二元元组 (x, y)
    """    
    # 创建坐标转换器
    transformer = Transformer.from_crs(from_crs, to_crs)
    
    # 将像素坐标转换为UTM坐标
    pixel_coordinates_utm = []
    for x, y in pixel_coordinates_w:
        utm_x, utm_y = transformer.transform(x, y)  # 注意纬度在前，经度在后
        utm_x = "{:.14f}".format(utm_x)
        utm_y = "{:.14f}".format(utm_y)
        pixel_coordinates_utm.append((utm_x, utm_y))
        
    return pixel_coordinates_utm


def convert_to_utm(pixel_coordinates_w, from_crs="epsg:4326", to_crs="epsg:32649"):
    """
    将像素坐标转换为UTM坐标
    
    参数：
    参数1：WGS84地理坐标系统 对应 4326 
    参数2：坐标系WKID 东莞市 WGS_1984_UTM_Zone_49N 对应 32649    
    pixel_coordinates_w: tuple or list，像素坐标，可以是一个二元元组 (x, y)，也可以是包含多个二元元组的列表 [(x1, y1), (x2, y2), ...]
    from_crs: str，输入坐标系，默认为WGS84 (EPSG:4326)
    to_crs: str，输出坐标系，默认为UTM Zone 49N (EPSG:32649)
    
    返回值：
    如果输入是单个坐标，则返回一个二元元组 (x, y)；
    如果输入是坐标列表，则返回包含多个二元元组的列表 [(x1, y1), (x2, y2), ...]
    """    
    # 创建坐标转换器
    transformer = Transformer.from_crs(from_crs, to_crs)
    
    # 将像素坐标转换为UTM坐标
    if isinstance(pixel_coordinates_w, tuple):  # 如果输入是单个坐标
        x, y = pixel_coordinates_w
        utm_x, utm_y = transformer.transform(x, y)  # 注意纬度在前，经度在后
        utm_x = "{:.14f}".format(utm_x)
        utm_y = "{:.14f}".format(utm_y)
        return (utm_x, utm_y)
    elif isinstance(pixel_coordinates_w, list):  # 如果输入是坐标列表
        pixel_coordinates_utm = []
        for x, y in pixel_coordinates_w:
            utm_x, utm_y = transformer.transform(x, y)  # 注意纬度在前，经度在后
            utm_x = "{:.14f}".format(utm_x)
            utm_y = "{:.14f}".format(utm_y)
            pixel_coordinates_utm.append((utm_x, utm_y))
        return pixel_coordinates_utm
    else:
        raise TypeError("Input pixel_coordinates_w must be a tuple or a list of tuples.")

#转换utm坐标到经纬度
def convert_to_latilon(pixel_coordinates, from_crs="epsg:32649", to_crs="epsg:4326"):
    # 创建坐标转换器
    transformer = Transformer.from_crs(from_crs, to_crs)
    
    # 将像素坐标转换为latilon坐标
    pixel_coordinates_w = []
    for x, y in pixel_coordinates:
        w_x, w_y = transformer.transform(x, y)  # 注意纬度在前，经度在后
        w_x = "{:.14f}".format(w_x)
        w_y = "{:.14f}".format(w_y)
        pixel_coordinates_w.append((w_x, w_y))        
    return pixel_coordinates_w

#连成闭合获取角点坐标但最后一个点会删除
def get_pixel_coordinates(image_path):
    # 创建空数组用于保存像素坐标
    pixel_coordinates = []
    
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
            pixel_coordinates.append(point[0])
            print("像素坐标:", point[0])

            # 在图上添加一个小点以标记所选位置
            ax.add_patch(Circle((point[0][0], point[0][1]), 2, color='r'))

            # 重新绘制图形以更新小点和连线
            plt.draw()
            # 绘制连接点的线段形成多边形
            if len(pixel_coordinates) >= 2:
                ax.plot([pixel_coordinates[-2][0], pixel_coordinates[-1][0]],
                        [pixel_coordinates[-2][1], pixel_coordinates[-1][1]], 'r')
                
        # 删除最后一个坐标
        pixel_coordinates = pixel_coordinates[:-1] 
        print("保存的像素坐标:", pixel_coordinates)
    except FileNotFoundError:
        print("找不到指定的图片文件，请确认路径是否正确。")
        return None
    except Exception as e:
        print("发生错误:", e)
        return None
    
    plt.close()  # 显式关闭Matplotlib图形
    return pixel_coordinates



def calculate_points_h(point1, points2, angle_change_h):
    """
    计算给定摄像机坐标点与一组世界坐标点之间的新坐标，考虑水平方向的角度变化。

    参数：
    point1: tuple,摄像机坐标 (x1, y1)
    points2: list,包含多个点的列表 [(x2_1, y2_1), (x2_2, y2_2), ...]
    angle_change_h: float,摄像机水平方向的角度变化
    
    返回值：
    new_points2: list,新的点坐标列表 [(x2_1_, y2_1_), (x2_2_, y2_2_), ...]
    """
    # 解析点的坐标
    x1, y1 = point1

    # 计算摄像机投影在平面的点到所有点的角度和距离
    angles = []
    distances = []
    for point2 in points2:
        x2, y2 = point2

        # 计算两点之间的距离
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distances.append(distance)

        # 计算两点之间的角度（弧度）
        angle = math.atan2(y2 - y1, x2 - x1)
        angles.append(angle)

    # 计算摄像头转动角度
    new_angle_h = math.radians(angle_change_h)

    # 计算新的坐标点
    new_points2 = []
    for distance, angle in zip(distances, angles):
        new_angle = angle + new_angle_h
        x2_ = x1 + distance * math.cos(new_angle)
        y2_ = y1 + distance * math.sin(new_angle)
        new_points2.append((x2_, y2_))

    return new_points2
def calculate_points_v(point1, points2, h, angle_change_v):
    """
    计算给定摄像机坐标点与一组坐标点得出的新坐标，考虑垂直方向的角度变化。
    
    参数：
    point1: tuple,摄像机坐标 (x1, y1)
    points2: list,包含多个点的列表 [(x2_1, y2_1), (x2_2, y2_2), ...]
    h: float,相机高度
    angle_change_v: float,垂直方向的角度变化
    
    返回值：
    new_points2: list,新的点坐标列表 [(x2_1_, y2_1_), (x2_2_, y2_2_), ...]
    """
    new_points2 = []
    for point2 in points2:
        # 解析点的坐标
        x1, y1 = point1
        x2, y2 = point2

        # 计算两点之间的欧氏距离
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # 计算旋转角度后的弧度
        angle_radians = math.atan(h / distance)
        angle_degrees = math.degrees(angle_radians + math.radians(angle_change_v))

        # 计算距离 x
        x = h / math.tan(math.radians(angle_degrees))

        # 计算 t （OA'/OA）
        t = x / distance

        # 计算点 C 的坐标
        Cx = (1 - t) * x1 + t * x2
        Cy = (1 - t) * y1 + t * y2

        new_points2.append((Cx, Cy))

    return new_points2

#计算像素坐标对应的新utm坐标
def get_new_utmposition(point1,ps,h_angle,v_angle=0,high=0):
    if v_angle !=0:
        ps1 = calculate_points_v(point1, ps,high, v_angle)
    else:
        ps1 = ps
    if h_angle !=0:
        new_ps = calculate_points_h(point1, ps1, h_angle)
    else:
        new_ps = ps1
    return new_ps

#在图片上画出网格
def draw_pixel_grilles(img_path, H_matrix):
    # 读取图片
    img = plt.imread(img_path)

    H = np.array(H_matrix)

    # 计算四角坐标
    def calculate_other_diagonals(coordinates):
        coord1 = coordinates[0]
        coord2 = coordinates[1]
        diagonal_coord3 = [coord1[0], coord2[1]]
        diagonal_coord4 = [coord2[0], coord1[1]]
        return [coord1, diagonal_coord3, coord2, diagonal_coord4]

    # 读取所有坐标点
    pixel_coordinates_w_all = []
    with open('./data/grille.txt', 'r') as file:
        lines = file.readlines()
    coordinates = ''.join(lines).replace('[', '').replace(']', '').split(',')

    # 将每两个连续的字符串转换为浮点数，并组成坐标点列表
    pixel_coordinates_w_all = []
    for i in range(0, len(coordinates), 2):
        x = float(coordinates[i])
        y = float(coordinates[i + 1])
        pixel_coordinates_w_all.append([x, y])

    pixel_coordinates = []
    for i in range(0, len(pixel_coordinates_w_all), 2): 
        pixel_coordinates.append([pixel_coordinates_w_all[i], pixel_coordinates_w_all[i+1]] ) 

    # 绘制图片
    plt.figure(figsize=(32, 24))
    plt.imshow(img)

    # 转换并绘制每组坐标
    for idx, pixel_coordinates_w in enumerate(pixel_coordinates):
        coordinates_four_w = calculate_other_diagonals(pixel_coordinates_w)
        MH = H
        
        #  convert_to_utm 
        coordinates_utm = convert_to_utm(coordinates_four_w)

        coordinates_utm_float = np.array([(float(x), float(y)) for x, y in coordinates_utm])

        coordinates_pixel = [np.dot(MH, np.array([x, y, 1])) for x, y in coordinates_utm_float]

        coordinates_pixel = [coord[:2] / coord[2] for coord in coordinates_pixel]

        # 连接四个点成四边形
        coordinates_pixel.append(coordinates_pixel[0])
        coordinates_pixel = np.array(coordinates_pixel)
        plt.plot(coordinates_pixel[:, 0], coordinates_pixel[:, 1], marker='o', color='blue', linestyle='-')
    
    plt.title("All Rectangles")  # 添加标题
    plt.savefig('./result_img/all_pixel_grilles.png')


