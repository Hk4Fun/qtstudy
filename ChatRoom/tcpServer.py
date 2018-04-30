__author__ = 'Hk4Fun'
__date__ = '2018/4/30 15:22'

import sys

from PyQt5.QtWidgets import (QWidget, QListWidget, QLineEdit, QPushButton, QLabel,
                             QGridLayout, QApplication, QMessageBox)
from PyQt5.QtNetwork import (QHostAddress, QTcpServer)


class TcpServer(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = 8888
        self.serverIP = QHostAddress('127.0.0.1')
        self.tcpClientSocketList = []
        self.initUI()

    def initUI(self):
        # 设置窗体的标题
        self.setWindowTitle('TCP Server')
        self.resize(400, 500)

        self.contentListWidget = QListWidget()
        self.serverIPLabel = QLabel('Server IP：')
        self.serverIPLineEdit = QLineEdit()
        self.portLabel = QLabel('Port：')
        self.portLineEdit = QLineEdit()
        self.openBtn = QPushButton('Open Chat Room')

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.contentListWidget, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.portLabel, 1, 0)
        self.mainLayout.addWidget(self.portLineEdit, 1, 1)
        self.mainLayout.addWidget(self.serverIPLabel, 2, 0)
        self.mainLayout.addWidget(self.serverIPLineEdit, 2, 1)
        self.mainLayout.addWidget(self.openBtn, 3, 0, 1, 2)

        self.portLineEdit.setText(str(self.port))
        self.serverIPLineEdit.setText(self.serverIP.toString())

        self.openBtn.clicked.connect(self.slotOpenOrClose)

        self.show()

    def validate(self):
        if not self.serverIP.setAddress(self.serverIPLineEdit.text()):  # 判断给定的IP是否能够被正确解析
            QMessageBox().information(self, 'ERROR', 'Server IP Error!')
            return False

        if not (0 <= int(self.portLineEdit.text()) <= 65535):
            QMessageBox().information(self, 'ERROR', 'Server Port Error!')
            return False
        self.port = int(self.portLineEdit.text())
        return True

    def slotOpenOrClose(self):
        if not self.isUp:
            if not self.validate(): return
            self.openRoom()
        else:
            self.closeRoom()

    def openRoom(self):
        self.openBtn.setText('Close Chat Room')
        self.isUp = True
        self.serverIPLineEdit.setEnabled(False)
        self.portLineEdit.setEnabled(False)

        self.tcpServer = QTcpServer()
        self.tcpServer.listen(self.serverIP, self.port)
        msg = '[*] Server is listening on {}:{} ........'.format(self.serverIP.toString(), self.port)
        self.contentListWidget.addItem(msg)
        self.tcpServer.newConnection.connect(self.addClient2List)

    def closeRoom(self):
        del (self.tcpServer)
        self.tcpClientSocketList = []
        self.isUp = False
        self.serverIPLineEdit.setEnabled(True)
        self.portLineEdit.setEnabled(True)
        self.openBtn.setText('Open Chat Room')
        msg = '[*] Chat Room is closed........'
        self.contentListWidget.addItem(msg)

    def addClient2List(self):
        tcpClientSocket = self.tcpServer.nextPendingConnection()
        self.tcpClientSocketList.append(tcpClientSocket)
        tcpClientSocket.readyRead.connect(self.slotDataReceived)
        tcpClientSocket.disconnected.connect(self.slotDisconnected)

    def slotDataReceived(self):
        tcpClientSocket = self.sender()
        recvData = ''
        while tcpClientSocket.bytesAvailable() > 0:
            recvData += str(tcpClientSocket.read(tcpClientSocket.bytesAvailable()), encoding='utf-8')
        self.contentListWidget.addItem(recvData)
        self.contentListWidget.scrollToBottom()
        # 实现信息的广播, tcpClientSocketList中保存了所有与服务器相连的TcpClientSocket对象
        for client in self.tcpClientSocketList:
            client.write(bytes(recvData, encoding='utf-8'))

    def slotDisconnected(self):
        # 从tcpClientSocketList列表中将断开连接的TcpClientSocket对象删除
        tcpClientSocket = self.sender()
        idx = self.tcpClientSocketList.index(tcpClientSocket)
        del (self.tcpClientSocketList[idx])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = TcpServer()
    app.exit(app.exec_())
