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
