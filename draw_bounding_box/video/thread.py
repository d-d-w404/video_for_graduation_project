import threading, time


import video
import timecount
# video
# timecount
def fuc():
    while True:
        print("kid")

# 2.创建子线程：thread类
if __name__ == '__main__':
    t1 = threading.Thread(target=video)
    t2 = threading.Thread(target=fuc())

    # 3. 守护线程 setDaemon()  语法：子线程名.setDaemon()
    # 主线程执行完，子线程也跟着结束，默认False，要True
    t1.setDaemon(True)
    t2.setDaemon(True)

    # 4. 开启子线程  start()
    t1.start()
    t2.start()
    # # 5.阻塞线程
    # t1.join()
    # t2.join()
    # # 6.获得线程名
    # print(t1.getName())
    # print(t2.getName())
    #
    # print('大家学习的不错')