__author__ = 'Hk4Fun'
__date__ = '2018/5/15 0:13'

import sys

from PyQt5.QtWidgets import (QApplication, QMessageBox, QWidget, QHeaderView,
                             QTableWidgetItem)
from PyQt5.QtNetwork import (QHostAddress, QTcpServer)
from PyQt5.QtCore import QTimer

sys.path.append('..')
from AirConditioningV2.protocols import *
from AirConditioningV2.utils import *
from AirConditioningV2.ui import ui_Controller


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    app.exit(app.exec_())
