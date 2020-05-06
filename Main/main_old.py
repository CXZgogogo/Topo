import threading
# from getTopo import *
import matplotlib
matplotlib.use("Qt5Agg")
from Interface.frequencyWindow import *
from Interface.delayWindow import *
from Interface.connectWindow import *
from Interface.busyWindow import *
from Interface.main import Ui_MainWindow
from Interface.topo_picture import *
from PyQt5.QtGui import *
import time
import logging
# import  serial_test01 as ser
import sys
import sip
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QGraphicsTextItem
from PyQt5.QtGui import (QBrush, QImage, QPainter, QPen, QPixmap)
from PyQt5.QtCore import (QPointF,Qt)
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsPixmapItem
# import  serial_test01 as ser
from SerialCommunication import Serial as ser
from TopoRecognitionAlgorithm import Topo

# 每次都会覆盖之前的日志文件
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO,filename='../log/procedure.log',filemode = 'w',)
# 设置的全局变量
# 最新数据
newNodeList = []
newNodeList1 = []
newRealList = []
newRealList1 = []
# 历史数据
oldNodeList = []
oldNodeList1 = []
oldRealList = []
oldRealList1 = []
# 参数设置
reallist=[]
paraList=[500,3,20,40,4]
tree_flag=1
end_flag=0
topo_flag=-1
num=0
cco = readConfigurationFile("Topo").getCon("CCO")
'''
    设置了4个线程，分别是对接口程序、接口已测量节点数目和拓扑算法程序、拓扑算法计算过程的线程
'''

# 接口测量的线程
class Qmeasure(QThread): #
    endflag = pyqtSignal(int)
    def __init__(self):
        super(Qmeasure,self).__init__()
    def run(self):
        global end_flag
        end_flag=ser.start_measure_order(paraList)
        # count_num=ser.count_flag
        # self.count.emit(int(count_num))
        self.endflag.emit(int(end_flag))
        # end_flag=0
        self.exit(0)
# 接口测量节点数目的线程
class Qcount(QThread):  #
    # endflag = pyqtSignal(int)
    count = pyqtSignal(int)
    def __init__(self):
        super(Qcount, self).__init__()
    def run(self):
        global end_flag
        # end_flag = ser.start_measure_order(paraList)
        while end_flag ==0:
            count_num=ser.count_flag
            self.count.emit(int(count_num))
            # self.endflag.emit(int(end_flag))
            time.sleep(0.005)
        self.count.emit(int(num))
        end_flag=0
        self.exit(0)
# 拓扑计算节点数目的线程
class Qcounttopo(QThread):  #
    # endflag = pyqtSignal(int)
    count = pyqtSignal(int)
    def __init__(self):
        super(Qcounttopo, self).__init__()
    def run(self):
        global topo_flag
        # end_flag = ser.start_measure_order(paraList)
        while topo_flag ==-1:
            count_num= Topo.count
            self.count.emit(int(count_num))
            # self.endflag.emit(int(end_flag))
            time.sleep(0.005)
        topo_flag=-1
        self.count.emit(15)
        self.exit(0)
#拓扑计算的线程
class QTopo(QThread): #
    endflag = pyqtSignal(int)

    def __init__(self):
        super(QTopo,self).__init__()
    def run(self):
        global topo_flag,cco
        # flag=ser.start_measure_order(paraList)
        # flag=Topo.getTopo('R')       #这里要传入cco的地址！！！！！！！！！
        # flag = Topo.getTopo('000000000000')#如果cco是全0的话用这个
        flag = Topo.getTopo(cco)
        # flag = Topo.getTopo('303030303052')
        topo_flag=flag
        # flag=0
        self.endflag.emit(int(flag))
        # print('计算完成')
        self.exit(0)

