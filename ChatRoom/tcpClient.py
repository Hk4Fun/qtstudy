__author__ = 'Hk4Fun'
__date__ = '2018/4/30 13:02'

import sys

from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox)
from PyQt5.QtNetwork import (QHostAddress, QTcpSocket)

sys.path.append('..')
from ChatRoom.ui import ui_tcpClient


class TcpClient(QWidget):

    def __init__(self):
        super().__init__()
        self.isOnline = False
        self.port = 8888
        self.serverIP = QHostAddress('127.0.0.1')
        self.initUI()

    def initUI(self):
        self.ui = ui_tcpClient.Ui_Form()
        self.ui.setupUi(self)
        self.ui.sendBtn.setEnabled(False)
        self.ui.portLineEdit.setText(str(self.port))
        self.ui.serverIPLineEdit.setText(self.serverIP.toString())

        self.ui.enterBtn.clicked.connect(self.slotEnterOrLeave)
        self.ui.sendBtn.clicked.connect(self.slotSend)
        self.ui.sendLineEdit.returnPressed.connect(self.slotSend)

        self.show()

    def slotEnterOrLeave(self):
        if not self.isOnline:
            if not self.validate(): return
            self.enterRoom()
        else:
            self.leaveRoom()

    def validate(self):
        if self.ui.userNameLineEdit.text() == '':
            QMessageBox().information(self, 'ERROR', 'User Name Error!')
            return False
        self.userName = self.ui.userNameLineEdit.text()

        if not self.serverIP.setAddress(self.ui.serverIPLineEdit.text()):  # 判断给定的IP是否能够被正确解析
            QMessageBox().information(self, 'ERROR', 'Server IP Error!')
            return False

        if not (0 <= int(self.ui.portLineEdit.text()) <= 65535):
            QMessageBox().information(self, 'ERROR', 'Server Port Error!')
            return False
        self.port = int(self.ui.portLineEdit.text())
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
        if self.ui.sendLineEdit.text() == '':
            return
        sendData = self.userName + ': ' + self.ui.sendLineEdit.text()
        self.tcpSocket.write(bytes(sendData, encoding='utf-8'))
        self.ui.sendLineEdit.clear()

    def slotConnected(self):
        self.ui.sendBtn.setEnabled(True)
        self.ui.userNameLineEdit.setEnabled(False)
        self.ui.serverIPLineEdit.setEnabled(False)
        self.ui.portLineEdit.setEnabled(False)
        self.ui.enterBtn.setText('Leave Chat Room')
        self.isOnline = True

        sendData = '[+] ' + self.userName + ': Enter Chat Room'
        self.tcpSocket.write(bytes(sendData, encoding='utf-8'))

    def slotDataReceived(self):
        recvData = ''
        while self.tcpSocket.bytesAvailable() > 0:
            recvData = self.tcpSocket.read(self.tcpSocket.bytesAvailable())
        self.ui.contentListWidget.addItem(str(recvData, encoding='utf-8'))
        self.ui.contentListWidget.scrollToBottom()  # 滚动到最后一行

    def slotDisconnected(self):
        self.ui.sendBtn.setEnabled(False)
        self.ui.userNameLineEdit.setEnabled(True)
        self.ui.serverIPLineEdit.setEnabled(True)
        self.ui.portLineEdit.setEnabled(True)
        self.ui.enterBtn.setText('Enter Chat Room')
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
            self.ui.contentListWidget.addItem(msg)
        elif socketError == 1:
            msg = '[*] RemoteHostClosedError: The remote host closed the connection.'
            self.ui.contentListWidget.addItem(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TcpClient()
    app.exit(app.exec_())
