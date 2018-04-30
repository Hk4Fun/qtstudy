__author__ = 'Hk4Fun'
__date__ = '2018/4/28 23:57'

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.statusBar().showMessage('准备就绪')

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Hk4Fun--简单的菜单')

        exitAct = QAction(QIcon('Hk4Fun.jpg'), '退出(&E)', self) # 按住“Alt+E”的时候就能退出了
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出程序')
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件(&F)')
        fileMenu.addAction(exitAct)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