'''
    页面设计的主程序
'''
# 页面返回清空
class myWindow(QtWidgets.QWidget,Ui_MainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setupUi(self)
        self.Ui_init()
        myWindow.setWindowFlags(self,QtCore.Qt.WindowStaysOnTopHint)
    def Ui_init(self):
        # 传递界面类
        self.fupin = fupinWindow()
        self.shiyan =shiyanWindow()
        self.conn = connectWindow()
        self.busy=busyWindow()
        # 菜单栏初始化
        self.printAction1 = QAction(self.tr("退出"), self)
        self.menu.addAction(self.printAction1)
        self.printAction1.triggered.connect(lambda :self.tuichu())
        self.printAction2 = QAction(self.tr("幅频显示"), self)
        self.printAction3 = QAction(self.tr("点对点时延"), self)
        self.menu_2.addAction(self.printAction2)
        self.menu_2.addAction(self.printAction3)
        self.printAction2.triggered.connect(lambda:self.showFupin())
        self.fupin.backsignal1.connect(lambda:self.showmain())
        self.printAction3.triggered.connect(lambda:self.showShiyan())
        self.shiyan.backsignal2.connect(lambda:self.showmain())
        self.busy.backsignal5.connect(self.busy_backsignal5)
        self.printAction4 = QAction(self.tr("参数设置"), self)
        self.menu_3.addAction(self.printAction4)
        self.printAction4.triggered.connect(lambda: self.showConnect())
        self.conn.backsignal3.connect(self.context_unit)
        self.conn.backsignal4.connect(lambda: self.showmain())
        # self.conn.backsignal3.connect(lambda :self.showConnect)
        # 窗口底部图标简介
        pix1=QPixmap(':/myIcons/绿.jpg').scaledToWidth(18).scaledToHeight(18)
        self.label_2.setPixmap(pix1)
        pix2 = QPixmap(':/myIcons/红.jpg').scaledToWidth(20).scaledToHeight(20)
        self.label_4.setPixmap(pix2)
        # 参数
        # self.old=True
        self.old = 1
        self.error=True
        self.connectError=False
        #  拓扑显示初始化
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graphicsView.scene = QtWidgets.QGraphicsScene(0, 0, 1920, 1080)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsView.setSceneRect(0, 0, 3840, 1160)  # fix scene size 500 500
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  ##设置视图的抗锯齿渲染模式。
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        # 拓扑显示控制按钮
        self.pushButton_3.clicked.connect(lambda:self.startShow())
        # 联机按钮
        self.pushButton.clicked.connect(lambda:self.connect())
        # 默认显示之前的页面
        sql = "select * from newTopo_A"
        oldNodeList = self.getTopo(sql)
        self.initialization(oldNodeList)
        #开始测量按钮
        self.pushButton_4.clicked.connect(lambda:self.startMeasure())
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.printAction2.setEnabled(False)
        self.printAction3.setEnabled(False)
        # 线程
        self.startM = Qmeasure()
        self.startM.endflag.connect(self.changeUI)
        self.topo=QTopo()
        self.topo.endflag.connect(self.newToposhow)
        self.countnum=Qcount()
        self.countnum.count.connect(self.showcount)
        self.counttopo = Qcounttopo()
        self.counttopo.count.connect(self.showcounttopo)
        self.step = 0
        self.progressBar.setValue(self.step)
        #选项框
        self.comboBox.currentIndexChanged.connect(self.btnStateChange)
        readConfigurationFile("Serial").setCon("serial_or_udp", "1")
        # myconfig = configparser.ConfigParser()
        # myconfig.read('config.ini')
        # myconfig.set("Serial", "serial_or_udp", "1")
        # myconfig.write(open("config.ini", "w+"))

    '''
        页面跳转的方法
        showmain()：显示主页面
        tuichu()：退出程序
        showFupin()：显示幅频页面
        showShiyan():显示时延页面
        showBusy():显示繁忙页面
        context_unit():将参数设置页面中设置的参数返回主页面中
    '''
    # 显示主页面
    def showmain(self):
        self.setVisible(1)
    # 退出应用
    def tuichu(self):
        self.close()
    # 显示幅频曲线界面
    def showFupin(self):
        self.setVisible(0) # 隐藏主界面
        self.fupin.setVisible(1)
    # 显示时延界面
    def showShiyan(self):
        self.setVisible(0)
        self.shiyan.setVisible(1)
    def showConnect(self):
        self.setVisible(0)
        self.conn.setVisible(1)
        # print(context)
    def showBusy(self):
        self.setVisible(0)
        self.busy.setVisible(1)
    def context_unit(self,i1,i2,i3,i4,i5):
        global paraList
        paraList=[]
        paraList.append(i1)
        paraList.append(i2)
        paraList.append(i3)
        paraList.append(i4)
        paraList.append(i5)
        self.setVisible(1)
    #选项框状态修改
    def btnStateChange(self):
        s1=str(self.comboBox.currentText())
        if s1=='串口':
            readConfigurationFile("Serial").setCon("serial_or_udp", "1")
            # myconfig = configparser.ConfigParser()
            # myconfig.read('config.ini')
            # myconfig.set("Serial","serial_or_udp","1")
            # myconfig.write(open("config.ini", "w+"))
        else:
            readConfigurationFile("Serial").setCon("serial_or_udp", "0")
            # myconfig = configparser.ConfigParser()
            # myconfig.read('config.ini')
            # myconfig.set("Serial", "serial_or_udp", "0")
            # myconfig.write(open("config.ini", "w+"))

    '''
        测量过程中主页面显示函数
        根据标志位flag=1时，将测量按钮设为禁用状态，当测量结束后并调用拓扑发现算法，恢复测量到的网络拓扑结构
        标志位flag！=1时，则表明测量过程中出现错误，要想重新测量则将测量按钮激活，否则的话退出程序
    '''
    # 测量过程中主页面显示的逻辑
    def changeUI(self, flag):
        if flag == 1:
            self.pushButton_3.setEnabled(True)
            # self.pushButton.setEnabled(False)
            self.printAction2.setEnabled(True)
            self.printAction3.setEnabled(True)
            self.pushButton_4.setText('启动测量')
            self.pushButton_4.setDisabled(False)
            end = QMessageBox.information(self, "测量结束提示框", "结束测量，是否开始显示", QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.Yes)
            if end == QMessageBox.Yes:
                    # 直接调用数据库信息
                    # Topo.getTopo()
                    # Topo.Main('R')
                    time.sleep(1)
                    self.topo.start()
                    self.counttopo.start()
                    self.pushButton_4.setText('正在计算拓扑')
                    self.pushButton_4.setDisabled(True)
                    self.pushButton_3.setEnabled(False)
                    self.pushButton.setEnabled(False)
                    # self.pushButton_4.setEnabled(False)
                    self.printAction2.setEnabled(False)
                    self.printAction3.setEnabled(False)
                    # print('计算完成')
                    # # self.reMeasure()
                    # sql = "select * from newtopo_b"
                    # newNodeList1 = self.getTopo(sql)
                    # self.initialization(newNodeList1)
                    # print('拓扑已显示')

        else:
            start = QMessageBox.information(self, "测量错误提示框", "是否重新测量？", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if start == QMessageBox.Yes:
                self.pushButton_3.setEnabled(True)
                # self.pushButton.setEnabled(False)
                self.printAction2.setEnabled(True)
                self.printAction3.setEnabled(True)
                self.pushButton_4.setText('启动测量')
                self.pushButton_4.setDisabled(False)
            else:
                self.tuichu()


    '''
        拓扑计算完成后的拓扑显示函数
        计算完成后将菜单栏中的“时延测量”、“幅频显示”选项的状态激活
        若是计算过程中出错则直接退出程序 
    '''
    # 拓扑计算完成后的拓扑显示函数
    def newToposhow(self,flag):
        if flag==1:
            self.pushButton_4.setText('计算完成')
            self.pushButton_4.setDisabled(False)
            self.pushButton_3.setDisabled(False)
            # self.pushButton_3.setEnabled(True)
            self.pushButton.setEnabled(False)
            # self.pushButton_4.setEnabled(False)
            self.printAction2.setEnabled(True)
            self.printAction3.setEnabled(True)
            logging.info('计算完成')
            # self.reMeasure()
            time.sleep(1)
            sql = "select * from newTopo_A"
            newNodeList = self.getTopo(sql)
            self.initialization(newNodeList)
            self.pushButton_4.setText('启动测量')
            self.old=5
            self.pushButton_3.setText("相位2当前拓扑")
            QApplication.processEvents()
            logging.info('拓扑已显示')
        else:
            start = QMessageBox.information(self, "计算错误提示框", "拓扑计算出错，退出！", QMessageBox.Yes,QMessageBox.Yes)
            if start == QMessageBox.Yes:
                self.tuichu()
    '''
        设置进度条值的函数
        showcount()：将已测量节点数目线程返回的数值处理后，设置进度条的值
        showcounttopo()：将拓扑计算算法过程的线程返回数值处理后，设置进度条的值
    '''
    def showcount(self,connect_num):
        self.step = (connect_num / num) * 85
        self.progressBar.setValue(int(self.step))
        self.label_6.setText('已经测量了 %d 个点'%connect_num)
        # print('已经测量了 %d 个点'%connect_num)
    def showcounttopo(self, measure_num):
        self.step = measure_num + 85
        self.progressBar.setValue(self.step)
        self.label_6.setText("正在计算拓扑")
        # print('已经计算了 %f' % float(measure_num/15))
    '''
        系统繁忙页面返回信号的槽函数
        若是选择重新发送操作选项，则是直接返回主页面
        若是选择取消操作选项，则是调用接口程序
    '''
    # 系统繁忙
    def busy_backsignal5(self,num):
        if num==1:
            # 重新发送操作
            self.setVisible(1)
        else:
            # ser.cancel_order()
            self.setVisible(1)
    def settreeflag(self, flag):
        global tree_flag
        tree_flag = flag
    '''
        主页面显示函数
        （1）节点目录和节点信息目录清空
        （2）查询数据库节点信息，设置节点目录treeWidget和节点信息目录tableWidget中的信息
        （3）调用isclick函数，点击节点目录treeWidget中的节点，会在节点信息目录tableWidget中显示相应的节点信息
        （4）调用topo_show函数，显示恢复的网络拓扑
    '''
    # 默认显示之前的页面
    def initialization(self,nodelist):
        logging.info('页面初始化开始')
        # self.pushButton_4.setText('正在显示拓扑')
        # global oldNodeList,oldRealList,oldNodeList1,oldRealList1,newNodeList,newRealList,newNodeList1,newRealList1
        # sql= "select * from oldTopo"
        # sql = "select * from oldTopo_a"
        # sql = "select * from oldtopo_b"
        # oldNodeList = self.getTopo(sql)
        # sql1 = "select * from oldtopo_a"
        # oldNodeList1 = self.getTopo(sql1)
        global  reallist
        reallist=self.getRealNode(nodelist)
        # if self.old==1:
        # oldRealList = self.getRealNode(oldNodeList)
        self.treeWidget.clear()
        self.tableWidget.clear()
        # 树状目录初始化
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setColumnWidth(0, 50)
        # self.treeWidget.setHeaderLabels(["分组"])
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        groupname='root'
        # root1 = self.creategroup(groupname, oldRealList)
        root1 = self.creategroup(groupname, reallist)
        root1.setExpanded(False)
        # 设置树状结构最外层节点的图标显示
        i = 0
        while i < self.treeWidget.topLevelItemCount():
            self.treeWidget.topLevelItem(i).setIcon(0, QIcon(':/myIcons/房.jpg'))
            i = i + 1
        # 表格初始化
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['名字', '与父节点的距离'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)
        self.treeWidget.itemClicked.connect(self.isclick)
        # 拓扑显示窗口
        # 显示拓扑
        t1 = threading.Thread(target=self.topo_show(nodelist), name='function')
        t1.start()
        # self.showold.start()
        logging.info('页面初始化完成')
    '''
        联机函数
        调用接口程序，根据接口程序返回的标志位flag进行相应的操作
        flag=1，则表示联机成功，并调用connectEnd()函数
        flag=-1，则表示系统繁忙，并调用showBusy()函数
        flag！=1且flag！=-1，则表示联机出错，并调用connectEnd()函数，退出程序
        
    '''
    # 联机函数
    def connect(self):
        logging.info('联机开始')
        global num
        # 根据设定的参数来进行联机操作
        (flag, num) = ser.build_order()
        #num=70
        # print(flag)
        flag=1
        if flag == 1:
            self.connectError = False
            self.connectEnd()
        elif flag == -1:
            self.showBusy()
        else:
            self.connectError = True
            self.connectEnd()
    '''
        联机是否成功函数
        connectError= True，则表示联机出错，退出程序
        connectError= False，则表示联机成功，将联机按钮状态设为禁用，其余按钮设为激活状态
    '''
    def connectEnd(self):
        if self.connectError:
            QMessageBox.information(self, "联机出错提示框", "组网未成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            time.sleep(2)
            # 模拟退出页面
            self.tuichu()
        else:
            QMessageBox.information(self, "联机成功提示框", "联机成功", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)     #20200120 by e
            self.pushButton.setEnabled(False)
            self.pushButton.setText('已联机')
            # self.pushButton_3.setEnabled(True)
            self.pushButton_3.setDisabled(False)
            self.old=2
            self.pushButton_3.setText('相位2历史拓扑')
            self.pushButton_4.setEnabled(True)
            self.printAction2.setEnabled(True)
            self.printAction3.setEnabled(True)
            self.comboBox.setDisabled(True)
            QApplication.processEvents()
        logging.info('联机完成')

    '''
        拓扑切换函数，根据self.old值显示拓扑图
        self.old=1，显示相位2历史拓扑图
        self.old=2，显示相位1当前拓扑图
        self.old=3，显示相位2当前拓扑图
        self.old！=1且self.old！=2且self.old！=3，显示相位1历史拓扑图
    '''
    #拓扑控制按钮
    def startShow(self):
        logging.info('拓扑切换开始')
        global oldNodeList,oldNodeList1,newNodeList,newNodeList1
        # print(self.old)
        if self.old==1:
            # self.topo_show(oldNodeList)
            sql = "select * from oldTopo_A"
            oldNodeList = self.getTopo(sql)
            self.initialization(oldNodeList)
            QApplication.processEvents()
            self.pushButton_3.setText("相位2历史拓扑")
            self.old = 2
        elif self.old==2:
            sql = "select * from oldTopo_B"
            oldNodeList1 = self.getTopo(sql)
            self.initialization(oldNodeList1)
            # self.topo_show(oldNodeList1)
            QApplication.processEvents()
            self.pushButton_3.setText("相位3历史拓扑")
            self.old = 3
        elif self.old==3:
            sql = "select * from oldTopo_C"
            oldNodeList1 = self.getTopo(sql)
            self.initialization(oldNodeList1)
            # self.topo_show(oldNodeList1)
            QApplication.processEvents()
            self.pushButton_3.setText("相位1当前拓扑")
            self.old = 4
        elif self.old==4:
            sql = "select * from newTopo_A"
            newNodeList = self.getTopo(sql)
            self.initialization(newNodeList)
            # self.topo_show(newNodeList)
            QApplication.processEvents()
            self.pushButton_3.setText("相位2当前拓扑")
            self.old = 5

        elif self.old==5:
            sql = "select * from newTopo_B"
            newNodeList1 = self.getTopo(sql)
            self.initialization(newNodeList1)
            # self.topo_show(newNodeList1)
            QApplication.processEvents()
            self.pushButton_3.setText("相位3当前拓扑")
            self.old = 0
        elif self.old==0:
            sql = "select * from newTopo_C"
            newNodeList1 = self.getTopo(sql)
            self.initialization(newNodeList1)
            # self.topo_show(newNodeList1)
            QApplication.processEvents()
            self.pushButton_3.setText("相位1历史拓扑")
            self.old = 1
        logging.info('拓扑切换完成')

    '''
        节点目录创建分组函数、节点点击和节点信息显示联动函数
    '''
    # 节点目录创建分组
    def creategroup(self, groupname, childList):
        group = QTreeWidgetItem(self.treeWidget)
        num_child = len(childList)
        j = 0
        while j < num_child:
            dict1 = childList[j].getName()
            child = QTreeWidgetItem()
            child.setText(0, dict1)
            child.setIcon(0, QIcon(':/myIcons/绿.jpg'))
            child.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            j = j + 1
            group.addChild(child)
        group.setText(0, groupname)
        return group
    # 节点点击和拓扑显示联动
    def isclick(self,item,column):
        # 最小的节点，输出节点信息
        global reallist
        if item.child(0) is None:
            for i in range(0,len(reallist)):
                if item.text(column) == reallist[i].getName():
                    newItem1 = QTableWidgetItem(reallist[i].getName())
                    self.tableWidget.setItem(0, 0, newItem1)
                    newItem2 = QTableWidgetItem(str(reallist[i].getLength()))
                    self.tableWidget.setItem(0, 1, newItem2)
                    break
        else:
            newItem1 = QTableWidgetItem(reallist[0].getName())
            self.tableWidget.setItem(0, 0, newItem1)
            newItem2 = QTableWidgetItem(str(reallist[0].getLength()))
            self.tableWidget.setItem(0, 1, newItem2)
    # 开始测量页面显示的槽函数，调用接口程序并将已测量节点数目返回主页面
    def startMeasure(self):
        logging.info('重新测量开始')
        # 弹出参数设置页面
        logging.info('参数设置')
        # 测量开始提示框
        start = QMessageBox.information(self, "测量开始提示框", "是否开始测量？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if start == QMessageBox.Yes:
            # 通知串口开始测量，测量结束后，弹出测量结束提示框
            # 测量出错，返回出错信息
            self.startM.start()
            self.countnum.start()
            # self.countnum.count.connect(self.showcount)
            self.pushButton_4.setText('正在测量')
            self.pushButton_4.setDisabled(True)
            self.pushButton_3.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.printAction2.setEnabled(False)
            self.printAction3.setEnabled(False)
        logging.info('重新测量结束')

    # 重新测量
    def reMeasure(self):
        logging.info('重新测量页面开始显示')
        global newNodeList, newRealList,newNodeList1
        # sql = "select * from newTopo_A"
        sql = "select * from newTopo_B"
        newNodeList = self.getTopo(sql)
        sql1 = "select * from newTopo_A"
        newNodeList1 = self.getTopo(sql1)
        newRealList = self.getRealNode(newNodeList)
        self.treeWidget.clear()
        self.tableWidget.clear()
        logging.info('节点信息显示')
        # 树状目录初始化
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setColumnWidth(0, 50)
        # self.treeWidget.setHeaderLabels(["分组"])
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # 添加串口通信函数
        # 添加算法函数
        # 树状目录节点设置
        groupname = 'root'
        root1 = self.creategroup(groupname, newRealList)
        root1.setExpanded(False)
        # 设置树状结构最外层节点的图标显示
        self.treeWidget.topLevelItem(0).setIcon(0, QIcon(':/myIcons/房.jpg'))
        # 表格初始化
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels([ '名字', '与父节点的距离'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        QTableWidget.resizeColumnsToContents(self.tableWidget)
        QTableWidget.resizeRowsToContents(self.tableWidget)
        self.treeWidget.itemClicked.connect(self.newisclick)
        logging.info('节点信息显示完成')
        # self.graphicsView.scene.update()
        # 拓扑显示窗口
        #self.graphicsView.scene = QtWidgets.QGraphicsScene(0, 0, 1920, 1080)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsView.setSceneRect(0, 0, 3840, 1160)  # fix scene size 500 500
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  ##设置视图的抗锯齿渲染模式。
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        # self.showPicture(path)
        logging.info('拓扑显示')
        t1 = threading.Thread(target=self.topo_show(newNodeList), name='function')
        t1.start()
        logging.info('重新测量页面完成显示')

        # 节点点击和拓扑显示联动
    def newisclick(self, item, column):
        # 最小的节点，输出节点信息
        global newRealList
        if item.child(0) is None:
            for i in range(0, len(newRealList)):
                if item.text(column) == newRealList[i].getName():
                    newItem1 = QTableWidgetItem(newRealList[i].getName())
                    self.tableWidget.setItem(0, 0, newItem1)
                    newItem2 = QTableWidgetItem(newRealList[i].getLength())
                    self.tableWidget.setItem(0, 1, newItem2)
                    break
        else:
            newItem1 = QTableWidgetItem(newRealList[0].getName())
            self.tableWidget.setItem(0, 0, newItem1)
            newItem2 = QTableWidgetItem(newRealList[0].getLength())
            self.tableWidget.setItem(0, 1, newItem2)
    '''
        处理读取到的数据库信息的函数
        getTopo():读取数据库中的内容，并将数据库中每一行的数据使用Node对象存储起来，将全部数据使用list数据类型存储
        getRoot()：获取getTopo()函数返回的list数据类型中的root节点
        getRealNode()：获取getTopo()函数返回的list数据类型中的真实节点，返回list数据类型
    '''
    def getTopo(self, sql):
        newList = []
        IDListNew = {}
        try:
            results = Sqlite().select(sql)
            for row in results:
                node = Node()
                IDListNew[row[0]] = node
                newList.append(node)
            for row in results:
                n = IDListNew.get(row[0])
                if row[1] != None:
                    n.setName(row[1])
                if row[2] != None:
                    n.setFather(IDListNew.get(row[2]))
                    n.setLength(row[3])
                if row[4] != None:
                    n.setFirstChild(IDListNew.get(row[4]))
                if row[5] != None:
                    n.setRightBrother(IDListNew.get(row[5]))
                if row[6] == 1:
                    n.setisVirtualNode(True)
        except:
            print("No Data")
        return newList
    def getRoot(self, List: list):
        node = Node()
        for n in List:
            if n.getFather() == None:
                node = n
                break
        return node
    def getRealNode(self, List: list):
        RealNodeList = []
        for node in List:
            if node.getisVirtualNode():
                continue
            RealNodeList.append(node)
        return RealNodeList

    def create_icon(self, type, x, y):
        ccoimage = QImage('../Interface/cco.png')
        steimage = QImage('../Interface/ste.png')
        vimage = QImage('../Interface/v.png')
        if type == "cco":
            ret = QGraphicsPixmapItem(QPixmap.fromImage(ccoimage))
        elif type == "ste":
            ret = QGraphicsPixmapItem(QPixmap.fromImage(steimage))
        else:
            ret = QGraphicsPixmapItem(QPixmap.fromImage(vimage))
        ret.setPos(x, y)
        self.scene.addItem(ret)
        return ret
    def topo_show(self,List:list):
        logging.info('拓扑开始显示')
        icon_width = 32
        root_node = self.getRoot(List)
        toponodes = []
        toponodes.append(root_node)
        icons = []
        icon_count = 0
        sip.delete(self.graphicsView.scene)
        self.graphicsView.scene = QtWidgets.QGraphicsScene(0, 0, 1920, 1080)
        self.graphicsView.setScene(self.graphicsView.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.graphicsView.setSceneRect(0, 0, 3840, 1160)  # fix scene size 500 500
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  ##设置视图的抗锯齿渲染模式。
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        for node in toponodes:
            # for node in newList:
            (y, x) = topo_picture().icon_locate(node, icon_width, icon_width, 100, 100)
            #print("Node", node.getName(), x, y)
            if node == root_node:
                iconi = self.create_icon("cco", x, y)
                icons.append(iconi)
                iconi.setPos(x, y)
                icon_count = icon_count + 1
                self.root_name = QGraphicsTextItem(str(node.getName()))
                #self.root_name.setFont(QFont("Times",6))
                self.root_name.setDefaultTextColor(Qt.darkBlue)
                self.root_name.setPos(QPointF(x, y + icon_width / 2 + 7))
                self.scene.addItem(self.root_name)
            else:
                xp = x + icon_width / 2
                yp = y + icon_width / 2
                node_father = node.getFather()
                (fy, fx) = topo_picture().icon_locate(node_father, icon_width, icon_width, 100, 100)
                fxp = fx + icon_width / 2
                fyp = fy + icon_width / 2
                self.scene.addLine(xp, yp, fxp, fyp, QPen(Qt.black))
                # QApplication.processEvents()
                ky = fyp - yp
                kx = fxp - xp
                if ky != 0:
                    k = kx / ky
                # 往直线上添加其与父节点之间的距离
                self.context = QGraphicsTextItem(str(node.getLength()))
                self.context.setDefaultTextColor(Qt.darkCyan)
                if ky == 0 or k == 0:
                    self.context.setPos(QPointF((xp + fxp - icon_width/8) / 2, (yp + fyp - icon_width) / 2))
                else:
                    self.context.setPos(QPointF((xp + fxp + icon_width/8) / 2, (yp + fyp - icon_width) / 2))
                #self.context.setPos(QPointF((xp + fxp - icon_width) / 2, (yp + fyp - icon_width) / 2))
                self.context.setFont(QFont("Times", 8))
                self.scene.addItem(self.context)
                # QApplication.processEvents()

                if node.getisVirtualNode():
                    self.scene.addRect(x + icon_width / 2 - 4, y + icon_width / 2 - 4, 8, 8, QPen(Qt.blue),QBrush(Qt.darkBlue))
                    # QApplication.processEvents()
                else:
                    iconi = self.create_icon("ste", x, y)
                    icons.append(iconi)
                    iconi.setPos(x, y)
                    # 添加真实节点的名字
                    self.name = QGraphicsTextItem(str(node.getName()[-4:]))
                    #self.name.setFont(QFont("Times", 6))
                    # self.name.setDefaultTextColor(QColor(0, 160, 230))
                    self.name.setDefaultTextColor(Qt.darkBlue)
                    self.name.setPos(QPointF(x, y + icon_width / 2 + 7))
                    self.scene.addItem(self.name)
                    # QApplication.processEvents()

            child = node.getFirstChild()
            while child is not None:
                for node_child in List:
                    if child == node_child:
                        toponodes.append(node_child)
                child = child.getRightBrother()
            # self.pushButton_4.setText('启动测量')
            # QApplication.processEvents()

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    app.processEvents()
    the_window = myWindow()
    the_window.show()
    sys.exit(app.exec_())
    #刷新 QApplication.processEvents()