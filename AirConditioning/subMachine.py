__author__ = 'Hk4Fun'
__date__ = '2018/5/14 17:22'

import sys
import random

from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox)
from PyQt5.QtNetwork import (QHostAddress, QTcpSocket)
from PyQt5.QtCore import (QTimer, QJsonDocument)

sys.path.append('..')
from utils import *
from AirConditioning.ui import ui_SubMachine


class SubMachine(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = DEFAULT_PORT
        self.serverIP = QHostAddress(DEFAULT_ADDR)
        self.mode = DEFAULT_MODE
        self.roomTemp = DEFAULT_ROOM_TEMP
        self.setTemp = DEFAULT_SET_TEMP
        self.windSpeed = DEFAULT_WIND_SPEED
        self.energy = 0
        self.money = 0
        self.room_temp_timer = QTimer()
        self.energy_timer = QTimer()
        self.initUi()

    def initUi(self):
        self.ui = ui_SubMachine.Ui_Form()
        self.ui.setupUi(self)
        self.room_temp_timer.timeout.connect(self.slotUpdateRoomTemp)
        self.energy_timer.timeout.connect(self.slotUpdateEnergyMoney)
        self.ui.btClose.clicked.connect(self.slotOpenOrClose)
        self.ui.btCold.clicked.connect(self.slotColdMode)
        self.ui.btWarm.clicked.connect(self.slotWarmMode)
        self.ui.btWindSpeedUp.clicked.connect(self.slotWindSpeedUp)
        self.ui.btWindSpeedDown.clicked.connect(self.slotWindSpeedDown)
        self.ui.btSetTempUp.clicked.connect(self.slotSetTempUp)
        self.ui.btSetTempDown.clicked.connect(self.slotSetTempDown)
        self.show()

    def slotUpdateRoomTemp(self):
        if self.roomTemp != self.setTemp:
            if self.roomTemp < self.setTemp:
                self.roomTemp += ROOM_TEMP_INC
            elif self.roomTemp > self.setTemp:
                self.roomTemp -= ROOM_TEMP_INC
        else:  # 根据设定温度和模式上下浮动
            if self.mode == COLD_MODE:  # 室外温度高
                self.roomTemp += random.choice([0, 1, 2])
            elif self.mode == WARM_MODE:  # 室外温度低
                self.roomTemp -= random.choice([0, 1, 2])
        self.ui.label_roomTemp.setText(str(self.roomTemp))

    def slotUpdateEnergyMoney(self):
        self.energy += ENERGY_INC * self.windSpeed
        self.money += MONEY_INC * self.windSpeed
        self.ui.label_energy.setText(str(round(self.energy, 2)))
        self.ui.label_money.setText(str(round(self.money, 2)))

    def slotColdMode(self):
        self.mode = COLD_MODE
        # send something

    def slotWarmMode(self):
        self.mode = WARM_MODE
        # send something

    def slotWindSpeedUp(self):
        if self.windSpeed != HIGH_WIND:
            self.windSpeed += 1
            self.ui.label_windSpeed.setText(mapWindSpeed(self.windSpeed))
            # send something

    def slotWindSpeedDown(self):
        if self.windSpeed != LOW_WIND:
            self.windSpeed -= 1
            self.ui.label_windSpeed.setText(mapWindSpeed(self.windSpeed))
            # send something

    def slotSetTempUp(self):
        if self.setTemp != MAX_TEMP:
            self.setTemp += 1
            self.ui.lcd_setTemp.display(self.setTemp)
            # send something

    def slotSetTempDown(self):
        if self.setTemp != MIN_TEMP:
            self.setTemp -= 1
            self.ui.lcd_setTemp.display(self.setTemp)
            # send something

    def slotOpenOrClose(self):
        if self.isUp:
            self.closeMachine()
        else:
            self.openMachine()

    def closeMachine(self):
        # send something
        self.sock.disconnectFromHost()

    def openMachine(self):
        self.roomId = self.ui.leRoomId.text()
        if self.roomId == '':
            msg = '请先填写房间号！'
            QMessageBox().warning(self, '房间号为空', msg, QMessageBox.Yes, QMessageBox.Yes)
            return
        self.sock = QTcpSocket(self)
        self.sock.connectToHost(self.serverIP, self.port)

        self.sock.connected.connect(self.slotConnected)
        self.sock.readyRead.connect(self.slotDataReceived)
        self.sock.disconnected.connect(self.slotDisconnected)
        self.sock.error.connect(self.slotErrorOccured)

    def slotConnected(self):
        self.ui.btCold.setEnabled(True)
        self.ui.btWarm.setEnabled(True)
        self.ui.btWindSpeedDown.setEnabled(True)
        self.ui.btWindSpeedUp.setEnabled(True)
        self.ui.btSetTempDown.setEnabled(True)
        self.ui.btSetTempUp.setEnabled(True)
        self.ui.btClose.setText('关机')
        self.isUp = True
        self.room_temp_timer.start(ROOM_TEMP_TIMER)
        self.energy_timer.start(ENERGY_TIMER)
        # send something

    def slotDataReceived(self):
        recvData = b''
        while self.sock.bytesAvailable() > 0:
            recvData += self.sock.read(self.sock.bytesAvailable())
        recvData = QJsonDocument().fromJson(recvData)
        self.parseData(recvData)

    def parseData(self, recvData):
        if recvData['type'] == TYPE_REQUEST_STATUS:
            self.sendStatus()

    def sendStatus(self):
        sendData = {'type': TYPE_RESPONSE_STATUS,
                    'roomId': self.roomId,
                    'mode': self.mode,
                    'roomTemp': self.roomTemp,
                    'setTemp': self.setTemp,
                    'windSpeed': self.windSpeed,
                    'energy': self.energy,
                    'money': self.money}
        sendData = QJsonDocument(sendData).toJson()
        self.sock.write(sendData)

    def slotDisconnected(self):
        self.ui.btCold.setEnabled(False)
        self.ui.btWarm.setEnabled(False)
        self.ui.btWindSpeedDown.setEnabled(False)
        self.ui.btWindSpeedUp.setEnabled(False)
        self.ui.btSetTempDown.setEnabled(False)
        self.ui.btSetTempUp.setEnabled(False)
        self.ui.btClose.setText('开机')
        self.room_temp_timer.stop()
        self.energy_timer.stop()
        self.isUp = False

    def slotErrorOccured(self, socketError):
        if socketError == 0:
            msg = '请确保中控机开启！'
            QMessageBox().warning(self, '连接异常', msg, QMessageBox.Yes, QMessageBox.Yes)
        elif socketError == 1:
            self.room_temp_timer.stop()
            self.energy_timer.stop()
            msg = '与中控机断开连接！'
            QMessageBox().critical(self, '连接异常', msg, QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sub_machine = SubMachine()
    app.exit(app.exec_())
