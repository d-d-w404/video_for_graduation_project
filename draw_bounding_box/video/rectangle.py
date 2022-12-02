from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
import cv2
import sys


class MyLabel(QLabel):
    # x0 = 0
    # y0 = 0
    # x1 = 0
    # y1 = 0

    flag = False  # 是否按下鼠标
    ifmove = False  # 是否进行拖拽整体移动
    biggerLeft = False  # 是否进行拖拽放大缩小，坐标点在标注框的左边
    biggerRight = False  # 是否进行拖拽放大缩小，坐标点在标注框的右边
    biggerButton = False  # 是否进行拖拽放大缩小，坐标点在标注框的下边
    biggerTop = False  # 是否进行拖拽放大缩小，坐标点在标注框的上边

    rect = []  # 标注框的起始点坐标和终点坐标，形如 [start_x, start_y, end_x, end_y]

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        self.rect = []
        print("双击事件发生！")
        self.update()

    # 鼠标单击事件
    def mousePressEvent(self, event):
        self.flag = True
        # self.x0 = event.x()
        # self.y0 = event.y()

        if self.rect:
            # 此时已经存在标注框，再点击，则为拖拽整体移动或者放大缩小
            # 整体移动：当点击坐标位于标注框内，则说明为整体移动
            # 放大缩小：当点击坐标位于标注框的四条边上，则说明为放大缩小

            # 框的左上角和右下角
            topleft_x = min(self.rect[0], self.rect[2])
            topleft_y = min(self.rect[1], self.rect[3])
            buttonright_x = max(self.rect[0], self.rect[2])
            buttonright_y = max(self.rect[1], self.rect[3])
            # 整体移动的判定：点坐标在左上角和右下角之间
            if (event.x() > topleft_x + 5) and (event.x() < buttonright_x - 5) and (event.y() > topleft_y + 5) and (
                    event.y() < buttonright_y - 5):
                print("判定为整体移动")
                self.ifmove = True
                self.preMousePosition = event.pos()
            # 放大缩小的判定：点坐标在框的四条边上
            # 上边，下边、左边、右边
            # 当点坐标在标注框的左边时
            if (event.x() > topleft_x - 5) and (event.x() < topleft_x + 5) and (event.y() > topleft_y) and (
                    event.y() < buttonright_y):
                print("判定为放大缩小，点坐标在标注框的左边上")
                self.biggerLeft = True
                self.preMousePosition = event.pos()
            # 当点坐标在标注框的右边时
            if (event.x() > buttonright_x - 5) and (event.x() < buttonright_x + 5) and (event.y() > topleft_y) and (
                    event.y() < buttonright_y):
                print("判定为放大缩小，点坐标在标注框的右边上")
                self.biggerRight = True
                self.preMousePosition = event.pos()
            # 当点坐标在标注框的下边时
            if (event.x() > topleft_x) and (event.x() < buttonright_x) and (event.y() > buttonright_y - 5) and (
                    event.y() < buttonright_y + 5):
                print("判定为放大缩小，点坐标在标注框的下边上")
                self.biggerButton = True
                self.preMousePosition = event.pos()
            # 当点坐标在标注框的上边时
            if (event.x() > topleft_x) and (event.x() < buttonright_x) and (event.y() > topleft_y - 5) and (
                    event.y() < topleft_y + 5):
                print("判定为放大缩小，点坐标在标注框的上边上")
                self.biggerTop = True
                self.preMousePosition = event.pos()

        else:
            # 如果当前没有标注框，则说明点击后开始拖拽生成标注框
            # 此时，没有整体移动和放大缩小
            self.ifmove = False
            self.biggerLeft = False
            self.biggerRight = False
            self.biggerButton = False
            self.biggerTop = False
            self.rect = [event.x(), event.y(), event.x(), event.y()]

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False
        self.biggerLeft = False
        self.biggerRight = False
        self.biggerButton = False
        self.biggerTop = False
        self.ifmove = False

        # 鼠标移动事件

    def mouseMoveEvent(self, event):
        start_x, start_y = self.rect[0:2]

        if self.flag:  # 按下鼠标，开始拖拽
            # 拖拽可能有三种情况
            # 情况1：在已有标注框的情况下，进行放大缩小
            # 情况1.1：标注框的左边
            if self.biggerLeft:
                print("放大缩小：左边进行x轴方向的缩放")
                differ = event.pos() - self.preMousePosition
                # 更新标注框
                start_x, start_y, end_x, end_y = self.rect
                if start_x < end_x:
                    start_x += differ.x()
                else:
                    end_x += differ.x()
                self.rect = [start_x, start_y, end_x, end_y]
                self.preMousePosition = event.pos()
            # 情况1.2：标注框的右边
            elif self.biggerRight:
                print("放大缩小：右边进行x轴方向的缩放")
                differ = event.pos() - self.preMousePosition
                # 更新标注框
                start_x, start_y, end_x, end_y = self.rect
                if start_x > end_x:
                    start_x += differ.x()
                else:
                    end_x += differ.x()
                self.rect = [start_x, start_y, end_x, end_y]
                self.preMousePosition = event.pos()
            # 情况1.3：标注框的下边
            elif self.biggerButton:
                print("放大缩小：下边进行y轴方向的缩放")
                differ = event.pos() - self.preMousePosition
                # 更新标注框
                start_x, start_y, end_x, end_y = self.rect
                if start_y > end_y:
                    start_y += differ.y()
                else:
                    end_y += differ.y()
                self.rect = [start_x, start_y, end_x, end_y]
                self.preMousePosition = event.pos()
            # 情况1.4：标注框的上边
            elif self.biggerTop:
                print("放大缩小：上边进行y轴方向的缩放")
                differ = event.pos() - self.preMousePosition
                # 更新标注框
                start_x, start_y, end_x, end_y = self.rect
                if start_y < end_y:
                    start_y += differ.y()
                else:
                    end_y += differ.y()
                self.rect = [start_x, start_y, end_x, end_y]
                self.preMousePosition = event.pos()

            # 情况2：在已有标注框的情况下，进行整体移动
            elif self.ifmove:
                differ = event.pos() - self.preMousePosition
                # 更新标注框
                start_x, start_y, end_x, end_y = self.rect
                start_x, start_y = start_x + differ.x(), start_y + differ.y()
                end_x, end_y = end_x + differ.x(), end_y + differ.y()
                self.rect = [start_x, start_y, end_x, end_y]
                self.preMousePosition = event.pos()
                print("整体移动")

            # 情况3：做标注框
            else:
                # self.x1 = event.x()
                # self.y1 = event.y()
                self.rect = [start_x, start_y, event.x(), event.y()]

            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        if len(self.rect) == 0: return

        # rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        # 这里换成任意方向的矩形框
        # 标注框的左上角和右下角坐标
        x0 = min(self.rect[0], self.rect[2])
        y0 = min(self.rect[1], self.rect[3])
        x1 = max(self.rect[0], self.rect[2])
        y1 = max(self.rect[1], self.rect[3])
        width = x1 - x0
        height = y1 - y0

        # 矩形
        rect = QRect(x0, y0, width, height)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(675, 500)
        self.move(100, 50)
        self.setWindowTitle('在label中绘制矩形')
        self.lb = MyLabel(self)  # 重定义的label
        # 这里直接读取图片
        img = QPixmap('C:/Users/Wander/Desktop/1.jpg')
        # 往显示视频的Label里 显示QImage
        self.lb.setPixmap(img)
        self.lb.setCursor(Qt.CrossCursor)  # 图片可以绘制
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())

