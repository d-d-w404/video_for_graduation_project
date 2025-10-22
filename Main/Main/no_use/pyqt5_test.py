import cv2
import image_processing
import numpy as np

global img
global point1, point2
global g_rect


def on_mouse(event, x, y, flags, param):
    global img, point1, point2, g_rect
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击,则在原图打点
        print("1-EVENT_LBUTTONDOWN")
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        cv2.imshow('image', img2)

    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳，画框
        print("2-EVENT_FLAG_LBUTTON")
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('image', img2)

    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放，显示
        print("3-EVENT_LBUTTONUP")
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), thickness=2)
        cv2.imshow('image', img2)
        if point1 != point2:
            min_x = min(point1[0], point2[0])
            min_y = min(point1[1], point2[1])
            width = abs(point1[0] - point2[0])
            height = abs(point1[1] - point2[1])
            g_rect = [min_x, min_y, width, height]
            cut_img = img[min_y:min_y + height, min_x:min_x + width]
            cv2.imshow('ROI', cut_img)

# cap = cv2.VideoCapture('vtest.avi')
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame',gray)

path="C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic/924.jpg"

video_path="C:/Users/LENOVO/Desktop/1.mp4"
cap = cv2.VideoCapture(video_path)
while(cap.isOpened()):
    ret, rgb_image = cap.read()

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    global img
    img = bgr_image
    #cv2.namedWindow('image')


    #while True:
    #cv2.setMouseCallback('image', on_mouse)
       # cv2.startWindowThread() # 加在这个位置
    cv2.imshow('image', img)
    #key = cv2.waitKey(0)
    # if key == 13 or key == 32:  # 按空格和回车键退出
    #     break
    if (cv2.waitKey(30) >= 0):
        cv2.setMouseCallback('image', on_mouse)
        cv2.waitKey(0)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#return g_rect