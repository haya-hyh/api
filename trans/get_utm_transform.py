'''
WGS84的经纬度 转 UTM的x,y
'''
from pyproj import Transformer
import numpy as np
# 参数1：WGS84地理坐标系统 对应 4326 
# 参数2：坐标系WKID 东莞市 WGS_1984_UTM_Zone_49N 对应 32649
def convert_to_utm(pixel_coordinates_w, from_crs="epsg:4326", to_crs="epsg:32649"):
    """
    将像素坐标转换为UTM坐标
    
    参数：
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

def convert_to_latilon(pixel_coordinates, from_crs="epsg:32649", to_crs="epsg:4326"):
    """
    将像素坐标转换为UTM坐标
    
    参数：
    pixel_coordinates_w: list，像素坐标组，每个元素是一个二元元组 (x, y)
    from_crs: str，输入坐标系，默认为WGS84 (EPSG:4326)
    to_crs: str，输出坐标系，默认为UTM Zone 49N (EPSG:32649)
    
    返回值：
    pixel_coordinates_utm: list，UTM坐标组，每个元素是一个二元元组 (x, y)
    """    
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
