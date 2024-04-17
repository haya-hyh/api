import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.image import imread

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

# 示例用法
if __name__ == "__main__":
    image_path1 = "01.jpg"
    recorded_coordinates = get_pixel_coordinates(image_path1)
    print(recorded_coordinates)