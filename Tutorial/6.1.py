__author__ = 'Hk4Fun'
__date__ = '2018/4/26 1:27'

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.statusBar().showMessage('准备就绪')
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Hk4Fun--状态栏')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
