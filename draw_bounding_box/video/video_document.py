import sys
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QDirModel, QLabel, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(1000, 500)

        # self.model = QDirModel(self)                            # 1
        # self.model.setReadOnly(False)
        # self.model.setSorting(QDir.Name | QDir.IgnoreCase)

        self.model = QDirModel()

        self.tree = QTreeView(self)
        self.tree.allColumnsShowFocus()
        self.tree.move(0,0)
        self.tree.setFixedSize(500,500)

        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('F:/train'))

        self.tree.clicked.connect(self.show_info)
        # self.index = self.model.index(QDir.currentPath())
        # self.tree.expand(self.index)
        # self.tree.scrollTo(self.index)

        self.info_label = QLabel(self)                          # 3
        self.info_label.setText("Waiting for video...")
        self.info_label.setFixedSize(500, 500)  # width height
        self.info_label.move(500, 0)
        self.info_label.setStyleSheet("QLabel{background:black;}"
                                 "QLabel{color:rgb(100,100,100);font-size:15px;font-weight:bold;font-family:宋体;}"
                                 )

        # self.v_layout = QVBoxLayout()
        # self.v_layout.addWidget(self.tree)
        # self.v_layout.addWidget(self.info_label)
        # self.setLayout(self.v_layout)


        # self.label = QLabel(self)
        # self.label.setText("Waiting for video...")
        # self.label.setFixedSize(100, 450)  # width height
        # self.label.move(500, 50)
        # self.label.setStyleSheet("QLabel{background:black;}"
        #                          "QLabel{color:rgb(100,100,100);font-size:15px;font-weight:bold;font-family:宋体;}"
        #                          )



    def show_info(self):
        index = self.tree.currentIndex()
        file_name = self.model.fileName(index)
        file_path = self.model.filePath(index)
        print(file_path+file_name)
        #file_info = 'File Name: {}\nFile Path: {}'.format(file_name, file_path)
        #self.info_label.setText(file_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())