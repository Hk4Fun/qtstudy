__author__ = 'Hk4Fun'
__date__ = '2018/4/25 23:16'

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Hk4Fun')

        bt1 = QPushButton('剪刀', self)
        bt2 = QPushButton('石头', self)
        bt3 = QPushButton('布', self)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(bt1)
        hbox.addWidget(bt2)
        hbox.addWidget(bt3)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec_())
