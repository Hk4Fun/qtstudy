__author__ = 'Hk4Fun'
__date__ = '2018/5/15 0:13'

import sys

from PyQt5.QtWidgets import (QApplication, QMessageBox, QWidget, QHeaderView,
                             QTableWidgetItem)
from PyQt5.QtNetwork import (QHostAddress, QTcpServer)
from PyQt5.QtCore import (QTimer, QJsonDocument)

sys.path.append('..')
from AirConditioning.utils import *
from AirConditioning.ui import ui_Controller


class ConnectClient():
    def __init__(self, sock):
        self.sock = sock
        self.roomId = None
        self.mode = None
        self.roomTemp = None
        self.setTemp = None
        self.windSpeed = None
        self.energy = None
        self.money = None


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = DEFAULT_PORT
        self.serverIP = QHostAddress(DEFAULT_ADDR)
        self.client_list = []
        self.req_sta_inter = REQUEST_STATUS_TIMER
        self.timer = QTimer(self)
        self.initUi()

    def initUi(self):
        self.ui = ui_Controller.Ui_Form()
        self.ui.setupUi(self)
        # 使行列头自适应宽度，所有列平均分来填充空白部分
        self.ui.tableSubMachine.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.timer.timeout.connect(self.slotRequestStatus)
        self.ui.spinRefresh.valueChanged.connect(self.slotSetRef)
        self.ui.btClose.clicked.connect(self.slotOpenOrClose)
        self.ui.btReport.clicked.connect(self.slotShowReport)
        self.show()

    def slotSetRef(self, interval):
        self.req_sta_inter = int(interval * 1000)
        self.timer.setInterval(self.req_sta_inter)

    def slotRequestStatus(self):
        sendData = QJsonDocument({'type': TYPE_REQUEST_STATUS}).toJson()
        for client in self.client_list:
            client.sock.write(sendData)

    def slotOpenOrClose(self):
        if self.isUp:
            self.closeController()
        else:
            self.openController()

    def openController(self):
        self.isUp = True
        self.ui.btClose.setText('关机')
        self.timer.start(self.req_sta_inter)

        self.server = QTcpServer()
        self.server.listen(self.serverIP, self.port)
        self.server.newConnection.connect(self.addClient2List)

    def closeController(self):
        del self.server
        self.isUp = False
        self.ui.btClose.setText('开机')
        self.client_list = []
        self.ui.tableSubMachine.clearContents()  # 不能直接调用clear()，否则head一起清空
        self.ui.tableSubMachine.setRowCount(0)

    def addClient2List(self):
        client_sock = self.server.nextPendingConnection()
        client = ConnectClient(client_sock)
        self.client_list.append(client)
        client_sock.readyRead.connect(self.slotDataReceived)
        client_sock.disconnected.connect(self.slotDisconnected)

    def findClient(self, socket):
        for idx, client in enumerate(self.client_list):
            if client.sock is socket:
                return idx
        return -1

    def parseData(self, client, recvData):
        if recvData['type'].toInt() == TYPE_RESPONSE_STATUS:
            self.addClientStatus(client, recvData)

    def addClientStatus(self, client, recvData):
        client.roomId = recvData['roomId'].toString()
        client.mode = recvData['mode'].toInt()
        client.roomTemp = recvData['roomTemp'].toInt()
        client.setTemp = recvData['setTemp'].toInt()
        client.windSpeed = recvData['windSpeed'].toInt()
        client.energy = recvData['energy'].toDouble()
        client.money = recvData['money'].toDouble()
        self.addClientStatus2table(client)

    def findRow(self, roomId):
        for row in range(self.ui.tableSubMachine.rowCount()):
            if self.ui.tableSubMachine.item(row, 0).text() == roomId:
                return row
        return -1

    def addClientStatus2table(self, client):
        row = self.findRow(client.roomId)
        if row == -1:  # 未找到，新建一行
            row = self.ui.tableSubMachine.rowCount()
            self.ui.tableSubMachine.setRowCount(row + 1)
        self.ui.tableSubMachine.setItem(row, 0, QTableWidgetItem(client.roomId))
        self.ui.tableSubMachine.setItem(row, 1, QTableWidgetItem(mapMode(client.mode)))
        self.ui.tableSubMachine.setItem(row, 2, QTableWidgetItem(str(client.roomTemp)))
        self.ui.tableSubMachine.setItem(row, 3, QTableWidgetItem(str(client.setTemp)))
        self.ui.tableSubMachine.setItem(row, 4, QTableWidgetItem(mapWindSpeed(client.windSpeed)))
        self.ui.tableSubMachine.setItem(row, 5, QTableWidgetItem(str(round(client.energy, 2))))
        self.ui.tableSubMachine.setItem(row, 6, QTableWidgetItem(str(round(client.money, 2))))

    def slotDataReceived(self):
        recvData = b''
        client_sock = self.sender()
        client = self.client_list[self.findClient(client_sock)]
        while client_sock.bytesAvailable() > 0:
            recvData += client_sock.read(client_sock.bytesAvailable())
        recvData = QJsonDocument().fromJson(recvData)
        self.parseData(client, recvData)

    def slotDisconnected(self):
        client_sock = self.sender()
        idx = self.findClient(client_sock)
        if idx >= 0:
            del (self.client_list[idx])

    def slotShowReport(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    app.exit(app.exec_())
