__author__ = 'Hk4Fun'
__date__ = '2018/4/26 0:35'

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QFormLayout, QLabel, QLineEdit, QTextEdit)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()
    def Init_UI(self):
        self.setGeometry(300,300,300,200)
        self.setWindowTitle('Hk4Fun')

        formlayout = QFormLayout()
        nameLabel = QLabel("姓名")
        nameLineEdit = QLineEdit("")
        introductionLabel = QLabel("简介")
        introductionLineEdit = QTextEdit("")

        formlayout.addRow(nameLabel,nameLineEdit)
        formlayout.addRow(introductionLabel,introductionLineEdit)
        self.setLayout(formlayout)

        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec_())