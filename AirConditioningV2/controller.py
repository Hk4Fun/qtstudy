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
        self.isUp = False
        self.port = DEFAULT_PORT
        self.serverIP = QHostAddress(DEFAULT_ADDR)
        self.serveQueue, self.waitQueue, self.tempQueue = [], [], []

        self.initUi()

    def initUi(self):
        self.ui = ui_Controller.Ui_Form()
        self.ui.setupUi(self)
        # 使行列头自适应宽度，所有列平均分来填充空白部分
        self.ui.tableSubMachine.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.spinRefresh.valueChanged.connect(self.slotSetRef)
        self.ui.btClose.clicked.connect(self.slotOpenOrClose)
        self.ui.btReport.clicked.connect(self.slotShowReport)
        self.show()

    def slotSetRef(self):
        pass

    def slotOpenOrClose(self):
        pass

    def slotShowReport(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    app.exit(app.exec_())
