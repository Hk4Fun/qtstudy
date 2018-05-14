__author__ = 'Hk4Fun'
__date__ = '2018/4/30 15:22'

import sys

from PyQt5.QtWidgets import (QApplication, QMessageBox, QWidget)
from PyQt5.QtNetwork import (QHostAddress, QTcpServer)

sys.path.append('..')
from ChatRoom.ui import ui_tcpServer


class ConnectClient():
    def __init__(self, socket, name='None'):
        self.socket = socket
        self.name = name


class TcpServer(QWidget):
    def __init__(self):
        super().__init__()
        self.isUp = False
        self.port = 8888
        self.serverIP = QHostAddress('127.0.0.1')
        self.tcpClientList = []
        self.initUi()

    def initUi(self):
        self.ui = ui_tcpServer.Ui_Form()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(1,1)
        self.ui.portLineEdit.setText(str(self.port))
        self.ui.serverIPLineEdit.setText(self.serverIP.toString())
        self.ui.openBtn.clicked.connect(self.slotOpenOrClose)
        self.show()

    def validate(self):
        if not self.serverIP.setAddress(self.ui.serverIPLineEdit.text()):  # 判断给定的IP是否能够被正确解析
            QMessageBox().information(self, 'ERROR', 'Server IP Error!')
            return False

        if not (0 <= int(self.ui.portLineEdit.text()) <= 65535):
            QMessageBox().information(self, 'ERROR', 'Server Port Error!')
            return False
        self.port = int(self.ui.portLineEdit.text())
        return True

    def slotOpenOrClose(self):
        if not self.isUp:
            if not self.validate(): return
            self.openRoom()
        else:
            self.closeRoom()

    def openRoom(self):
        self.ui.openBtn.setText('Close Chat Room')
        self.isUp = True
        self.ui.serverIPLineEdit.setEnabled(False)
        self.ui.portLineEdit.setEnabled(False)

        self.tcpServer = QTcpServer()
        self.tcpServer.listen(self.serverIP, self.port)
        msg = '[*] Server is listening on {}:{} ........'.format(self.serverIP.toString(), self.port)
        self.ui.contentListWidget.addItem(msg)
        self.tcpServer.newConnection.connect(self.addClient2List)

    def closeRoom(self):
        del (self.tcpServer)
        self.tcpClientList = []
        self.ui.userListWidget.clear()
        self.isUp = False
        self.ui.serverIPLineEdit.setEnabled(True)
        self.ui.portLineEdit.setEnabled(True)
        self.ui.openBtn.setText('Open Chat Room')
        msg = '[*] Chat Room is closed........'
        self.ui.contentListWidget.addItem(msg)

    def addClient2List(self):
        tcpClientSocket = self.tcpServer.nextPendingConnection()
        client = ConnectClient(tcpClientSocket)
        self.tcpClientList.append(client)
        tcpClientSocket.readyRead.connect(self.slotDataReceived)
        tcpClientSocket.disconnected.connect(self.slotDisconnected)
        self.ui.onlineNumLabel.setText(str(len(self.tcpClientList)))

    def slotDataReceived(self):
        tcpClientSocket = self.sender()
        recvData = ''
        while tcpClientSocket.bytesAvailable() > 0:
            recvData += str(tcpClientSocket.read(tcpClientSocket.bytesAvailable()), encoding='utf-8')
        self.ui.contentListWidget.addItem(recvData)
        self.ui.contentListWidget.scrollToBottom()
        self._parseData(recvData, tcpClientSocket)
        # 实现信息的广播, tcpClientList中保存了所有与服务器相连的TcpClientSocket对象
        for client in self.tcpClientList:
            client.socket.write(bytes(recvData, encoding='utf-8'))

    def slotDisconnected(self):
        # 从tcpClientList列表中将断开连接的TcpClientSocket对象删除
        tcpClientSocket = self.sender()
        idx = self._findClient(tcpClientSocket)
        if idx >= 0:
            del (self.tcpClientList[idx])
        self.ui.onlineNumLabel.setText(str(len(self.tcpClientList)))

    def _findClient(self, socket):
        for idx, client in enumerate(self.tcpClientList):
            if client.socket is socket:
                return idx
        return -1

    def _parseData(self, data, socket):
        if data.startswith('[+]'):
            name = data.split(':')[0][4:]
            idx = self._findClient(socket)
            if idx >= 0:
                self.tcpClientList[idx].name = name
                self.ui.userListWidget.addItem(name)
        elif data.startswith('[-]'):
            idx = self._findClient(socket)
            if idx >= 0:
                self.ui.userListWidget.takeItem(idx)

    def closeEvent(self, event):
        if self.isUp:
            msg = 'Are you sure to close the chat room ?'
            reply = QMessageBox().warning(self, 'Quit', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.closeRoom()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = TcpServer()
    app.exit(app.exec_())
