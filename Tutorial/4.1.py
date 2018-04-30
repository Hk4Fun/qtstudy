__author__ = 'Hk4Fun'
__date__ = '2018/4/25 20:55'

import sys
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QDial, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        lcd = QLCDNumber(self)
        dial = QDial(self)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Hk4Fun')

        lcd.setGeometry(100, 50, 150, 60)
        dial.setGeometry(120, 120, 100, 100)

        dial.valueChanged.connect(lcd.display)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
