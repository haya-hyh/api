import math

# def calculate_points_h(point1, points2, angle_change_h):
#     """
#     计算给定点与一组点之间的新坐标，考虑水平方向的角度变化。
    
#     参数：
#     point1: tuple，起始点坐标 (x1, y1)
#     points2: list，包含多个点的列表 [(x2_1, y2_1), (x2_2, y2_2), ...]
#     angle_change_h: float，水平方向的角度变化
    
#     返回值：
#     new_points2: list，新的点坐标列表 [(x2_1_, y2_1_), (x2_2_, y2_2_), ...]
#     """
#     new_points2 = []
#     for point2 in points2:
#         # 解析点的坐标
#         x1, y1 = point1
#         x2, y2 = point2

#         # 计算两点之间的距离
#         distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#         # 计算直线的斜率
#         if x2 - x1 != 0:
#             slope = (y2 - y1) / (x2 - x1)
#         else:
#             slope = float('inf')  # 处理斜率为无穷大的情况

#         # 计算直线与 x 轴的夹角（弧度）
#         angle_radians = math.atan(slope)

#         # 将弧度转换为角度
#         angle_degrees = math.degrees(angle_radians)

#         # 计算与 x 轴正方向的夹角
#         if x2 > x1:  # 点2在点1的右方
#             angle_degrees = angle_degrees % 360
#         else:  # 点2在点1的左方
#             angle_degrees = (180 + angle_degrees) % 360

#         # 将角度转换为新的摄像头转动角度
#         angle_degrees += angle_change_h

#         # 计算新的取点坐标
#         angle_radians = math.radians(angle_degrees)
#         x2_ = x1 + distance * math.cos(angle_radians)
#         y2_ = y1 + distance * math.sin(angle_radians)

#         new_points2.append((x2_, y2_))

#     return new_points2
# import math

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

# def calculate_points_v(point1, points2, h, angle_change_v):
#     """
#     计算给定点与一组点之间的新坐标，考虑垂直方向的角度变化。
    
#     参数：
#     point1: tuple，摄像机坐标 (x1, y1)
#     points2: list，包含多个点的列表 [(x2_1, y2_1), (x2_2, y2_2), ...]
#     h: float，相机高度‘
#     angle_change_v: float，垂直方向的角度变化
    
#     返回值：
#     new_points2: list，新的点坐标列表 [(x2_1_, y2_1_), (x2_2_, y2_2_), ...]
#     """
#     new_points2 = []
#     for point2 in points2:
#         # 解析点的坐标
#         x1, y1 = point1
#         x2, y2 = point2

#         # 计算两点之间的欧氏距离
#         distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#         # 计算正切值
#         tan_value = h / distance

#         # 计算旋转角度后的弧度
#         angle_radians = math.atan(tan_value)
#         angle_degrees = math.degrees(angle_radians)
#         angle_degrees += angle_change_v

#         # 将角度转换为弧度
#         angle_radians = math.radians(angle_degrees)

#         # 计算旋转后的正切值
#         tan_value = math.tan(angle_radians)

#         # 计算 x 坐标
#         x = h / tan_value

#         # 计算距离1
#         distance1 = distance - x

#         # 计算 t
#         t = distance1 / distance

#         # 计算点 C 的坐标
#         Cx = (1 - t) * x1 + t * x2
#         Cy = (1 - t) * y1 + t * y2

#         new_points2.append((Cx, Cy))

#     return new_points2
import math

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

import math

# def calculate_points_v(point1, points2, h, angle_change_v):
#     """
#     计算给定点与一组点之间的新坐标，考虑垂直方向的角度变化。
    
#     参数：
#     point1: tuple，摄像机坐标 (x1, y1)
#     points2: list，包含多个点的列表 [(x2_1, y2_1), (x2_2, y2_2), ...]
#     h: float，相机高度
#     angle_change_v: float，垂直方向的角度变化
    
#     返回值：
#     new_points2: list，新的点坐标列表 [(x2_1_, y2_1_), (x2_2_, y2_2_), ...]
#     """
#     new_points2 = []
    
#     # 计算角度变化对应的弧度
#     angle_radians_change = math.radians(angle_change_v)
    
#     for point2 in points2:
#         # 解析点的坐标
#         x1, y1 = point1
#         x2, y2 = point2

#         # 计算两点之间的欧氏距离
#         distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#         # 计算旋转角度后的弧度
#         angle_radians = math.atan(h / distance) + angle_radians_change
#         angle_degrees = math.degrees(angle_radians)

#         # 计算距离1
#         x = h / math.tan(angle_radians)

#         # 计算 t
#         t = (distance - x) / distance

#         # 计算点 C 的坐标
#         Cx = (1 - t) * x1 + t * x2
#         Cy = (1 - t) * y1 + t * y2

#         new_points2.append((Cx, Cy))

#     return new_points2


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
