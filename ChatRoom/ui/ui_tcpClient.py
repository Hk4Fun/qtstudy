# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tcpClient.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(434, 549)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.contentListWidget = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.contentListWidget.setFont(font)
        self.contentListWidget.setObjectName("contentListWidget")
        self.gridLayout.addWidget(self.contentListWidget, 0, 0, 1, 3)
        self.sendLineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.sendLineEdit.setFont(font)
        self.sendLineEdit.setObjectName("sendLineEdit")
        self.gridLayout.addWidget(self.sendLineEdit, 1, 0, 1, 2)
        self.sendBtn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.sendBtn.setFont(font)
        self.sendBtn.setObjectName("sendBtn")
        self.gridLayout.addWidget(self.sendBtn, 1, 2, 1, 1)
        self.userNameLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.userNameLabel.setFont(font)
        self.userNameLabel.setObjectName("userNameLabel")
        self.gridLayout.addWidget(self.userNameLabel, 2, 0, 1, 1)
        self.userNameLineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.userNameLineEdit.setFont(font)
        self.userNameLineEdit.setObjectName("userNameLineEdit")
        self.gridLayout.addWidget(self.userNameLineEdit, 2, 1, 1, 2)
        self.serverIPLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.serverIPLabel.setFont(font)
        self.serverIPLabel.setObjectName("serverIPLabel")
        self.gridLayout.addWidget(self.serverIPLabel, 3, 0, 1, 1)
        self.serverIPLineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.serverIPLineEdit.setFont(font)
        self.serverIPLineEdit.setObjectName("serverIPLineEdit")
        self.gridLayout.addWidget(self.serverIPLineEdit, 3, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.portLineEdit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.portLineEdit.setFont(font)
        self.portLineEdit.setObjectName("portLineEdit")
        self.gridLayout.addWidget(self.portLineEdit, 4, 1, 1, 2)
        self.enterBtn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.enterBtn.setFont(font)
        self.enterBtn.setObjectName("enterBtn")
        self.gridLayout.addWidget(self.enterBtn, 5, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TCP Client"))
        self.sendBtn.setText(_translate("Form", "Send"))
        self.userNameLabel.setText(_translate("Form", "User Name："))
        self.serverIPLabel.setText(_translate("Form", "Server IP："))
        self.label_3.setText(_translate("Form", "Server Port："))
        self.enterBtn.setText(_translate("Form", "Enter Chat Room"))

