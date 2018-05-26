__author__ = 'Hk4Fun'
__date__ = '2018/5/22 23:03'
import sys

from PyQt5.QtWidgets import (QWidget, QHeaderView, QTableWidgetItem, QInputDialog)

sys.path.append('..')
from AirConditioningV2.ui import ui_Reporter
from AirConditioningV2.ui import ui_Bill
from AirConditioningV2.database import *
from AirConditioningV2.logger import *
from AirConditioningV2.filters import *


class DetailList():
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db
        self.query = db.query
        self.showDetailList()

    def showDetailList(self):
        self.ui.tbDetail.clearContents()
        self.ui.tbDetail.setSortingEnabled(False)  # http://doc.qt.io/qt-5/qtablewidget.html#setItem
        self.db.sqlExec('SELECT * FROM detail_list')
        row = 0
        while self.query.next():
            self.ui.tbDetail.setRowCount(row + 1)
            self.ui.tbDetail.setItem(row, 0, QTableWidgetItem(self.query.value(0)))
            self.ui.tbDetail.setItem(row, 1, QTableWidgetItem(mapUserLevel_c2w(self.query.value(3))))
            self.ui.tbDetail.setItem(row, 2, QTableWidgetItem(timeFormat(self.query.value(1))))
            self.ui.tbDetail.setItem(row, 3, QTableWidgetItem(timeFormat(self.query.value(2))))
            self.ui.tbDetail.setItem(row, 4, QTableWidgetItem(durationFormat(self.query.value(1), self.query.value(2))))
            self.ui.tbDetail.setItem(row, 5, QTableWidgetItem(str(self.query.value(4))))
            self.ui.tbDetail.setItem(row, 6, QTableWidgetItem(str(self.query.value(5))))
            self.ui.tbDetail.setItem(row, 7, QTableWidgetItem(str(self.query.value(6))))
            self.ui.tbDetail.setItem(row, 8, QTableWidgetItem(str(self.query.value(7))))
            self.ui.tbDetail.setItem(row, 9, QTableWidgetItem(str(self.query.value(8))))
            self.ui.tbDetail.setItem(row, 10, QTableWidgetItem(isSettle(self.query.value(9))))
            row += 1
        self.ui.tbDetail.setSortingEnabled(True)

    def saveDetail(self, client):
        sql = 'INSERT INTO detail_list VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, client.roomId)
        self.query.bindValue(1, int(client.openTime))
        self.query.bindValue(2, int(client.closeTime))
        self.query.bindValue(3, client.userLevel)
        self.query.bindValue(4, client.tempAdjust)
        self.query.bindValue(5, client.tempBackCount)
        self.query.bindValue(6, client.speedAdjust)
        self.query.bindValue(7, round(client.energy, 2))
        self.query.bindValue(8, round(client.cost, 2))
        self.query.bindValue(9, '0')  # 单号为0表示还未结算
        self.db.sqlExec()


class BillList():
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db
        self.query = db.query
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

    def addBill(self, orderId, roomId, userLevel, cost):
        sql = 'INSERT INTO bill_list(orderID, roomID, userLevel, cost, discount, receive) VALUES (?, ?, ?, ?, ?, ?)'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, orderId)
        self.query.bindValue(1, roomId)
        self.query.bindValue(2, userLevel)
        self.query.bindValue(3, cost)
        self.query.bindValue(4, mapDiscount(userLevel))
        self.query.bindValue(5, cost * mapDiscount(userLevel))
        self.db.sqlExec()


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


class Reporter(QWidget):
    def __init__(self, db, server):
        super().__init__()
        self.db = db
        self.server = server
        self.query = self.db.query
        self.initUi()

    def initUi(self):
        self.ui = ui_Reporter.Ui_Form()
        self.ui.setupUi(self)
        # resize column both on content and stretch
        header = self.ui.tbDetail.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        header = self.ui.tbBillList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.ui.btRefresh.clicked.connect(self.slotRefTb)
        self.ui.btSettle.clicked.connect(self.slotSettle)
        self.ui.tabWidget.currentChanged.connect(self.slotChangePage)

        self.detailList = DetailList(self.ui, self.db)
        self.billList = BillList(self.ui, self.db)

    def slotRefTb(self):
        self.detailList.showDetailList()
        self.billList.showBillList()

    def slotChangePage(self, idx):
        if idx == 0:
            self.detailList.showDetailList()
        elif idx == 1:
            self.billList.showBillList()

    def slotSettle(self):
        roomId, res = QInputDialog.getText(self, '请输入房间号', '房间号')
        if not res: return
        if not roomId:
            msg = '房间号不能为空'
            QMessageBox().warning(self, '房间号为空', msg, QMessageBox.Yes, QMessageBox.Yes)
            return
        isOpening, client = self.isOpening(roomId)
        if isOpening:
            msg = '当前房间空调尚未关机，是否强制关机？'
            res = QMessageBox().warning(self, '空调尚未关机', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if res == QMessageBox.No: return
            self.disClient(client)
            self.detailList.saveDetail(client)
        if self.hasSettled(roomId):
            msg = '该房间号不存在或已结账！'
            QMessageBox().warning(self, '房间号', msg, QMessageBox.Yes, QMessageBox.Yes)
            return
        self.settleAccount(roomId)

    def hasSettled(self, roomId):
        sql = 'SELECT * FROM detail_list WHERE orderID = "0" AND roomID = ?'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, roomId)
        self.db.sqlExec()
        self.query.next()
        return False if self.query.value(0) else True

    def isOpening(self, roomId):
        for client in self.server.serveQueue + self.server.waitQueue + self.server.tempQueue:
            if client.roomId == roomId:
                return True, client
        return False, None

    def disClient(self, client):
        client.room_temp_timer.stop()
        client.energy_timer.stop()
        client.sock.abort()
        client.closeTime = time.time()

    def getUserLevel(self, roomId):
        sql = 'SELECT userLevel FROM detail_list WHERE roomID = ? AND orderID = "0"'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, roomId)
        self.db.sqlExec()
        self.query.next()
        return self.query.value(0)

    def calcTotalCost(self, roomId):
        sql = 'SELECT SUM(cost) FROM detail_list WHERE roomID = ? AND orderID = "0"'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, roomId)
        self.db.sqlExec()
        self.query.next()
        return self.query.value(0)

    def setOrderId(self, roomId):
        orderId = str(int(time.time()))
        sql = 'UPDATE detail_list SET orderID = ? WHERE roomID = ? AND orderID = "0"'
        self.db.sqlPrepare(sql)
        self.query.bindValue(0, orderId)
        self.query.bindValue(1, roomId)
        self.db.sqlExec()
        return orderId

    def settleAccount(self, roomId):
        userLevel = self.getUserLevel(roomId)
        cost = self.calcTotalCost(roomId)
        # start a transaction
        if self.db.dbh.transaction():
            orderId = self.setOrderId(roomId)
            self.billList.addBill(orderId, roomId, userLevel, cost)
            if not self.db.dbh.commit():
                logger.error(self.db.dbh.lastError().text())
                if not self.db.dbh.rollback():
                    logger.error(self.db.dbh.lastError().text())
                msg = '结账过程出错！'
                QMessageBox().critical(self, '结账失败', msg, QMessageBox.Yes, QMessageBox.Yes)
                return
            self.bill = Bill(self.db, orderId)
            self.bill.show()
