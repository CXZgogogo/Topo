from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from Interface.frequency import Ui_fupin
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Interface.sharedClass import *
from PyQt5 import QtWidgets
# import  serial_test01 as ser
from SerialCommunication import Serial as ser
import numpy as np
import matplotlib,sip
matplotlib.use("Qt5Agg")
import logging
# 每次都会覆盖之前的日志文件
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO, filename='../log/procedure.log', filemode ='w', )
'''
    幅频显示页面，定义了一个返回信号，用于测量页面和主页面之间的跳转 
    在combobox选项框中选择的两个节点，选择的不是同一节点，才会调用接口程序，
    接口程序将测量结果上传到数据库，然后读取数据库信息，将测量结果显示出来
    
'''
TABLE = readConfigurationFile("Database").getCon("table_adjacentNode")
delayTABLE=readConfigurationFile("Database").getCon("table_delay")
fupinTABLE=readConfigurationFile("Database").getCon("table_fupin")
# 幅频显示界面类
class fupinWindow(QtWidgets.QMainWindow,Ui_fupin):
    # 定义返回之前界面的信号
    backsignal1=pyqtSignal()
    def __init__(self):
        super(fupinWindow,self).__init__()
        self.setupUi(self) #加载幅频显示窗口
        self.pushButton.clicked.connect(self.backmain)
        # 初始化combobox
        self.init_combobox1()
        self.init_combobox2()
        # 退出按钮槽函数
        # fig=self.simplePicture()
        self.pushButton.clicked.connect(self.backmain)
        # 确定按钮
        self.pushButton_2.clicked.connect(lambda: self.frequencyshow())
        # 取消按钮
        self.pushButton_3.clicked.connect(lambda: self.cancelbt())
        self.comboBox.currentIndexChanged.connect(self.btnState)
        fig = plt.figure()
        self.canvas = FigureCanvas(fig)
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        self.gridlayout.addWidget(self.canvas, 0, 1)
        logging.info('幅频页面开始')

    def btnState(self):
        combobox1_node=self.comboBox.currentText()
        sql = "SELECT node FROM "+str(TABLE)+" WHERE src='%s'" % combobox1_node
        neighborNodeList=self.lengthNum(sql)
        self.comboBox_2.clear()
        for node in neighborNodeList:
            self.comboBox_2.addItem(node['name'])

    # combobox初始化函数
    def init_combobox1(self):
        # 设置item的个数
        sql = "SELECT DISTINCT(src) FROM "+str(TABLE)
        realList2 = self.lengthNum(sql)
        self.comboBox.setMaxCount(len(realList2))
        for node in realList2:
            self.comboBox.addItem(node['name'])

    def init_combobox2(self):
        sql = "SELECT DISTINCT(src) FROM "+str(TABLE)
        realList2 = self.lengthNum(sql)
        self.comboBox_2.setMaxCount(len(realList2))
        for node in realList2:
            self.comboBox_2.addItem(node['name'])
    # 幅频曲线显示显示框
    def frequencyshow(self):
        t1 = self.comboBox.currentText()
        t2 = self.comboBox_2.currentText()
        if t1 == t2:
            logging.info('输入节点信息有误')
            print("输入的两个节点是同一个节点")
        else:
            logging.info('显示输入节点的幅频曲线')
            # 幅频曲线显示，将两个节点信息发送给串口，得到两个点的幅频信息，查询数据库获得幅频数据
            ser.am_measure_order(t1, t2)
            sqlAmplitude = "SELECT fupin FROM "+fupinTABLE+" WHERE src='%s' AND node='%s'" % (t1, t2)
            fig1 = self.simplePicture(sqlAmplitude)
            sip.delete(self.canvas)
            self.canvas = FigureCanvas(fig1)
            self.gridlayout.addWidget(self.canvas, 0, 1)
    # 取消按钮的槽函数
    def cancelbt(self):
        self.comboBox.clear()
        self.init_combobox1()
        self.comboBox_2.clear()
        self.init_combobox2()

    # 横纵坐标轴都没有取对数
    def simplePicture(self, sqlAmplitude):
        # 创建一个Figure
        fig = plt.figure()
        fig.clf()
        canvas = FigureCanvas(fig)
        frequency=[]
        a=0.4
        for i in range(0,136):
            frequency.append(a)
            a=a+0.1
        sql = sqlAmplitude
        results=Sqlite().select(sql)
        str1=results[0][0]
        arr1=str1.split(',')
        arr2=[]
        for arr in arr1:
            arr2.append(int(arr) *(-1))
        frequency_np = np.array(frequency)
        amplitude = np.array(arr2)
        plt.plot(frequency_np, amplitude)
        return fig

    # 使用邻接表查询节点的名字
    def lengthNum(self, sql):
        data = []
        try:
            results = Sqlite().select(sql)
            for row in results:
                result = {}
                result['name'] = str(row[0])
                data.append(result)
        except:
            print("查询出错")
        return data

    # 返回界面信号
    def backmain(self):
        self.backsignal1.emit()
        logging.info('返回主页面')
        self.setVisible(0)
if __name__ == '__main__':
    import sys
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    the_window = fupinWindow()
    the_window.show()
    sys.exit(app.exec_())