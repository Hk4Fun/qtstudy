# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Controller.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(728, 408)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btClose = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btClose.setFont(font)
        self.btClose.setObjectName("btClose")
        self.horizontalLayout.addWidget(self.btClose)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinRefresh = QtWidgets.QDoubleSpinBox(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.spinRefresh.setFont(font)
        self.spinRefresh.setWrapping(False)
        self.spinRefresh.setDecimals(1)
        self.spinRefresh.setSingleStep(0.5)
        self.spinRefresh.setProperty("value", 5.0)
        self.spinRefresh.setObjectName("spinRefresh")
        self.horizontalLayout.addWidget(self.spinRefresh)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.btReport = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btReport.setFont(font)
        self.btReport.setObjectName("btReport")
        self.horizontalLayout.addWidget(self.btReport)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableSubMachine = QtWidgets.QTableWidget(Form)
        self.tableSubMachine.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableSubMachine.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableSubMachine.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableSubMachine.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableSubMachine.setObjectName("tableSubMachine")
        self.tableSubMachine.setColumnCount(7)
        self.tableSubMachine.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSubMachine.setHorizontalHeaderItem(6, item)
        self.tableSubMachine.horizontalHeader().setCascadingSectionResizes(False)
        self.tableSubMachine.horizontalHeader().setDefaultSectionSize(100)
        self.tableSubMachine.horizontalHeader().setSortIndicatorShown(False)
        self.tableSubMachine.horizontalHeader().setStretchLastSection(False)
        self.tableSubMachine.verticalHeader().setHighlightSections(True)
        self.tableSubMachine.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.tableSubMachine)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "中控机"))
        self.btClose.setText(_translate("Form", "开机"))
        self.label.setText(_translate("Form", "刷新频率"))
        self.btReport.setText(_translate("Form", "报表"))
        self.tableSubMachine.setSortingEnabled(True)
        item = self.tableSubMachine.horizontalHeaderItem(0)
        item.setText(_translate("Form", "房间号"))
        item = self.tableSubMachine.horizontalHeaderItem(1)
        item.setText(_translate("Form", "模式"))
        item = self.tableSubMachine.horizontalHeaderItem(2)
        item.setText(_translate("Form", "当前温度"))
        item = self.tableSubMachine.horizontalHeaderItem(3)
        item.setText(_translate("Form", "设定温度"))
        item = self.tableSubMachine.horizontalHeaderItem(4)
        item.setText(_translate("Form", "风速"))
        item = self.tableSubMachine.horizontalHeaderItem(5)
        item.setText(_translate("Form", "耗能"))
        item = self.tableSubMachine.horizontalHeaderItem(6)
        item.setText(_translate("Form", "当前计费"))

