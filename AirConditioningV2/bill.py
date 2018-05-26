__author__ = 'Hk4Fun'
__date__ = '2018/5/26 2:17'

import sys

from PyQt5.QtWidgets import (QWidget, QHeaderView, QTableWidgetItem)

sys.path.append('..')
from AirConditioningV2.ui import ui_Bill, ui_BillList
from AirConditioningV2.filters import *


class Bill(QWidget):
    def __init__(self, db, orderId):
        super().__init__()
        self.db = db
        self.query = self.db.query
        self.orderId = orderId
        self.initUi()

    def initUi(self):
        self.ui = ui_Bill.Ui_Form()
        self.ui.setupUi(self)
        self.ui.btPrinter.clicked.connect(self.printBill)
        self.showBill()

    def showBill(self):
        sql = 'SELECT * FROM bill_list WHERE orderID = ?'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, self.orderId)
        self.db.sqlExec()
        self.query.next()
        self.ui.label_date.setText(self.query.value(0))
        self.ui.label_orderId.setText(self.query.value(1))
        self.ui.label_roomId.setText(self.query.value(2))
        self.ui.label_userLevel.setText(mapUserLevel_c2w(self.query.value(3)))
        self.ui.label_cost.setText(str(round(self.query.value(4), 2)))
        self.ui.label_discount.setText(discountFormat(self.query.value(5)))
        self.ui.label_receive.setText(str(round(self.query.value(6), 2)))

    def printBill(self):
        pass


class BillList(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.query = self.db.query
        self.initUi()

    def initUi(self):
        self.ui = ui_BillList.Ui_Form()
        self.ui.setupUi(self)
        header = self.ui.tbBillList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.btRefresh.clicked.connect(self.showBillList)
        self.ui.tbBillList.cellDoubleClicked.connect(self.showBill)
        self.showBillList()

    def showBillList(self):
        self.ui.tbBillList.clearContents()
        self.ui.tbBillList.setSortingEnabled(False)
        self.db.sqlExec('SELECT * FROM bill_list')
        totalIncome = 0
        row = 0
        while self.query.next():
            self.ui.tbBillList.setRowCount(row + 1)
            self.ui.tbBillList.setItem(row, 0, QTableWidgetItem(self.query.value(0)))
            self.ui.tbBillList.setItem(row, 1, QTableWidgetItem(self.query.value(1)))
            self.ui.tbBillList.setItem(row, 2, QTableWidgetItem(self.query.value(2)))
            self.ui.tbBillList.setItem(row, 3, QTableWidgetItem(mapUserLevel_c2w(self.query.value(3))))
            self.ui.tbBillList.setItem(row, 4, QTableWidgetItem(str(round(self.query.value(4), 2))))
            self.ui.tbBillList.setItem(row, 5, QTableWidgetItem(discountFormat(self.query.value(5))))
            self.ui.tbBillList.setItem(row, 6, QTableWidgetItem(str(round(self.query.value(6), 2))))
            totalIncome += self.query.value(6)
            row += 1
        self.ui.tbBillList.setSortingEnabled(True)
        self.ui.label_totalIncome.setText(str(round(totalIncome, 2)))

    def showBill(self, row):
        orderId = self.ui.tbBillList.item(row, 1).text()
        self.bill = Bill(self.db, orderId)
        self.bill.show()
