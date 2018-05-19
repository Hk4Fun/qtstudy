__author__ = 'Hk4Fun'
__date__ = '2018/5/18 15:57'

from AirConditioningV2.settings import *
from PyQt5.QtWidgets import QMessageBox


class Protocol:
    def __init__(self, sock, ac, isClient=False):
        self.sock = sock
        self.ac = ac
        self.isClient = isClient

    def sendPacket(self, packet):
        sendData = '|'.join(map(str, packet))
        self.sock.write(sendData.encode())

    def recvPacket(self):
        recvData = ''
        while self.sock.bytesAvailable() > 0:
            recvData += self.sock.read(self.sock.bytesAvailable()).decode()
        self.dataParse(recvData.split('|'))

    def dataParse(self, data):
        code = int(data[0])
        if code == OPEN_ACK_CODE:  # OPEN_ACK_CODE|Res
            self.ac.recvOpenACK(int(data[1]))
        elif code == SPEED_ACK_CODE:  # SPEED_ACK_CODE|Res
            self.ac.recvSpeedACK(int(data[1]))
        elif code == TEMP_ACK_CODE:  # TEMP_ACK_CODE|Res
            self.ac.recvTempACK(int(data[1]))
        elif code == STATE_CODE:  # STATE_CODE|Room_id|Mode|Cur_temp|Target_temp|Speed|Energy|Cost
            state = {
                'roomId': data[1],
                'mode': int(data[2]),
                'roomTemp': int(data[3]),
                'setTemp': int(data[4]),
                'windSpeed': int(data[5]),
                'energy': round(float(data[6]), 2),
                'cost': round(float(data[7]), 2)
            }
            self.ac.recvState(state)
        elif code == HALT_CODE:  # HALT_CODE|Room_id
            self.ac.recvHalt(data[1])
        elif code == OPEN_CODE:  # OPEN_CODE|Room_id|userLevel
            data = {
                'roomId': data[1],
                'userLevel': int(data[2])
            }
            self.ac.recvOpen(data)
        elif code == SPEED_CODE:  # SPEED_CODE|Room_id|userLevel|Speed_type
            data = {
                'roomId': data[1],
                'userLevel': int(data[2]),
                'windSpeed': int(data[3])
            }
            self.ac.recvSpeed(data)
        elif code == TEMP_CODE:  # TEMP_CODE|Room_id|userLevel|Temp_value
            data = {
                'roomId': data[1],
                'userLevel': int(data[2]),
                'setTemp': int(data[3])
            }
            self.ac.recvTemp(data)
        elif code == TEMP_BACK_CODE:  # TEMP_BACK_CODE|roomTemp
            self.ac.recvTemBack(int(data[1]))
        else:
            self.protocolError()

    def sendOpen(self):
        # OPEN_CODE|Room_id|userLevel
        self.sendPacket([OPEN_CODE, self.ac.roomId, self.ac.userLevel])

    def sendSpeed(self, type):
        # SPEED_CODE|Room_id|userLevel|Speed_type
        self.sendPacket([SPEED_CODE, self.ac.roomId, self.ac.userLevel, type])

    def sendTemp(self, value):
        # TEMP_CODE|Room_id|userLevel|Temp_value
        self.sendPacket([TEMP_CODE, self.ac.roomId, self.ac.userLevel, value])

    def sendTempBack(self):
        # TEMP_BACK_CODE|roomTemp
        self.sendPacket([TEMP_BACK_CODE, self.ac.roomTemp])

    def sendState(self):
        # STATE_CODE|Room_id|Mode|Cur_temp|Target_temp|Speed|Energy|Cost
        self.sendPacket([STATE_CODE, self.ac.roomId, self.ac.mode,
                         self.ac.roomTemp, self.ac.setTemp, self.ac.windSpeed,
                         self.ac.energy, self.ac.money])

    def sendOpenACK(self, res):
        self.sendPacket([OPEN_ACK_CODE, res])

    def sendSpeedACK(self, res):
        self.sendPacket([SPEED_ACK_CODE, res])

    def sendTempACK(self, res):
        self.sendPacket([TEMP_ACK_CODE, res])

    def sendHalt(self):
        self.sendPacket([HALT_CODE, self.ac.roomId])

    def protocolError(self):
        msg = '协议发生严重性错误！'
        if self.isClient:
            QMessageBox().critical(self.ac.server, '协议出错', msg, QMessageBox.Yes, QMessageBox.Yes)
            self.ac.server.closeMachine()
        else:
            QMessageBox().critical(self.ac, '协议出错', msg, QMessageBox.Yes, QMessageBox.Yes)
            self.ac.closeMachine()

    def serveQueueFull(self):
        msg = '服务队列已满，请耐心等候......'
        QMessageBox().warning(self.ac, '服务队列已满', msg, QMessageBox.Yes, QMessageBox.Yes)
