import cv2 as cv
import os

#这个函数主要用于导入视频源，然后通过Opencv截取每条帧，然后存储在temp_pic中并逐帧播放
#URL是视频源
#path是我暂时存储的地方
def load_pic(URL,temp_path):

    # #视频源地址
    # URL='C:/Users/LENOVO/Desktop/1.mp4'
    #
    # #暂时存储图片地址
    # path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'

    #视频捕捉
    #cap = cv.VideoCapture(0) 这是用来链接摄像头的
    cap = cv.VideoCapture(URL)

    count=1

    while(True):
        # 一帧一帧捕捉
        # URL = 'C:/Users/LENOVO/Desktop/1.mp4'
        # vcap = cv.VideoCapture(URL)
        ret, frame = cap.read()

        if (ret):
            #存储下面准备播放的图片
            cv.imwrite(os.path.join(temp_path, str(count)+'.jpg'), frame)
            count=count+1

            # 我们对帧的操作在这里
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # 播放图片
            cv.imshow('frame',frame)
        else:
            #这个是导入完整个视频后结束
            break

        #这个是可以进行中途的断开
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # 当所有事完成，释放 VideoCapture 对象
    cap.release()
    cv.destroyAllWindows()
