# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Reporter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 500)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.horizontalLayout.addWidget(self.radioButton_4)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dateEdit = QtWidgets.QDateEdit(self.page)
        self.dateEdit.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.dateEdit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1753, 9, 14), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.page_2)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_3)
        self.comboBox = QtWidgets.QComboBox(self.page_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.stackedWidget.addWidget(self.page_2)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox_4 = QtWidgets.QComboBox(self.page_4)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_4)
        self.comboBox_5 = QtWidgets.QComboBox(self.page_4)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_5)
        self.stackedWidget.addWidget(self.page_4)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.page_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox_2)
        self.stackedWidget.addWidget(self.page_3)
        self.horizontalLayout_4.addWidget(self.stackedWidget)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btRefresh = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btRefresh.setFont(font)
        self.btRefresh.setObjectName("btRefresh")
        self.horizontalLayout_5.addWidget(self.btRefresh)
        self.btSettle = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btSettle.setFont(font)
        self.btSettle.setObjectName("btSettle")
        self.horizontalLayout_5.addWidget(self.btSettle)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabDatail = QtWidgets.QWidget()
        self.tabDatail.setObjectName("tabDatail")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabDatail)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tbDetail = QtWidgets.QTableWidget(self.tabDatail)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tbDetail.setFont(font)
        self.tbDetail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tbDetail.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbDetail.setObjectName("tbDetail")
        self.tbDetail.setColumnCount(11)
        self.tbDetail.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbDetail.setHorizontalHeaderItem(10, item)
        self.verticalLayout_2.addWidget(self.tbDetail)
        self.tabWidget.addTab(self.tabDatail, "")
        self.tabBillList = QtWidgets.QWidget()
        self.tabBillList.setObjectName("tabBillList")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabBillList)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tbBillList = QtWidgets.QTableWidget(self.tabBillList)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tbBillList.setFont(font)
        self.tbBillList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tbBillList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbBillList.setObjectName("tbBillList")
        self.tbBillList.setColumnCount(7)
        self.tbBillList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbBillList.setHorizontalHeaderItem(6, item)
        self.verticalLayout_4.addWidget(self.tbBillList)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.tabBillList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.label_totalIncome = QtWidgets.QLabel(self.tabBillList)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_totalIncome.setFont(font)
        self.label_totalIncome.setText("")
        self.label_totalIncome.setObjectName("label_totalIncome")
        self.horizontalLayout_6.addWidget(self.label_totalIncome)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tabBillList, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.tabWidget.raise_()
        self.stackedWidget.raise_()
        self.btSettle.raise_()

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "报表"))
        self.groupBox.setTitle(_translate("Form", "报表类型"))
        self.radioButton.setText(_translate("Form", "日报表"))
        self.radioButton_2.setText(_translate("Form", "月报表"))
        self.radioButton_4.setText(_translate("Form", "季报表"))
        self.radioButton_3.setText(_translate("Form", "年报表"))
        self.dateEdit.setDisplayFormat(_translate("Form", "yyyy/M/dd"))
        self.comboBox_3.setItemText(0, _translate("Form", "2018年"))
        self.comboBox.setItemText(0, _translate("Form", "一月"))
        self.comboBox.setItemText(1, _translate("Form", "二月"))
        self.comboBox.setItemText(2, _translate("Form", "三月"))
        self.comboBox.setItemText(3, _translate("Form", "四月"))
        self.comboBox.setItemText(4, _translate("Form", "五月"))
        self.comboBox.setItemText(5, _translate("Form", "六月"))
        self.comboBox.setItemText(6, _translate("Form", "七月"))
        self.comboBox.setItemText(7, _translate("Form", "八月"))
        self.comboBox.setItemText(8, _translate("Form", "九月"))
        self.comboBox.setItemText(9, _translate("Form", "十月"))
        self.comboBox.setItemText(10, _translate("Form", "十一月"))
        self.comboBox.setItemText(11, _translate("Form", "十二月"))
        self.comboBox_4.setItemText(0, _translate("Form", "2018年"))
        self.comboBox_5.setItemText(0, _translate("Form", "第一季度"))
        self.comboBox_5.setItemText(1, _translate("Form", "第二季度"))
        self.comboBox_5.setItemText(2, _translate("Form", "第三季度"))
        self.comboBox_5.setItemText(3, _translate("Form", "第四季度"))
        self.comboBox_2.setItemText(0, _translate("Form", "2018年"))
        self.btRefresh.setText(_translate("Form", "刷新"))
        self.btSettle.setText(_translate("Form", "结帐"))
        self.tbDetail.setSortingEnabled(True)
        item = self.tbDetail.horizontalHeaderItem(0)
        item.setText(_translate("Form", "房间号"))
        item = self.tbDetail.horizontalHeaderItem(1)
        item.setText(_translate("Form", "用户等级"))
        item = self.tbDetail.horizontalHeaderItem(2)
        item.setText(_translate("Form", "开机时间"))
        item = self.tbDetail.horizontalHeaderItem(3)
        item.setText(_translate("Form", "关机时间"))
        item = self.tbDetail.horizontalHeaderItem(4)
        item.setText(_translate("Form", "时长"))
        item = self.tbDetail.horizontalHeaderItem(5)
        item.setText(_translate("Form", "调温次数"))
        item = self.tbDetail.horizontalHeaderItem(6)
        item.setText(_translate("Form", "回温次数"))
        item = self.tbDetail.horizontalHeaderItem(7)
        item.setText(_translate("Form", "调风次数"))
        item = self.tbDetail.horizontalHeaderItem(8)
        item.setText(_translate("Form", "耗能（kW·h）"))
        item = self.tbDetail.horizontalHeaderItem(9)
        item.setText(_translate("Form", "费用（元）"))
        item = self.tbDetail.horizontalHeaderItem(10)
        item.setText(_translate("Form", "单号"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDatail), _translate("Form", "详单"))
        self.tbBillList.setSortingEnabled(True)
        item = self.tbBillList.horizontalHeaderItem(0)
        item.setText(_translate("Form", "日期"))
        item = self.tbBillList.horizontalHeaderItem(1)
        item.setText(_translate("Form", "单号"))
        item = self.tbBillList.horizontalHeaderItem(2)
        item.setText(_translate("Form", "房间号"))
        item = self.tbBillList.horizontalHeaderItem(3)
        item.setText(_translate("Form", "用户级别"))
        item = self.tbBillList.horizontalHeaderItem(4)
        item.setText(_translate("Form", "总消费（元）"))
        item = self.tbBillList.horizontalHeaderItem(5)
        item.setText(_translate("Form", "折扣率"))
        item = self.tbBillList.horizontalHeaderItem(6)
        item.setText(_translate("Form", "应收金额（元）"))
        self.label.setText(_translate("Form", "总收入（元）："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBillList), _translate("Form", "账单"))

