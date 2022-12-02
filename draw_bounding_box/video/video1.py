import cv2


def onTrackbarSlide(pos):
    global cap
    cap.set(0, pos * 1000)

def video_player(cap):
    fps = cap.get(5)  # 帧速率cv2.CAP_PROP_FPS，单位：帧数/秒
    fcount = cap.get(7)  # 获得视频总帧数
    seccount = int(fcount/fps)  # 计算出视频总时长，单位：秒

    cv2.namedWindow('MyWindow', 1)  # 创建窗口
    cv2.createTrackbar('TimePos', 'MyWindow', 0, seccount, onTrackbarSlide)  # 创建滑动条和回调函数
    while (cap.isOpened()):
        _, frame = cap.read()
        cv2.imshow('MyWindow', frame)

        curtime = int(cap.get(0) / 1000)  # 获得当前时间，单位：秒
        cv2.setTrackbarPos('TimePos', 'MyWindow', curtime)  # 更新滑动条上的位置

        if cv2.waitKey(int(fps)) in [ord('q'), 27]:  # 按q或esc结束
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = r'C:\Work\python\python_project\video_for_graduation_project\draw_bounding_box\video\1.mp4'
    cap = cv2.VideoCapture(video_path)
    video_player(cap)