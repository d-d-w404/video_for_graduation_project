from draw_bounding_box import DrawBoundingBox
import cv2
from functools import partial


def get_box_info(self):
    return [('prasanna', [10, 10, 150, 150]), ('reyaan', [250, 250, 400, 400])]


def image_from_cv(read):
    # return None if ret == False else return frame
    ret, frame = read()
    return frame if ret else None

'''
ret, frame = cap.read()返回值含义：
参数ret 为True 或者False,代表有没有读取到图片
第二个参数frame表示截取到一帧的图片
'''





URL='C:/Users/LENOVO/Desktop/1.mp4'
#URL = '/home/zf/1.mp4'
vcap = cv2.VideoCapture(URL)
bbox = DrawBoundingBox(get_box_info, partial(image_from_cv, read=vcap.read))
bbox.run()

#我发现当函数做参数的时候，似乎不需要加()，只要函数名即可，见上read=vcap.read