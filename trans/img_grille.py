import get_utm_transform as getu
import numpy as np
import matplotlib.pyplot as plt

# 输入
img = input("请输入要打开的图片路径：")
H = input("请输入转换矩阵（世界坐标到图像坐标）：")



H = np.array(H)
# 计算四角坐标
def calculate_other_diagonals(coordinates):
    print("Coordinates:", coordinates)  # 调试打印
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

print(pixel_coordinates_w_all)
pixel_coordinates = []
for i in range(0, len(pixel_coordinates_w_all), 2): 
       pixel_coordinates.append([pixel_coordinates_w_all[i], pixel_coordinates_w_all[i+1]] ) 
print(pixel_coordinates)



# 绘制图片
plt.figure(figsize=(32, 24))
plt.imshow(img)

# 转换并绘制每组坐标
for idx, pixel_coordinates_w in enumerate(pixel_coordinates):
    coordinates_four_w = calculate_other_diagonals(pixel_coordinates_w)
    coordinates_utm = getu.convert_to_utm(coordinates_four_w)
    MH = H

    
    coordinates_utm_float = np.array([(float(x), float(y)) for x, y in coordinates_utm])
    print(coordinates_utm_float)
    

    coordinates_pixel = [np.dot(MH, np.array([x, y, 1])) for x, y in coordinates_utm_float]

    coordinates_pixel = [coord[:2] / coord[2] for coord in coordinates_pixel]

    # 标出坐标点
    # for coord in coordinates_pixel:
    #     plt.scatter(coord[0], coord[1], color='red')

    # 连接四个点成四边形
    coordinates_pixel.append(coordinates_pixel[0])
    coordinates_pixel = np.array(coordinates_pixel)
    plt.plot(coordinates_pixel[:, 0], coordinates_pixel[:, 1], marker='o', color='blue', linestyle='-')
plt.draw()

plt.title("All Rectangles")  # 添加标题
plt.savefig('./result_img/all_pixel_grilles.png')

