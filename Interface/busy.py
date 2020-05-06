# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'busy.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_busy(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(350, 250)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 50, 211, 51))
        self.label.setStyleSheet("font: 12pt \"Arial\";")
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(40, 160, 89, 21))
        self.radioButton.setStyleSheet("font: 11pt \"Arial\";")
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(220, 160, 89, 21))
        self.radioButton_2.setStyleSheet("font: 11pt \"Arial\";")
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "繁忙页面"))
        self.label.setText(_translate("Form", "当前繁忙，请选择以下操作："))
        self.radioButton.setText(_translate("Form", "重新发送"))
        self.radioButton_2.setText(_translate("Form", "中止操作"))
