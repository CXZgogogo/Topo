from PyQt5.QtWidgets import QMessageBox
# import  serial_test01 as ser
from SerialCommunication import Serial as ser
from Interface.delay import Ui_shiyan
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from Interface.sharedClass import *
import sys
# from getTopo import *
import matplotlib
matplotlib.use("Qt5Agg")
import logging
# 每次都会覆盖之前的日志文件
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO, filename='../log/procedure.log', filemode ='w', )
'''
    时延测量页面，定义了一个返回信号，用于测量页面和主页面之间的跳转
    在combobox选项框中选择的两个节点，若是选择的是同一节点，在结果显示框中显示“输入的节点是同一节点”的提示信息，
    若是选择的不是同一节点，则调用接口程序，根据接口程序返回的标志位判断测量过程是否出错，出错的话则显示“测量出错”的提示信息，
    若是测量没有出错并判断结果信息无误，则显示测量结果  
'''
TABLE = readConfigurationFile("Database").getCon("table_adjacentNode")
delayTABLE=readConfigurationFile("Database").getCon("table_delay")
fupinTABLE=readConfigurationFile("Database").getCon("table_fupin")

class shiyanWindow(QtWidgets.QMainWindow,Ui_shiyan):
    # 定义返回之前界面的信号
    backsignal2=pyqtSignal()
    def __init__(self):
        super(shiyanWindow,self).__init__()
        self.setupUi(self) #加载时延显示窗口
        # 初始化combobox
        self.init_combobox1()
        self.init_combobox2()
        # 退出按钮槽函数
        self.pushButton.clicked.connect(self.backmain)
        # 确定按钮的槽函数
        self.pushButton_2.clicked.connect(lambda: self.timeshow())
        # 取消按钮的槽函数
        self.pushButton_3.clicked.connect(lambda: self.cancelbt())
        self.comboBox.currentIndexChanged.connect(self.btnState)
        logging.info('时延页面开始')
    def btnState(self):
        combobox1_node=self.comboBox.currentText()
        sql = "SELECT node FROM "+str(TABLE)+" WHERE src='%s'" % combobox1_node
        neighborNodeList=self.lengthNum(sql)
        self.comboBox_2.clear()
        # self.comboBox_2.
        for node in neighborNodeList:
            self.comboBox_2.addItem(node['name'])
    # combobox初始化函数
    def init_combobox1(self):
        # 查询邻接表中节点信息，设置combobox1的信息
        sql = "SELECT DISTINCT(src) FROM "+str(TABLE)
        realList1 = self.lengthNum(sql)
        self.comboBox.setMaxCount(len(realList1))
        for node in realList1:
            self.comboBox.addItem(node['name'])
    def init_combobox2(self):
        # 查询邻接表中节点信息，设置combobox2的信息
        sql = "SELECT DISTINCT(src) FROM "+str(TABLE)
        realList1 = self.lengthNum(sql)
        self.comboBox_2.setMaxCount(len(realList1))
        for node in realList1:
            self.comboBox_2.addItem(node['name'])
    # 时延显示框
    def timeshow(self):
        # t1、t2是选项框中选择的节点
        t1=self.comboBox.currentText()
        t2=self.comboBox_2.currentText()
        if t1 == t2:
            logging.info('输入节点信息有误')
            self.textEdit.setText("输入的两个节点是同一个节点")
        else:
            # 调用接口程序
            flag=1
            flag=ser.delay_measure_order(t1,t2)
            # 根据接口程序返回的flag值判断测量是否出错
            if flag==1:
                sql = "SELECT * FROM "+delayTABLE+" WHERE src='%s' AND node='%s'" % (t1, t2)
                data=self.delay_info(sql)
                logging.info(data)
                if data==0xFFFF:
                    self.textEdit.setText('节点不可达')
                elif data>=0:
                    self.textEdit.setText(str(data)+'ns')
                else:
                    self.textEdit.setText(str(data))
            else:
                start = QMessageBox.warning(self, "Warning！", '测量出错，点击OK退出测量界面', QMessageBox.Ok,QMessageBox.Ok)
                if start == QMessageBox.Ok:
                    self.backmain()
                # time.sleep(5)
                self.backmain()
    #使用邻接表查询所有节点的名字
    def lengthNum(self,sql):
        data = []
        results=Sqlite().select(sql)
        try:
            for row in results:
                result = {}
                result['name'] = str(row[0])
                data.append(result)
        except:
            logging.info("查询出错")
        return data
    def delay_info(self,sql):
        try:
            reseult = Sqlite().select(sql)
            data = reseult[0][2]
        except:
            print("查询出错")
        return data

    # 取消按钮的槽函数，点击取消按钮，选项框的内容会返回初始化的状态
    def cancelbt(self):
        self.comboBox.clear()
        self.init_combobox1()
        self.comboBox_2.clear()
        self.init_combobox2()
    # 界面信号显示函数，点击退出按钮返回主页面
    def backmain(self):
        logging.info('返回主页面')
        self.backsignal2.emit()
        self.setVisible(0)
if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    the_window = shiyanWindow()
    the_window.show()
    sys.exit(app.exec_())