import cv2
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QGuiApplication, QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5 import QtWidgets

import sys
class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

        pqscreen = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        pixmap2.save('555.png')


# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.resize(675, 300)
#         self.setWindowTitle('关注微信公众号：学点编程吧--opencv、PyQt5的小小融合')
#
#         self.lb = myLabel(self)
#         self.lb.setGeometry(QRect(0, 30, 511, 241))
#
#         path = "C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic/924.jpg"
#
#         img = cv2.imread(path)
#         height, width, bytesPerComponent = img.shape
#         bytesPerLine = 3 * width
#         cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
#         QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(QImg)
#
#         self.lb.setPixmap(pixmap)
#         self.lb.setCursor(Qt.CrossCursor)
#
#         self.show()
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     # MainWindow = QtWidgets.QMainWindow()  # 创建窗体对象
#     # ui = document.Ui_MainWindow()  # 创建PyQt设计的窗体对象
#     # ui.setupUi(MainWindow)  # 调用PyQt窗体方法，对窗体对象初始化设置
#     # MainWindow.show()  # 显示窗体
#
#     my = Example()
#     my.show()
#     sys.exit(app.exec_())
