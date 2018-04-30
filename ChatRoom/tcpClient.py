__author__ = 'Hk4Fun'
__date__ = '2018/4/30 13:02'

import sys

from PyQt5.QtWidgets import (QWidget, QListWidget, QLineEdit, QPushButton, QLabel,
                             QGridLayout, QApplication, QMessageBox)
from PyQt5.QtNetwork import (QHostAddress, QTcpSocket)


class TcpClient(QWidget):

    def __init__(self):
        super().__init__()
        self.isOnline = False
        self.port = 8888
        self.serverIP = QHostAddress('127.0.0.1')
        self.initUI()

    def initUI(self):
        # 设置窗体的标题
        self.setWindowTitle('TCP Client')
        self.resize(400, 500)

        # 初始化各个控件
        self.contentListWidget = QListWidget()
        self.sendLineEdit = QLineEdit()
        self.sendBtn = QPushButton('Send')
        self.userNameLabel = QLabel('User Name：')
        self.userNameLineEdit = QLineEdit()
        self.serverIPLabel = QLabel('Server IP：')
        self.serverIPLineEdit = QLineEdit()
        self.portLabel = QLabel('Server Port：')
        self.portLineEdit = QLineEdit()
        self.enterBtn = QPushButton('Enter Chat Room')

        # 设置布局
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.contentListWidget, 0, 0, 1, 2)
        mainLayout.addWidget(self.sendLineEdit, 1, 0)
        mainLayout.addWidget(self.sendBtn, 1, 1)
        mainLayout.addWidget(self.userNameLabel, 2, 0)
        mainLayout.addWidget(self.userNameLineEdit, 2, 1)
        mainLayout.addWidget(self.serverIPLabel, 3, 0)
        mainLayout.addWidget(self.serverIPLineEdit, 3, 1)
        mainLayout.addWidget(self.portLabel, 4, 0)
        mainLayout.addWidget(self.portLineEdit, 4, 1)
        mainLayout.addWidget(self.enterBtn, 5, 0, 1, 2)

        self.sendBtn.setEnabled(False)
        self.portLineEdit.setText(str(self.port))
        self.serverIPLineEdit.setText(self.serverIP.toString())

        self.enterBtn.clicked.connect(self.slotEnterOrLeave)
        self.sendBtn.clicked.connect(self.slotSend)
        self.sendLineEdit.returnPressed.connect(self.slotSend)

        self.show()

    def slotEnterOrLeave(self):
        if not self.isOnline:
            if not self.validate(): return
            self.enterRoom()
        else:
            self.leaveRoom()

    def validate(self):
        if self.userNameLineEdit.text() == '':
            QMessageBox().information(self, 'ERROR', 'User Name Error!')
            return False
        self.userName = self.userNameLineEdit.text()

        if not self.serverIP.setAddress(self.serverIPLineEdit.text()):  # 判断给定的IP是否能够被正确解析
            QMessageBox().information(self, 'ERROR', 'Server IP Error!')
            return False

        if not (0 <= int(self.portLineEdit.text()) <= 65535):
            QMessageBox().information(self, 'ERROR', 'Server Port Error!')
            return False
        self.port = int(self.portLineEdit.text())
        return True

    def enterRoom(self):
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connectToHost(self.serverIP, self.port)

        self.tcpSocket.connected.connect(self.slotConnected)
        self.tcpSocket.readyRead.connect(self.slotDataReceived)
        self.tcpSocket.disconnected.connect(self.slotDisconnected)
        self.tcpSocket.error.connect(self.slotErrorOccured)

    def leaveRoom(self):
        sendData = '[-] ' + self.userName + ': Leave Chat Room'
        self.tcpSocket.write(bytes(sendData, encoding='utf-8'))
        self.tcpSocket.disconnectFromHost()

    def slotSend(self):
        if self.sendLineEdit.text() == '':
            return
        sendData = self.userName + ': ' + self.sendLineEdit.text()
        self.tcpSocket.write(bytes(sendData, encoding='utf-8'))
        self.sendLineEdit.clear()

    def slotConnected(self):
        self.sendBtn.setEnabled(True)
        self.userNameLineEdit.setEnabled(False)
        self.serverIPLineEdit.setEnabled(False)
        self.portLineEdit.setEnabled(False)
        self.enterBtn.setText('Leave Chat Room')
        self.isOnline = True

        sendData = '[+] ' + self.userName + ': Enter Chat Room'
        self.tcpSocket.write(bytes(sendData, encoding='utf-8'))

    def slotDataReceived(self):
        recvData = ''
        while self.tcpSocket.bytesAvailable() > 0:
            recvData = self.tcpSocket.read(self.tcpSocket.bytesAvailable())
        self.contentListWidget.addItem(str(recvData, encoding='utf-8'))
        self.contentListWidget.scrollToBottom()  # 滚动到最后一行

    def slotDisconnected(self):
        self.sendBtn.setEnabled(False)
        self.userNameLineEdit.setEnabled(True)
        self.serverIPLineEdit.setEnabled(True)
        self.portLineEdit.setEnabled(True)

        self.enterBtn.setText('Enter Chat Room')
        self.isOnline = False

    def closeEvent(self, event):
        if self.isOnline:
            msg = 'Are you sure to leave the chat room ?'
            reply = QMessageBox().warning(self, 'Quit', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.leaveRoom()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def slotErrorOccured(self, socketError):
        if socketError == 0:
            msg = '[*] ConnectionRefusedError: The connection was refused by the peer (or timed out).'
            self.contentListWidget.addItem(msg)
        elif socketError == 1:
            msg = '[*] RemoteHostClosedError: The remote host closed the connection.'
            self.contentListWidget.addItem(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TcpClient()
    app.exit(app.exec_())
