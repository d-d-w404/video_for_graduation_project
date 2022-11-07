import load
import search

# 视频源地址
URL = 'C:/Users/LENOVO/Desktop/1.mp4'

# 暂时存储图片地址
temp_path = 'C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'

# 找到投篮帧后存储的地址
target_path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic'

# 目标帧数,二分法结束的范围
target_range=10

load.load_pic(URL,temp_path)
search.search(temp_path,target_path,target_range)

