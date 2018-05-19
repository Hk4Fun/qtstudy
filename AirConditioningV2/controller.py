__author__ = 'Hk4Fun'
__date__ = '2018/5/15 0:13'

import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QHeaderView, QTableWidgetItem)
from PyQt5.QtNetwork import (QHostAddress, QTcpServer)
from PyQt5.QtCore import QTimer

sys.path.append('..')
from AirConditioningV2.protocols import *
from AirConditioningV2.utils import *
from AirConditioningV2.ui import ui_Controller


class ConnectClient():
    def __init__(self, sock, server):
        self.sock = sock
        self.protocol = Protocol(sock, self, True)
        self.server = server
        self.roomId = None
        self.userLevel = None
        self.mode = DEFAULT_MODE
        self.roomTemp = DEFAULT_ROOM_TEMP
        self.setTemp = DEFAULT_SET_TEMP
        self.windSpeed = DEFAULT_WIND_SPEED
        self.energy = 0
        self.money = 0
        self.room_temp_timer = QTimer()
        self.energy_timer = QTimer()
        self.room_temp_timer.timeout.connect(self.slotChangeRoomTemp)
        self.energy_timer.timeout.connect(self.slotChangeEnergyMoney)

    def hasRegistered(self, roomId):
        for client in self.server.serveQueue + self.server.waitQueue + self.server.tempQueue:
            if client.roomId == roomId:
                return True
        return False

    def startServe(self, client):
        client.room_temp_timer.start(ROOM_TEMP_TIMER)
        client.energy_timer.start(ENERGY_TIMER)

    def stopServe(self, client):
        client.room_temp_timer.stop()
        client.energy_timer.stop()
        client.protocol.sendHalt()

    def add2ServeOrWait(self):
        if len(self.server.serveQueue) < MAX_SERVE_LEN:
            self.server.serveQueue.append(self)
            self.startServe(self)
        elif self.userLevel == USER_NORMAL:  # 普通用户在服务队列满时只能放进等待队列
            self.server.waitQueue.append(self)
        else:  # VIP用户可以直接进入服务队列队尾享受服务，而队首被顶掉放入回温队列
            head = self.server.serveQueue.pop(0)
            self.stopServe(head)
            self.server.tempQueue.append(head)
            self.server.serveQueue.append(self)
            self.startServe(self)

    def recvOpen(self, data):
        if self.hasRegistered(data['roomId']):
            self.protocol.sendOpenACK(int(False))
        else:  # 加入等待队列或服务队列
            self.protocol.sendOpenACK(int(True))
            self.roomId = data['roomId']
            self.userLevel = data['userLevel']
            self.add2ServeOrWait()

    def recvSpeed(self, data):
        if data['roomId'] != self.roomId and data['userLevel'] != self.userLevel:
            self.protocol.protocolError()
        elif self in self.server.serveQueue:
            self.protocol.sendSpeedACK(int(True))
            self.windSpeed = data['windSpeed']
        elif self in self.server.waitQueue:
            self.protocol.sendSpeedACK(int(False))
        else:
            self.protocol.protocolError()

    def recvTemp(self, data):
        if data['roomId'] != self.roomId and data['userLevel'] != self.userLevel:
            self.protocol.protocolError()
        elif self in self.server.serveQueue:
            self.protocol.sendTempACK(int(True))
            self.setTemp = data['setTemp']
        elif self in self.server.waitQueue:
            self.protocol.sendTempACK(int(False))
        else:
            self.protocol.protocolError()

    def recvTemBack(self, roomTemp):
        if self in self.server.tempQueue:  # 检查一下自己是否在回温队列中
            self.roomTemp = roomTemp
            self.server.tempQueue.remove(self)
            self.add2ServeOrWait()
        else:
            self.protocol.protocolError()

    def slotChangeRoomTemp(self):
        if self.roomTemp != self.setTemp:
            if self.roomTemp < self.setTemp:
                self.roomTemp += 1
            elif self.roomTemp > self.setTemp:
                self.roomTemp -= 1
        else:  # 服务结束放入回温队列
            self.stopServe(self)
            self.server.serveQueue.remove(self)
            self.server.tempQueue.append(self)
            if self.server.waitQueue:  # 如果此时等待队列不为空，则把等待队列队首加入服务队列队尾
                head = self.server.waitQueue.pop(0)
                self.server.serveQueue.append(head)
                self.startServe(head)

    def slotChangeEnergyMoney(self):
        self.energy += ENERGY_INC * self.windSpeed
        self.money += MONEY_INC * self.windSpeed


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = DEFAULT_PORT
        self.serverIP = QHostAddress(DEFAULT_ADDR)
        self.serveQueue, self.waitQueue, self.tempQueue = [], [], []  # # mutex ??? find usage
        self.sendStateTimer = QTimer()
        self.refTableTimer = QTimer()
        self.sendInterval = SEND_STATE_TIMER
        self.refInterval = TABLE_REF_TIMER
        self.initUi()

    def initUi(self):
        self.ui = ui_Controller.Ui_Form()
        self.ui.setupUi(self)
        # 使行列头自适应宽度，所有列平均分来填充空白部分
        self.ui.tbServeQueue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tbWaitQueue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tbTempQueue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.spRefFre.valueChanged.connect(self.slotSetRefFre)
        self.ui.spSendFre.valueChanged.connect(self.slotSetSendFre)
        self.ui.btClose.clicked.connect(self.slotOpenOrClose)
        self.ui.btWarm.clicked.connect(self.slotWarmMode)
        self.ui.btCold.clicked.connect(self.slotColdMode)
        self.ui.btReport.clicked.connect(self.slotShowReport)
        self.sendStateTimer.timeout.connect(self.slotSendState)
        self.refTableTimer.timeout.connect(self.slotRefTable)
        self.show()

    def slotWarmMode(self):
        for client in self.serveQueue:
            client.mode = WARM_MODE

    def slotColdMode(self):
        for client in self.serveQueue:
            client.mode = COLD_MODE

    def slotSetRefFre(self, interval):
        self.refInterval = int(interval * 1000)
        self.refTableTimer.setInterval(self.refInterval)

    def slotSetSendFre(self, interval):
        self.sendInterval = int(interval * 1000)
        self.sendStateTimer.setInterval(self.sendInterval)

    def slotSendState(self):
        for client in self.serveQueue:
            client.protocol.sendState()

    def add2table(self, queue, table):
        for row, client in enumerate(queue):
            table.setRowCount(row + 1)
            table.setItem(row, 0, QTableWidgetItem(client.roomId))
            table.setItem(row, 1, QTableWidgetItem(mapUserLevel_c2w(client.userLevel)))
            table.setItem(row, 2, QTableWidgetItem(mapMode_c2w(client.mode)))
            table.setItem(row, 3, QTableWidgetItem(str(client.roomTemp)))
            table.setItem(row, 4, QTableWidgetItem(str(client.setTemp)))
            table.setItem(row, 5, QTableWidgetItem(mapWindSpeed_c2w(client.windSpeed)))
            table.setItem(row, 6, QTableWidgetItem(str(round(client.energy, 2))))
            table.setItem(row, 7, QTableWidgetItem(str(round(client.money, 2))))

    def slotRefTable(self):
        self.ui.tbServeQueue.clearContents()
        self.ui.tbWaitQueue.clearContents()
        self.ui.tbTempQueue.clearContents()
        self.add2table(self.serveQueue, self.ui.tbServeQueue)
        self.add2table(self.waitQueue, self.ui.tbWaitQueue)
        self.add2table(self.tempQueue, self.ui.tbTempQueue)

    def slotOpenOrClose(self):
        if self.isUp:
            self.closeMachine()
        else:
            self.openMachine()

    def openMachine(self):
        self.isUp = True
        self.ui.btCold.setEnabled(True)
        self.ui.btWarm.setEnabled(True)
        self.ui.spRefFre.setEnabled(True)
        self.ui.spSendFre.setEnabled(True)
        self.ui.btClose.setText('关机')
        self.server = QTcpServer()
        self.server.listen(self.serverIP, self.port)
        self.server.newConnection.connect(self.addClient2Queue)
        self.sendStateTimer.start(self.sendInterval)
        self.refTableTimer.start(self.refInterval)

    def closeMachine(self):
        for client in self.serveQueue + self.waitQueue + self.tempQueue:
            client.room_temp_timer.stop()
            client.energy_timer.stop()
            client.sock.abort()
        self.serveQueue, self.waitQueue, self.tempQueue = [], [], []
        del self.server
        self.isUp = False
        self.ui.btClose.setText('开机')
        self.ui.btCold.setEnabled(False)
        self.ui.btWarm.setEnabled(False)
        self.ui.spRefFre.setEnabled(False)
        self.ui.spSendFre.setEnabled(False)
        self.ui.tbServeQueue.clearContents()  # 不能直接调用clear()，否则head一起清空
        self.ui.tbServeQueue.setRowCount(0)
        self.ui.tbWaitQueue.clearContents()
        self.ui.tbWaitQueue.setRowCount(0)
        self.ui.tbTempQueue.clearContents()
        self.ui.tbTempQueue.setRowCount(0)
        self.sendStateTimer.stop()
        self.refTableTimer.stop()

    def addClient2Queue(self):
        client_sock = self.server.nextPendingConnection()
        client = ConnectClient(client_sock, self)
        client_sock.readyRead.connect(client.protocol.recvPacket)
        client_sock.disconnected.connect(self.slotDisconnected)

    def slotDisconnected(self):
        client_sock = self.sender()
        idx, queue = self.findClient(client_sock)
        if idx >= 0:
            queue[idx].room_temp_timer.stop()
            queue[idx].energy_timer.stop()
            del (queue[idx])

    def findClient(self, sock):
        for idx, client in enumerate(self.serveQueue):
            if client.sock is sock:
                return idx, self.serveQueue
        for idx, client in enumerate(self.waitQueue):
            if client.sock is sock:
                return idx, self.waitQueue
        for idx, client in enumerate(self.tempQueue):
            if client.sock is sock:
                return idx, self.tempQueue
        return -1, None

    def slotShowReport(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    app.exit(app.exec_())
