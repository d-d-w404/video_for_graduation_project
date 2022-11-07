import numpy as np
import cv2 as cv
import os
import count


#path是暂时存储整个视频帧的地方
#target_path是找到投篮帧，然后存储的地方
#target_range是我最终找到的投篮帧的个数范围
def search(temp_path,target_path,target_range):
    # path = 'C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'
    # target_path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic'
    # 统一规定这里的range是left和right的差值
    # target_range = 10

    left = 1
    right = count.count_file_number(temp_path)
    real_range = right - left

    #做一个容器，保留我曾经访问过的图片的编号，为了能够回退
    memo=[]

    while(real_range>target_range):
        point=(int)((left+right)/2)
        print(left," ",point," ",right)
        #根据信息画出指定的图片
        img = cv.imread(temp_path + '/'+str(point)+'.jpg', 0)
        cv.imshow('image', img)

        memo.append([left,point,right])

        # 通过按键进行二分搜索，并且更新range值
        k = cv.waitKey(0)
        if k==ord('a'):
            left=left
            right=point
            real_range=right-left
            cv.destroyAllWindows()
        elif k == ord('d'):
            left=point
            right=right
            real_range = right - left
            cv.destroyAllWindows()
        elif k == 27:  # ESC 退出
            cv.destroyAllWindows()
            break
        elif len(memo)>1 and k == ord('r'):  # 设计一个可以反悔的按键，用与回退回错误判断前
            memo.pop(-1)
            left=memo[-1][0]
            right=memo[-1][2]
            real_range=right-left
            #这里需要再删除一下，因为上面在返回之后又会记录一次
            memo.pop(-1)
            cv.destroyAllWindows()
    else:
        for i in range(left,right+1):#左闭右开
            cv.waitKey(500)
            img = cv.imread(temp_path + '/' + str(i) + '.jpg', 0)
            cv.imshow('image', img)
            cv.imwrite(os.path.join(target_path, str(i)+'.jpg'), img)



#用于测试
# 暂时存储图片地址
temp_path = 'C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'
# 找到投篮帧后存储的地址
target_path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic'
# 目标帧数,二分法结束的范围
target_range=10
search(temp_path,target_path,target_range)
