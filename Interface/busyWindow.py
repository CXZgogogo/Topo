from Interface.busy import Ui_busy
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import sys
import logging
# import  serial_test01 as ser
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO, filename='../Main/procedure.log', filemode ='w', )
'''
    繁忙页面，设置了一个返回信号
    选择重新操作选项，会返回数字1
    选择停止操作选项，会返回数字2
'''
class busyWindow(QtWidgets.QMainWindow,Ui_busy):
    # 定义返回之前界面的信号
    backsignal5=pyqtSignal(int)
    def __init__(self):
        super(busyWindow,self).__init__()
        self.setupUi(self) #加载连接窗口
        self.radioButton.setChecked(True)
        # 重新操作选项按钮
        self.radioButton.clicked.connect(lambda:self.restart() )
        # 停止操作选项按钮
        self.radioButton_2.clicked.connect(lambda:self.stop())
        logging.info('系统繁忙选择页面')
    # 重新操作按钮的槽函数
    def restart(self):
        # 判断按钮的状态：是否被选中
        if self.radioButton.isChecked():
            self.radioButton.setChecked(False)
        self.backsignal5.emit(1)
        logging.info('重新操作')
        self.setVisible(0)
    # 停止按钮的槽函数
    def stop(self):
        # 判断按钮的状态：是否被选中
        if self.radioButton.isChecked():
            self.radioButton2.setChecked(False)
        self.backsignal5.emit(2)
        logging.info('停止操作')
        self.setVisible(0)
if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    the_window = busyWindow()
    the_window.show()
    sys.exit(app.exec_())