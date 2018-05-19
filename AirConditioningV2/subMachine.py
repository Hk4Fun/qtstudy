__author__ = 'Hk4Fun'
__date__ = '2018/5/14 17:22'

import sys

from PyQt5.QtWidgets import (QWidget, QApplication)
from PyQt5.QtNetwork import (QHostAddress, QTcpSocket)
from PyQt5.QtCore import QTimer

sys.path.append('..')
from AirConditioningV2.protocols import *
from AirConditioningV2.utils import *
from AirConditioningV2.ui import ui_SubMachine


class SubMachine(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = DEFAULT_PORT
        self.serverIP = QHostAddress(DEFAULT_ADDR)
        self.userLevel = DEFAULT_USER_LEVEL
        self.roomTemp = DEFAULT_ROOM_TEMP
        self.setTemp = DEFAULT_SET_TEMP
        self.windSpeed = DEFAULT_WIND_SPEED
        self.mode = DEFAULT_MODE
        self.tempBackTimer = QTimer()
        self.countDown = TEMP_BACK_RANGE
        self.initUi()

    def initUi(self):
        self.ui = ui_SubMachine.Ui_Form()
        self.ui.setupUi(self)
        self.tempBackTimer.timeout.connect(self.tempBack)
        self.ui.cb_userLevel.currentIndexChanged.connect(self.slotSelectUserLevel)
        self.ui.btClose.clicked.connect(self.slotOpenOrClose)
        self.ui.btWindSpeedUp.clicked.connect(self.slotWindSpeedUp)
        self.ui.btWindSpeedDown.clicked.connect(self.slotWindSpeedDown)
        self.ui.btSetTempUp.clicked.connect(self.slotSetTempUp)
        self.ui.btSetTempDown.clicked.connect(self.slotSetTempDown)
        self.show()

    def slotSelectUserLevel(self):
        if self.ui.cb_userLevel.currentText() == 'VIP':
            self.userLevel = USER_VIP
        elif self.ui.cb_userLevel.currentText() == '普通用户':
            self.userLevel = USER_NORMAL

    def slotOpenOrClose(self):
        if self.isUp:
            self.closeMachine()
        else:
            self.openMachine()

    def closeMachine(self):
        self.sock.disconnectFromHost()

    def openMachine(self):
        self.roomId = self.ui.leRoomId.text()
        if self.roomId == '':
            msg = '请先填写房间号！'
            QMessageBox().warning(self, '房间号为空', msg, QMessageBox.Yes, QMessageBox.Yes)
            return
        self.sock = QTcpSocket(self)
        self.protocol = Protocol(self.sock, self)
        self.sock.connectToHost(self.serverIP, self.port)

        self.sock.connected.connect(self.protocol.sendOpen)
        self.sock.readyRead.connect(self.protocol.recvPacket)
        self.sock.disconnected.connect(self.slotDisconnected)
        self.sock.error.connect(self.slotErrorOccured)

    def slotWindSpeedUp(self):
        if self.windSpeed != HIGH_WIND:
            self.ui.btWindSpeedUp.setEnabled(False)
            self.ui.btWindSpeedDown.setEnabled(False)
            self.windSpeed += 1
            self.protocol.sendSpeed(self.windSpeed)

    def slotWindSpeedDown(self):
        if self.windSpeed != LOW_WIND:
            self.ui.btWindSpeedUp.setEnabled(False)
            self.ui.btWindSpeedDown.setEnabled(False)
            self.windSpeed -= 1
            self.protocol.sendSpeed(self.windSpeed)

    def slotSetTempUp(self):
        if self.setTemp != MAX_TEMP:
            self.ui.btSetTempUp.setEnabled(False)
            self.ui.btSetTempDown.setEnabled(False)
            self.setTemp += 1
            self.protocol.sendTemp(self.setTemp)

    def slotSetTempDown(self):
        if self.setTemp != MIN_TEMP:
            self.ui.btSetTempUp.setEnabled(False)
            self.ui.btSetTempDown.setEnabled(False)
            self.setTemp -= 1
            self.protocol.sendTemp(self.setTemp)

    def recvOpenACK(self, res):
        if res:
            self.isUp = True
            self.ui.btWindSpeedDown.setEnabled(True)
            self.ui.btWindSpeedUp.setEnabled(True)
            self.ui.btSetTempDown.setEnabled(True)
            self.ui.btSetTempUp.setEnabled(True)
            self.ui.leRoomId.setEnabled(False)
            self.ui.cb_userLevel.setEnabled(False)
            self.ui.btClose.setText('关机')
        else:
            msg = '该房间已入住，请更换其他房间号！'
            QMessageBox().warning(self, '开机失败', msg, QMessageBox.Yes, QMessageBox.Yes)

    def recvSpeedACK(self, res):
        if res:
            self.ui.label_windSpeed.setText(mapWindSpeed_c2w(self.windSpeed))
        else:
            self.windSpeed = mapWindSpeed_w2c(self.ui.label_windSpeed.text())
            self.protocol.serveQueueFull()
        self.ui.btWindSpeedDown.setEnabled(True)
        self.ui.btWindSpeedUp.setEnabled(True)

    def recvTempACK(self, res):
        if res:
            self.ui.lcd_setTemp.display(self.setTemp)
        else:
            self.setTemp = self.ui.lcd_setTemp.intValue()
            self.protocol.serveQueueFull()
        self.ui.btSetTempDown.setEnabled(True)
        self.ui.btSetTempUp.setEnabled(True)

    def recvState(self, state):
        if state['roomId'] != self.roomId:
            self.protocol.protocolError()
        else:
            self.roomTemp = state['roomTemp']  # 房间温度由主控通知
            self.mode = state['mode']
            self.setTemp = state['setTemp']
            self.windSpeed = state['windSpeed']
            self.ui.label_windSpeed.setText(mapWindSpeed_c2w(self.windSpeed))
            self.ui.lcd_setTemp.display(self.setTemp)
            self.ui.label_roomTemp.setText(str(state['roomTemp']))
            self.ui.label_mode.setText(mapMode_c2w(state['mode']))  # 模式由主控决定
            self.ui.label_energy.setText(str(state['energy']))  # 耗能由主控统计
            self.ui.label_money.setText(str(state['cost']))  # 计费由主控计算

    def recvHalt(self, roomId):
        if roomId != self.roomId:
            self.protocol.protocolError()
        else:  # 触发回温机制
            # 回温时关闭按钮的响应
            self.ui.btWindSpeedDown.setEnabled(False)
            self.ui.btWindSpeedUp.setEnabled(False)
            self.ui.btSetTempDown.setEnabled(False)
            self.ui.btSetTempUp.setEnabled(False)
            self.tempBackTimer.start(TEMP_BACK_TIMER)

    def tempBack(self):
        if self.countDown:
            self.countDown -= 1  # 回温次数-1
            if self.mode == COLD_MODE:  # 室外温度高
                self.roomTemp += 1
            elif self.mode == WARM_MODE:  # 室外温度低
                self.roomTemp -= 1
            self.ui.label_roomTemp.setText(str(self.roomTemp))
        else:  # 回温结束，重新申请服务
            # 开启按钮的响应
            self.ui.btWindSpeedDown.setEnabled(True)
            self.ui.btWindSpeedUp.setEnabled(True)
            self.ui.btSetTempDown.setEnabled(True)
            self.ui.btSetTempUp.setEnabled(True)

            self.tempBackTimer.stop()
            self.countDown = TEMP_BACK_RANGE
            self.protocol.sendTempBack()

    def slotDisconnected(self):
        self.isUp = False
        self.ui.btWindSpeedDown.setEnabled(False)
        self.ui.btWindSpeedUp.setEnabled(False)
        self.ui.btSetTempDown.setEnabled(False)
        self.ui.btSetTempUp.setEnabled(False)
        self.ui.leRoomId.setEnabled(True)
        self.ui.cb_userLevel.setEnabled(True)
        self.ui.btClose.setText('开机')

    def slotErrorOccured(self, socketError):
        if socketError == 0:
            msg = '请确保中控机开启！'
            QMessageBox().warning(self, '连接异常', msg, QMessageBox.Yes, QMessageBox.Yes)
        elif socketError == 1:
            msg = '与中控机断开连接！'
            QMessageBox().critical(self, '连接异常', msg, QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sub_machine = SubMachine()
    app.exit(app.exec_())
