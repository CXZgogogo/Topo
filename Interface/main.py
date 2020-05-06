# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(30, 20, 1211, 601))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1209, 599))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollArea.setStyleSheet('''QScrollArea {border-radius:0.1px solid;}''')


        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(10, 530, 261, 61))
        self.tableWidget.setMinimumSize(QtCore.QSize(50, 50))
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 2000))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        # self.tableWidget.setStyleSheet('''QTableWidget {background:black;color:white;font-size:15px;font-weight:8;font-family:Roman times;}''')

        self.treeWidget = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidget.setGeometry(QtCore.QRect(10, 20, 261, 501))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "节点目录")

        # self.treeWidget.setStyleSheet("background-color:black;color:white;font-size:15px;font-weight:8;font-family:Roman times;")

        self.graphicsView = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents)
        self.graphicsView.setGeometry(QtCore.QRect(290, 20, 911, 571))
        self.graphicsView.setObjectName("graphicsView")

        # self.graphicsView.setStyleSheet("background-color:rgb(40, 40, 40)")
        self.graphicsView.setStyleSheet("background-color:rgb(230, 230, 230)")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(30, 620, 1211, 51))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        # self.scrollArea_2.setStyleSheet('''QScrollArea {background-color:black;border:0.5px solid;}''')
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1209, 49))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setGeometry(QtCore.QRect(20, 10, 31, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setGeometry(QtCore.QRect(60, 10, 54, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setGeometry(QtCore.QRect(140, 10, 31, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setGeometry(QtCore.QRect(180, 10, 54, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setGeometry(QtCore.QRect(250, 10, 54, 31))
        self.label_5.setObjectName("label_5")
        self.comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.comboBox.setGeometry(QtCore.QRect(310, 10, 71, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 10, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 10, 91, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton.setGeometry(QtCore.QRect(600, 10, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_2)
        self.progressBar.setGeometry(QtCore.QRect(1050, 10, 151, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_6.setGeometry(QtCore.QRect(890, 10, 151, 31))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        # MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        # MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 美化标签
        self.label.setStyleSheet('''QLabel{color:black;font-size:12px;font-weight:4;font-family:Roman times;border-radius:3.5px;background:#bfbfbf;}''')
        self.label_3.setStyleSheet('''QLabel{color:black;font-size:12px;font-weight:4;font-family:Roman times;border-radius:3.5px;background:#bfbfbf;}''')
        self.label_5.setStyleSheet('''QLabel{color:black;font-size:12px;font-weight:4;font-family:Roman times;border-radius:3.5px;background:#bfbfbf;}''')
        self.label_6.setStyleSheet('''QLabel{color:black;font-size:12px;font-weight:4;font-family:Roman times;border-radius:3.5px;background:#999999;}''')
        # 按钮美化 ,触发时颜色变亮
        self.pushButton_3.setStyleSheet('''QPushButton{color:black;border-radius:15px;background:#999999;}QPushButton:hover{background:white;}''')
        self.pushButton_4.setStyleSheet('''QPushButton{color:black;border-radius:15px;background:#999999;}QPushButton:hover{background:white;}''')
        self.pushButton.setStyleSheet('''QPushButton{color:black;border-radius:15px;background:#999999;}QPushButton:hover{background:white;}''')


        #菜单栏样式
        self.menubar.setStyleSheet('''QMenuBar{background-color:transparent;border: 0.5px solid gray;}''')
        # self.menubar.setStyleSheet('''QMenuBar{background-color:transparent;border: 1px solid gray;}QMenuBar:item:selected{background-color:white;}QMenuBar:item{font-size:12px;font-family:Microsoft YaHei;color:black;}''')
        # self.menubar.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "节点信息"))
        self.label.setText(_translate("MainWindow", "正常"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "异常"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "接口设置："))
        self.comboBox.setItemText(0, _translate("MainWindow", "串口"))
        self.comboBox.setItemText(1, _translate("MainWindow", "socket"))
        self.pushButton_3.setText(_translate("MainWindow", "历史数据"))
        self.pushButton_4.setText(_translate("MainWindow", "开始测量"))
        self.pushButton.setText(_translate("MainWindow", "联机"))
        self.label_6.setText(_translate("MainWindow", "计数板"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "查看"))
        self.menu_3.setTitle(_translate("MainWindow", "设置"))

        MainWindow.setWindowOpacity(1)  # 设置窗口透明度
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 无边框，置顶
        # MainWindow.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景色
        pe = QPalette()
        MainWindow.setAutoFillBackground(True)
        pe.setColor(QPalette.Background, QtGui.QColor(200, 200, 200))  # 设置背景色
        MainWindow.setPalette(pe)


from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
    # def __init__(self, grScene, parent=None):
        super().__init__(parent)
        # self.grScene = grScene

        self.initUI()

        # self.setScene(self.grScene)

        self.zoomInFactor = 1.25
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        # 图像品质
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        # 全部刷新
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 关闭滚动条
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    # 判断鼠标按下的类型
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    # 判断鼠标松开的类型
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def leftMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    # 滚轮缩放的实现
    def wheelEvent(self, event):
        # calculate our zoom Factor

        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        # 放大触发
        if event.angleDelta().y() > 0:
            # 放大比例 1.25
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        # 缩小触发
        else:
            # 缩小的比例 0.8
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        # self.zoomRange[0] = 0 , self.zoomRange[1] =10
        # 限制缩放的极致 , 缩小到self.zoom = -1 或者放大到self.zoom=11 时,
        # 取消 缩放 ,
        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            # 缩放实现的函数
            self.scale(zoomFactor, zoomFactor)



