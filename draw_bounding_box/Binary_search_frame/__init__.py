import numpy as np
import cv2 as cv
import os
import shutil

def image_from_cv(read):
    # return None if ret == False else return frame
    ret, frame = read()
    return frame if ret else None



#视频源地址
URL='C:/Users/LENOVO/Desktop/1.mp4'

#暂时存储图片地址
path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'

# def delete():
#     shutil.rmtree(path,ignore_errors = False,onerror = None)

#视频捕捉
#cap = cv.VideoCapture(0) 这是用来链接摄像头的
cap = cv.VideoCapture(URL)

count=0

while(True):
    # 一帧一帧捕捉
    # URL = 'C:/Users/LENOVO/Desktop/1.mp4'
    # vcap = cv.VideoCapture(URL)
    ret, frame = cap.read()

    #存储下面准备播放的图片
    cv.imwrite(os.path.join(path, str(count)+'.jpg'), frame)
    count=count+1

    # 我们对帧的操作在这里
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 播放图片
    cv.imshow('frame',frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# 当所有事完成，释放 VideoCapture 对象
cap.release()
cv.destroyAllWindows()



