from PyQt5.QtWidgets import QMessageBox
from Interface.connect import Ui_connect
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import sys
textList=[500,3,20,10,4]
# from getTopo import *
# 输出的是变量：‘汉字’+str(变量名)
import logging
# import  serial_test01 as ser
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO, filename='../log/procedure.log', filemode ='w', )
'''
            参数设置页面，页面参数信息会自动显示上次页面设置的参数，定义了两个返回信号
            单击确定按钮会返回参数设置页面中设置的5个参数值
            点击取消按钮不会返回任何参数值
'''
class connectWindow(QtWidgets.QMainWindow,Ui_connect):
    # 定义返回之前界面的信号
    backsignal3=pyqtSignal(int,int,int,int,int)
    backsignal4=pyqtSignal()
    def __init__(self):
        super(connectWindow,self).__init__()
        # 加载连接窗口
        self.setupUi(self)
        # 显示上次设置的参数信息
        global textList
        self.textEdit.setText(str(textList[0]))
        self.textEdit.setAlignment(Qt.AlignHCenter)
        self.textEdit_2.setText(str(textList[1]))
        self.textEdit_2.setAlignment(Qt.AlignHCenter)
        self.textEdit_3.setText(str(textList[2]))
        self.textEdit_3.setAlignment(Qt.AlignHCenter)
        self.textEdit_4.setText(str(textList[3]))
        self.textEdit_4.setAlignment(Qt.AlignHCenter)
        self.textEdit_5.setText(str(textList[4]))
        self.textEdit_5.setAlignment(Qt.AlignHCenter)
        # 确定按钮
        self.pushButton.clicked.connect(self.backmain)
        # 取消按钮
        self.pushButton_2.clicked.connect(lambda: self.cancelbt())
        logging.info('参数设置页面')
    # 取消按钮的槽函数
    def cancelbt(self):
        self.backsignal4.emit()
        self.setVisible(0)
    # 确定按钮的槽函数，i1,i2,i3,i4,i5是参数设置页面中设置的参数
    def backmain(self):
        global textList
        i1 = int(self.textEdit.toPlainText())
        i2 = int(self.textEdit_2.toPlainText())
        i3 = int(self.textEdit_3.toPlainText())
        i4 = int(self.textEdit_4.toPlainText())
        i5 = int(self.textEdit_5.toPlainText())
        textList = []
        textList.append(i1)
        textList.append(i2)
        textList.append(i3)
        textList.append(i4)
        textList.append(i5)
        if i1 in range(0,65536) and i2 in range(0,11) and i3 in range(1,256) and i4 in range(1,256) and i5 in range(1,256):
            self.backsignal3.emit(i1, i2, i3, i4, i5)
            self.setVisible(0)
        else:
            QMessageBox.about(self,'消息提示框','请输入正确参数信息')
            return
        logging.info('参数设置完成，返回主页面')

if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    the_window = connectWindow()
    the_window.show()
    sys.exit(app.exec_())