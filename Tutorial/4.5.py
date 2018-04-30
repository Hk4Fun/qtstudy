__author__ = 'Hk4Fun'
__date__ = '2018/4/25 22:26'

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
from PyQt5.QtCore import (pyqtSignal, QObject, pyqtSlot)


class Signal(QObject):
    showmouse = pyqtSignal()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Hk4Fun')

        self.s = Signal()
        self.s.showmouse.connect(self.about)

        self.show()

    def about(self):
        QMessageBox.about(self, '鼠标', '你点鼠标了吧！')

    def mousePressEvent(self, e):
        self.s.showmouse.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
