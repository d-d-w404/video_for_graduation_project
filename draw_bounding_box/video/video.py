import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import cv2
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtCore import Qt



global img
global point1, point2
global g_rect

global text_0
global text_1
global text_2
global text_3
text_0=""
text_1=""
text_2=""
text_3=""

#这个是为了最后导出通过这个软件收集的数据，而设定的文件地址和名称
global source_file_name
global target_file_name
global target_file_path

source_file_name="C:/Users/Wander/Desktop/Graduation_Project/train"
target_file_name=""
target_file_path="C:/Users/Wander/Desktop/Graduation_Project/output"

class Video(QWidget):
    def __init__(self):
        super(Video, self).__init__()

        #下面的一段代码需要在每次导入新文件后重新初始化一次
        #否则就会出现第一个帧的数目递增和视频播放速度变快的问题
        self.frame = []  # 存图片
        self.detectFlag = False  # 检测flag
        self.cap = []
        self.timer_camera = QTimer()  # 定义定时器


        self.timefps=1 #这个是每一张图片间隔的时间
        self.start_time = 0
        #self.curtime=0

        self.frame_count = 0   # 帧数,这个参数可以用cap.get(1)去得到
        self.frame_all =0 #全部的幀數
        self.PauseFlag=True
        self.flag=True #这个flag用于我拖动滑条时，让其不会在拖动的过程中自己自动播放
        self.change_count=0

        self.fps = 0  # 帧速率cv2.CAP_PROP_FPS，单位：帧数/秒
        self.fcount = 0  # 获得视频总帧数
        self.seccount = 0  # 计算出视频总时长，单位：秒

        self.lock=False #这个是为了让刚导入一个视频处于暂停状态

        self.left=0
        self.right=100
        self.range=0

        #这是为了二分法能够回退做的容器
        self.memo=[]

        #这个是左右界的标签的位置记录，因为我的标签是通过label设置的，而且最后会通过int实现一个进位
        #如果使用了r，回退，就会容易使标签发生移位
        #self.memo_label=[]

        self.target_label=""
        self.left_right_lock=False

        self.temp_filename=''


        # 外框
        self.resize(1400, 650)
        self.setWindowTitle("播放器-抽帧-boundingbox")

        # 图片label
        #self.label = QLabel(self)
        self.label=myLabel(self)
        self.label.setText("Waiting for video...")
        self.label.setFixedSize(900, 450)  # width height
        self.label.move(50, 50)
        self.label.setStyleSheet("QLabel{background:black;}"
                                 "QLabel{color:lime;font-size:15px;font-weight:bold;font-family:宋体;}"
                                 )

        #设置一个可以实时查询文件的下拉框
        self.model = QDirModel()
        self.tree = QTreeView(self)
        self.tree.allColumnsShowFocus()
        self.tree.move(960,0)
        self.tree.setFixedSize(430,500)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(source_file_name))
        self.tree.clicked.connect(self.show_info)

        self.tree.doubleClicked.connect(self.tree_cilcked)


        #左右边界的标签,每个视频由于帧数长度不同，所以开始的时候也需要不同的位置
        self.left_label=QLabel(self)
        self.left_label.setStyleSheet("QLabel{background:cyan;}")
        self.left_label.setFixedSize(3,50)
        #self.left_label.move(50+1 +5,500)

        self.right_label=QLabel(self)
        self.right_label.setStyleSheet("QLabel{background:crimson;}")
        self.right_label.setFixedSize(3,50)
        #self.right_label.move(950-1 -9,500)



        # 显示人数label
        self.label_num = QLabel(self)
        self.label_num.setText("视频相关信息：" +
                               "      帧数：" + str(round(self.frame_count, 2))+
                               "      左边界：" + str(self.left)+
                               "      右边界：" + str(self.right)+
                               "      投篮帧范围："+str(self.right-self.left)
                               )
        self.label_num.setFixedSize(900, 50)  # width height
        self.label_num.move(50, 0)
        self.label_num.setStyleSheet("QLabel{background:aqua;}")

        #播放器滑动条
        # 设置最大最小值
        self.sld=QSlider(Qt.Horizontal, self)
        self.sld.setMaximum(800)
        self.sld.setMinimum(0)
        self.sld.setSingleStep(1) # 设置单步值
        self.sld.setValue(1)# 设置初始值
        self.sld.setTickPosition(QSlider.TicksAbove)# 设置刻度线位置
        self.sld.setFixedSize(900, 50)  # width height
        self.sld.move(50, 525)
        #self.sld.valueChanged.connect(self.changevalue)# 设置信号与槽

        self.sld.sliderPressed.connect(self.k1)
        self.sld.sliderMoved.connect(self.changevalue)
        self.sld.sliderReleased.connect(self.k2)

        # 开启视频按键
        self.btn = QPushButton(self)
        self.btn.setText("Load")
        self.btn.setFixedSize(50,50)
        self.btn.move(50, 580)
        self.btn.clicked.connect(self.slotStart)

        # 关闭视频按钮
        self.btn_stop = QPushButton(self)
        self.btn_stop.setText("Stop")
        self.btn_stop.setFixedSize(50,50)
        self.btn_stop.move(150, 580)
        self.btn_stop.clicked.connect(self.slotStop)

        # 暂停键
        self.btn_pause = QPushButton(self)
        self.btn_pause.setText("Pause")
        self.btn_pause.setFixedSize(50,50)
        self.btn_pause.move(250, 580)
        self.btn_pause.setStyleSheet("QPushButton{background:green;}")
        self.btn_pause.clicked.connect(self.slotPause)

        # 确定采集到的数据存放的文件夹地址
        self.btn_file_path = QPushButton(self)
        self.btn_file_path.setText("FILE_PATH")
        self.btn_file_path.setFixedSize(100,50)
        self.btn_file_path.move(350+300, 580)
        self.btn_file_path.clicked.connect(self.slotFile)

        # 我的视频数据来源的文件夹
        self.btn_file_path = QPushButton(self)
        self.btn_file_path.setText("SOURCE_PATH")
        self.btn_file_path.setFixedSize(100,50)
        self.btn_file_path.move(350+150, 580)
        self.btn_file_path.clicked.connect(self.slotSourceFile)

        # 键盘
        self.label_key=QLabel('',self)
        self.label_key.setFixedSize(0, 0)
        self.label_key.move(0,0)
        self.label_key.setStyleSheet("QLabel{background:black;}"
                                 "QLabel{color:rgb(100,100,100);font-size:15px;font-weight:bold;font-family:宋体;}"
                                 )
        self.label_key.grabKeyboard()   #控件开始捕获键盘
        # 只有控件开始捕获键盘，控件的键盘事件才能收到消息


        # 图片label
        #self.label = QLabel(self)
        self.label_store_data=QLabel(self)
        self.label_store_data.setText("Bounding Box information:")
        self.label_store_data.setFixedSize(430, 130)  # width height
        self.label_store_data.move(960, 500)
        self.label_store_data.setStyleSheet("QLabel{background:lightsteelblue;}"
                                 "QLabel{color:black;font-size:16px;font-weight:bold;font-family:宋体;}"
                                 )






    def show_info(self):
        index = self.tree.currentIndex()
        file_name = self.model.fileName(index)
        file_path = self.model.filePath(index)
        global target_file_name
        target_file_name=file_name

    def tree_cilcked(self, Qmodelidx):

        self.temp_filename=self.model.filePath(Qmodelidx)
        if self.temp_filename[-4:]==".avi" or self.temp_filename[-4:]==".mp4":
            self.slotStart_plus()
        # 还有比如 self.model.fileInfo(Qmodelidx).


    def slotStart(self):
        self.frame = []  # 存图片
        self.detectFlag = False  # 检测flag
        self.cap = []
        self.timer_camera = QTimer()  # 定义定时器

        self.memo = []
        self.left_right_lock = False

        global clean_out
        clean_out = False

        videoName, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.mp4;;*.avi;;All Files(*)")
        # 这个函数就是为了：当我存储数据或者更换了新的视频源后刷新暂存的数据
        global target_file_name
        #如果我一开始直接使用load，会导致程序死机，原因就是此时的targe_file_name 没有值
        target_file_name = videoName.split('/')[-1]
        self.temp_clean()

        if videoName != "":  # “”为用户取消
            self.cap = cv2.VideoCapture(videoName)

            #视频总共的帧数
            self.frame_all = (int)(self.cap.get(7)-1)#这里减1是为了避免拖动进度条到最后时发生卡住的bug
            #print(self.frame_all)
            self.left=1
            self.right=self.frame_all
            self.range=self.right-self.left

            #视频的基本参数
            self.fps = self.cap.get(5)  # 帧速率cv2.CAP_PROP_FPS，单位：帧数/秒
            self.timefps= int(1000 / self.fps)
            #print(self.timefps)

            # 左右标签的位置
            # 5和9实际上是让标签恰好对准拖动条开始和结束刻度的数据，是我试出来的
            # 而add则是不同的长度的视频的一刻度的位置不同
            add = int((self.left / self.frame_all) * 900)
            #print(add)
            self.left_label.move(50 + 1 + 5 + add, 500)

            # minus = int((1 / self.frame_all) * 900)
            self.right_label.move(950 - 1 - 9, 500)

            #通过导入新的视频，进度条也需要相应的改变
            self.sld.setMaximum(self.frame_all)
            self.sld.setValue(1)

            #有新的视频导入就需要用一次
            self.lock = False

            self.PauseFlag = True
            self.btn_pause.setStyleSheet("QPushButton{background:green;}")

            self.timer_camera.start(self.timefps)
            self.timer_camera.timeout.connect(self.openFrame)

    def slotStart_plus(self):
        self.frame = []  # 存图片
        self.detectFlag = False  # 检测flag
        self.cap = []
        self.timer_camera = QTimer()  # 定义定时器

        self.memo=[]
        self.left_right_lock = False

        global clean_out
        clean_out=False

        # 这个函数就是为了：当我存储数据或者更换了新的视频源后刷新暂存的数据
        self.temp_clean()
        self.cap = cv2.VideoCapture(self.temp_filename)

        # 视频总共的帧数
        self.frame_all = (int)(self.cap.get(7) - 1)  # 这里减1是为了避免拖动进度条到最后时发生卡住的bug
        # print(self.frame_all)
        self.left = 1
        self.right = self.frame_all
        self.range = self.right - self.left

        # 视频的基本参数
        self.fps = self.cap.get(5)  # 帧速率cv2.CAP_PROP_FPS，单位：帧数/秒
        self.timefps = int(1000 / self.fps)
        #print(self.timefps)

        # 左右标签的位置
        #5和9实际上是让标签恰好对准拖动条开始和结束刻度的数据，是我试出来的
        #而add则是不同的长度的视频的一刻度的位置不同
        add = int((self.left / self.frame_all) * 900)
        #print(add)
        self.left_label.move(50 + 1 + 5 +add, 500)

        # minus = int((1 / self.frame_all) * 900)
        self.right_label.move(950 - 1 - 9, 500)

        # 通过导入新的视频，进度条也需要相应的改变
        self.sld.setMaximum(self.frame_all)
        self.sld.setValue(1)

        # 有新的视频导入就需要用一次
        self.lock = False

        self.PauseFlag = True
        self.btn_pause.setStyleSheet("QPushButton{background:green;}")

        self.timer_camera.start(self.timefps)
        self.timer_camera.timeout.connect(self.openFrame)

    def slotStop(self):
        global clean_out
        clean_out=False
        # 这个函数就是为了：当我存储数据或者更换了新的视频源后刷新暂存的数据
        self.temp_clean()

        if self.cap != []:
            self.cap.release()
            self.timer_camera.stop()  # 停止计时器
            self.label.setText("You can choose another video on the right.")
            self.label.setStyleSheet("QLabel{background:black;}"
                                     "QLabel{color:lime;font-size:15px;font-weight:bold;font-family:宋体;}"
                                     )
        else:
            self.label_num.setText("Push the left upper corner button to Quit.")
            Warming = QMessageBox.warning(self, "Warming", "Push the left upper corner button to Quit.",
                                          QMessageBox.Yes)

    def slotPause(self):
        #self.frame_count = self.cap.get(1)#停下来的时候也要让滑条和视频的帧数保持一致
        if  self.left_right_lock==False:
            if self.PauseFlag == True:
                self.btn_pause.setStyleSheet("QPushButton{background:red;}")
                self.timer_camera.stop()  # 停止计时器
            else:
                self.btn_pause.setStyleSheet("QPushButton{background:green;}")
                self.timer_camera.start(self.timefps) #打开计时器
            self.PauseFlag = not self.PauseFlag  # 取反

    def slotFile(self):
        filename= QFileDialog.getExistingDirectory(self,"file_path","")
        global target_file_path
        target_file_path=filename

        #选定文件夹后需要马上 在界面上显现出来
        self.temp_clean()

    def slotSourceFile(self):
        filename= QFileDialog.getExistingDirectory(self,"file_path","")
        global source_file_name
        source_file_name=filename

        self.tree.setRootIndex(self.model.index(source_file_name))





    def openFrame(self):
        global clean_out
        clean_out=False

        if (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if ret  and self.flag==True:#有一个flag在，作用是我在拖动的过程中视频不会播放，只有我松开后才会继续播放

                frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                # 这是基于视频自己的播放的流程
                self.frame_count=int(self.cap.get(1))
                self.sld.setValue(self.frame_count)

                # 显示人数label
                #self.label_num = QLabel(self)
                self.label_num.setText("视频相关信息：" +
                                       "      帧数：" + str(round(self.frame_count, 2)) +
                                       "      左边界：" + str(self.left) +
                                       "      右边界：" + str(self.right) +
                                       "      投篮帧范围：" + str(self.right - self.left)
                                       )
                self.label_num.setFixedSize(900, 50)  # width height
                self.label_num.move(50, 0)
                self.label_num.setStyleSheet("QLabel{background:aqua;}")


                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width
                q_image = QImage(frame.data, width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.label.width(), self.label.height())
                self.label.setPixmap(QPixmap.fromImage(q_image))

                if self.lock == False:
                    self.lock=True
                    self.memo.append([1,1,self.frame_all])
                    self.slotPause()


    def changevalue(self):
        self.timer_camera.start(self.timefps)
        self.frame_count=self.sld.value()
        self.cap.set(1,self.frame_count)
        if self.change_count==3:
            self.change_count=0
            self.subfuc()
        self.change_count+=1

    def k1(self):
        self.timer_camera.stop()  # 停止计时器
        self.flag= not self.flag

    def k2(self):
        if self.PauseFlag==False:#代表此时是暂停的状态
            self.timer_camera.stop()  # 停止计时器
        self.flag = not self.flag
        self.subfuc()



    def subfuc(self):
        #这个函数主要用于我在拖动滑动条的时候，能够每拖动一段，就显示一些图片。
        #同时这个函数也能让我在最终松开滑动条的时候能够显示此时的图片，无论是不是暂停的状态

        # 这里减一，是因为后面的self.cap.read()会从下一个开始读
        #如果这里减一就正好

        self.frame_count = self.sld.value()-1
        self.cap.set(1, self.frame_count)

        ret, self.frame = self.cap.read()
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        #鼠标画框的函数
        global img
        img = frame

        global clean_out
        clean_out=False


        self.frame_count = int(self.cap.get(1))
        self.sld.setValue(self.frame_count)
        self.label_num.setText("视频相关信息：" +
                               "      帧数：" + str(round(self.frame_count, 2))+
                               # "      视频时间"+str(round(self.cap.get(0),2))+
                               # "      真实时间"+str(round(self.curtime,2))+
                               # "      图片间的时间间隔（ms）"+str(round(self.timefps,2))
                               "      左边界：" + str(self.left)+
                               "      右边界：" + str(self.right)+
                               "      投篮帧范围："+str(self.right-self.left)
                               )
        self.label_num.setFixedSize(900, 50)  # width height
        self.label_num.move(50, 0)
        self.label_num.setStyleSheet("QLabel{background:aqua;}")
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        q_image = QImage(frame.data, width, height, bytesPerLine,
                         QImage.Format_RGB888).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(QPixmap.fromImage(q_image))

    def label_change(self):

        new_left_label = int(50+6 + (self.left / self.frame_all) * (900-16) )
        self.left_label.move(new_left_label, 500)

        new_right_label = int(50+6 + (self.right / self.frame_all) * (900-16))
        self.right_label.move(new_right_label, 500)


    def temp_clean(self):
        # 这句话主要就是为了让我存储了数据后，清空当前的暂存数据
        global pos_human
        global pos_ball
        pos_human=[0,0,0,0]
        pos_ball=[0,0,0,0]

        global text_0
        global text_1
        global text_2
        global text_3

        # 最终决定输出文件格式后的要求：（去除了ball,加入了左右帧位置，去除了括号）
        text_0 = '{},{}'.format(0,0)
        text_1 = '{},{},{},{}'.format(0,0,0,0)
        text_2 = '{},{},{},{}'.format(0,0,0,0)
        text_3 = '{},{},{},{}'.format(0,0,0,0)

        self.label_store_data.setText(
            "文件名称:" + target_file_name +"\n"+
            "文件地址:"+ target_file_path+"\n" +
            text_0 + "\n" + text_1 + "\n" + text_2 + "\n" + text_3 + "\n"+
            "        按Enter键将数据导入文件")



    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        # 参数1  控件
        if QKeyEvent.key() == Qt.Key_Left and self.lock and self.left<self.right and self.left_right_lock==False:
            # 判断是否按下了左键

            #这个方法是按照我目前的拖动条上的指针的位置
            #temp_frame=int(self.cap.get(1))

            #这个方法是只按照左右边界的位置，计算出中心位置，然后让中心位置做新的左或者右边界
            temp_frame=int((self.left+self.right)/2)
            self.right=temp_frame
            target_frame=int((self.left+self.right)/2)
            self.sld.setValue(target_frame)
            self.subfuc()

            self.memo.append([self.left, target_frame, self.right])


            #实现右标签的变动
            self.label_change()


        if QKeyEvent.key() == Qt.Key_Right and self.lock and self.left<self.right and self.left_right_lock==False:  # 判断是否按下了右键
            #这个方法是按照我目前的拖动条上的指针的位置
            #temp_frame=int(self.cap.get(1))

            #这个方法是只按照左右边界的位置，计算出中心位置，然后让中心位置做新的左或者右边界
            temp_frame=int((self.left+self.right)/2)
            self.left=temp_frame
            target_frame=int((self.left+self.right)/2)
            self.sld.setValue(target_frame)
            self.subfuc()
            self.memo.append([self.left, target_frame, self.right])

            #实现左标签的变动
            self.label_change()

        if QKeyEvent.key() == Qt.Key_R and len(self.memo)>1 and self.lock  and self.left_right_lock==False:
            #这个函数是为了在二分法时进行回退
            self.memo.pop(-1)
            self.left=self.memo[-1][0]
            self.right=self.memo[-1][2]
            self.sld.setValue(self.memo[-1][1])
            self.subfuc()

            self.label_change()


        if QKeyEvent.key() == Qt.Key_I and self.lock  and self.left_right_lock==False:
            #后面我又加了一些功能后，感觉这个功能有些鸡肋，但是还是放这儿吧

            # 进入二分法模式,按下i键，能够启动视频。
            #若视频正在启动，则会暂停，而且返回之前的做二分法的位置

            self.slotPause()
            self.left=self.memo[-1][0]
            self.right=self.memo[-1][2]

            if self.sld.value()==self.left:
                self.sld.setValue(self.left)
            elif self.sld.value()==self.right:
                self.sld.setValue(self.right)
            else:
                self.sld.setValue(self.memo[-1][1])

            self.subfuc()

        if QKeyEvent.key() == Qt.Key_A and self.lock   and self.left_right_lock==False:  # 让拖动条切换到左边界
            #判断中加一个len(self.memo)>1是为了让我没有做二分法时，即刚刚导入视频时，不能使用左右中切换
            #因为此时没有中
            self.sld.setValue(self.memo[-1][0])#先修改目前的拖动条
            self.subfuc()#这个函数根据拖动条的位置，确定播放的图片

        if QKeyEvent.key() == Qt.Key_D and self.lock   and self.left_right_lock==False:  # 让拖动条切换到右边界
            self.sld.setValue(self.memo[-1][2])
            self.subfuc()

        if QKeyEvent.key() == Qt.Key_S and self.lock   and self.left_right_lock==False:  # 让拖动条切换到中间
            self.sld.setValue(self.memo[-1][1])
            self.subfuc()

        if QKeyEvent.key() == Qt.Key_P and self.lock  and self.left_right_lock==False:  # 暂停键
            self.slotPause()

        if QKeyEvent.key() == Qt.Key_Q and self.lock:  #用于拖动条的一点一点的移动
            step = -1
            if self.left_right_lock == False:
                self.sld.setValue(self.sld.value() + step)
                self.subfuc()
            else:
                if self.left == self.right and self.target_label == "right":
                    print()
                else:
                    self.sld.setValue(self.sld.value() + step)
                    self.subfuc()

            #按下w的时候进入一个锁定模式，只在左右边界锁定，锁定后，通过q和e实现左右边界的移动
            #在锁定的时候，只能让标签缓慢的左右移动，所以说
            #在这个模式下不能使用二分法，因为二分法会让标签瞬移
            if self.left_right_lock==True and self.left>1 and self.right>1:
                if self.target_label=="left":
                    self.left-=1
                if self.target_label=="right" and self.right>self.left:
                    self.right-=1

                self.label_change()

                target_frame = int((self.left + self.right) / 2)
                self.memo.append([self.left, target_frame, self.right])


        if QKeyEvent.key() == Qt.Key_E and self.lock:
            step=1
            if self.left_right_lock == False :
                self.sld.setValue(self.sld.value() + step)
                self.subfuc()
            else:
                if self.left == self.right and self.target_label == "left":
                    print()
                else:
                    self.sld.setValue(self.sld.value()+step)
                    self.subfuc()

            if self.left_right_lock==True and self.left<self.frame_all and self.right<self.frame_all:
                if self.target_label=="left" and self.left<self.right:
                    self.left+=1
                if self.target_label=="right":
                    self.right+=1
                self.label_change()

                target_frame = int((self.left + self.right) / 2)
                self.memo.append([self.left, target_frame, self.right])

        if QKeyEvent.key() == Qt.Key_W and self.lock:  # 打下左右标签的锁，只对左右标签有用，其他的地方无法锁
            if self.sld.value()==self.left or self.sld.value()==self.right:
                if self.left_right_lock==False:
                    # 在左或右的标签附近打上显眼的记号

                    if self.sld.value()==self.left:
                        self.target_label="left"
                    elif self.sld.value()==self.right:
                        self.target_label="right"
                    self.left_right_lock=True
                else:
                    self.left_right_lock=False
            else:
                print("")


        if QKeyEvent.key() == Qt.Key_O and self.lock:  # 判断是否按下了O键
            print(self.left)
            print(self.right)

        global choice
        global pos_human
        global pos_ball

        global text_0
        global text_1
        global text_2
        global text_3

        global target_file_path

        if QKeyEvent.key() == Qt.Key_1 and self.lock:
            choice=1

        if QKeyEvent.key() == Qt.Key_2 and self.lock:
            choice=2

        if QKeyEvent.key() == Qt.Key_Space and self.lock:

            human_x0 = pos_human[0]
            human_y0 = pos_human[1]
            human_x1 = pos_human[2]
            human_y1 = pos_human[3]
            ball_x0 = pos_ball[0]
            ball_y0 = pos_ball[1]
            ball_x1 = pos_ball[2]
            ball_y1 = pos_ball[3]

            #通过目前滑动条的位置判断

            #最终决定输出文件格式后的要求：（去除了ball,加入了左右帧位置，去除了括号）
            if self.sld.value()==self.memo[-1][0]:
                text_0='{},{}'.format(self.memo[-1][0],self.memo[-1][2])
                text_1='{},{},{},{}'.format(human_x0, human_y0, human_x1, human_y1,)
            elif self.sld.value()==self.memo[-1][1]:
                text_2='{},{},{},{}'.format(human_x0, human_y0, human_x1, human_y1,)
            elif self.sld.value()==self.memo[-1][2]:
                text_0 = '{},{}'.format(self.memo[-1][0], self.memo[-1][2])
                text_3='{},{},{},{}'.format(human_x0, human_y0, human_x1, human_y1,)

            self.label_store_data.setText(
                "文件名称:" + target_file_name + "\n" +
                "文件地址:" + target_file_path+"\n" +
                text_0 + "\n" + text_1 + "\n" + text_2 + "\n" + text_3 + "\n" +
                "        按Enter键将数据导入文件")


        if QKeyEvent.key() == Qt.Key_M and self.lock:
            #先看文件是否已经存在了
            if os.path.exists(target_file_path+"/"+target_file_name[0:-4]+".txt"):
                Warming = QMessageBox.warning(self, "Warming", "已经存在同名的文件了！！！",
                                                   QMessageBox.Yes)
            else:
                f = open(target_file_path+"/"+target_file_name[0:-4]+".txt", 'w')
                f.write(text_0+"\n"+text_1+"\n"+text_2+"\n"+text_3)
                f.close()

            #这个函数就是为了：当我存储数据或者更换了新的视频源后刷新暂存的数据
            self.temp_clean()


        #未来可能会用到的键组合
        if QKeyEvent.modifiers() == Qt.ControlModifier | Qt.ShiftModifier and QKeyEvent.key() == Qt.Key_A:  # 三键组合
            print('按下了Ctrl+Shift+A键')

        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_A:  # 两键组合
            print('按下了Ctrl-A键')





global choice
#这是一个数据，分别为x0,y0,x1,y1 然后再*2
global pos_human
global pos_ball
pos_human=[0,0,0,0]
pos_ball=[0,0,0,0]

#这是一个标记，用于当我导入新视频后清空之前的方框
global clean_out
clean_out=True

class myLabel(QLabel):
    #这里的方框需要在我使用stop和load或者导入新的视频文件后消除，不能留下来
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    global choice
    choice=1
    human=QRect()
    ball=QRect()
    line_width=2
    global pos_human
    global pos_ball

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        if choice==1:
            self.human=QRect(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)
            pos_human[0]=self.human.x()
            pos_human[1]=self.human.y()
            pos_human[2] =self.human.x() + self.human.width()
            pos_human[3] =self.human.y() + self.human.height()

        if choice==2:
            self.ball=QRect(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)
            pos_ball[0]=self.ball.x()
            pos_ball[1]=self.ball.y()
            pos_ball[2] =self.ball.x() + self.ball.width()
            pos_ball[3] =self.ball.y() + self.ball.height()

        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        #这个rect是为了实现画rect的动画，让我画框的动作连贯
        rect = QRect(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)
        painter = QPainter(self)

        #导入新视频或者stop或者load后，清空方框
        global clean_out
        if clean_out==False:
            self.human=QRect()
            self.ball=QRect()
            rect=QRect()
            #painter.drawRect(rect)

            #每次更换后，choice自动变为1，成为human
            global choice
            choice=1
            clean_out=True

            global pos_human
            global pos_ball
            pos_human=[0,0,0,0]
            pos_ball=[0,0,0,0]


        if choice==1:
            painter.setPen(QPen(Qt.red, self.line_width, Qt.SolidLine))
            painter.drawRect(self.ball)

            painter.setPen(QPen(Qt.green, self.line_width, Qt.SolidLine))
        elif choice==2:
            #下面两句话是用来画出human的方框，和正在画的ball不冲突
            painter.setPen(QPen(Qt.green, self.line_width, Qt.SolidLine))
            painter.drawRect(self.human)

            painter.setPen(QPen(Qt.red, self.line_width, Qt.SolidLine))
        #让我画框的动作连贯
        painter.drawRect(rect)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = Video()
    my.show()
    sys.exit(app.exec_())
