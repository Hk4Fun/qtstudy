__author__ = 'Hk4Fun'
__date__ = '2018/5/18 15:57'

from AirConditioningV2.settings import *
from PyQt5.QtWidgets import QMessageBox

class Protocol:
    def __init__(self, sock, ac):
        self.sock = sock
        self.ac = ac

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
        elif code == SPEED_ACK_CODE:  # SPEED_ACK_CODE|Res|Speed_type
            self.ac.recvSpeedACK(int(data[1]))
        elif code == TEMP_ACK_CODE:  # TEMP_ACK_CODE|Res|Temp_value
            self.ac.recvTempACK(int(data[1]))
        elif code == STATE_CODE:  # STATE_CODE|Room_id|Mode|Cur_temp|Target_temp|Speed|Energy|Cost
            self.ac.recvState(data[1:])
        elif code == HALT_CODE:  # HALT_CODE|Room_id
            self.ac.recvHalt(data[1])
        elif code == CLOSE_ACK_CODE:  # CLOSE_ACK_CODE|Res
            pass

    def sendOpen(self):
        # OPEN_CODE|Room_id|userLevel
        self.sendPacket([OPEN_CODE, self.ac.roomId, self.ac.userLevel])

    def sendSpeed(self, type):
        # SPEED_CODE|Room_id|userLevel|Speed_type
        self.sendPacket([SPEED_CODE, self.ac.roomId, self.ac.userLevel, type])

    def sendTemp(self, value):
        # TEMP_CODE|Room_id|userLevel|Temp_value
        self.sendPacket([SPEED_CODE, self.ac.roomId, self.ac.userLevel, value])

    def protocolError(self):
        msg = '协议发生严重性错误！'
        QMessageBox().critical(self.ac, '协议出错', msg, QMessageBox.Yes, QMessageBox.Yes)
        self.ac.closeMachine()



