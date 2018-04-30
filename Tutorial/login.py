__author__ = 'Hk4Fun'
__date__ = '2018/4/26 1:33'
from PyQt5 import QtWidgets, QtGui, QtSql
import sys


class LoginDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.InitUI()
        self.InitDb()

    def InitUI(self):
        self.setWindowTitle('登录')
        self.setGeometry(300, 300, 300, 150)

        self.leName = QtWidgets.QLineEdit(self)
        self.leName.setPlaceholderText('用户名')

        self.lePwd = QtWidgets.QLineEdit(self)
        self.lePwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lePwd.setPlaceholderText('密码')

        self.pbLogin = QtWidgets.QPushButton('登录', self)
        self.pbCancel = QtWidgets.QPushButton('取消', self)

        self.pbLogin.clicked.connect(self.login)
        self.pbCancel.clicked.connect(self.cancel)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.leName)
        layout.addStretch(1)
        layout.addWidget(self.lePwd)
        layout.addStretch(1)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.pbLogin)
        buttonLayout.addWidget(self.pbCancel)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def InitDb(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('db.sqlite3')
        self.db.open()

    def login(self):
        if self.valid(self.leName.text(), self.lePwd.text()):
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, '错误', '用户名密码不匹配！')
            self.lePwd.clear()
            self.lePwd.setFocus()

    def cancel(self):
        self.close()

    def valid(self, name, pwd):
        query = QtSql.QSqlQuery()
        query.prepare('select 1 from user where name = ? and pwd = ?')
        query.bindValue(0, name)
        query.bindValue(1, pwd)
        query.exec_()
        return query.next()



class Calculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Hk4Fun-计算器')
        self.setWindowIcon(QtGui.QIcon('Hk4Fun.jpg'))

        self.lcd = QtWidgets.QLCDNumber()
        grid.addWidget(self.lcd, 0, 0, 3, 0)
        grid.setSpacing(10)

        names = ['Cls', 'Bc', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(4, 9) for j in range(0, 4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QtWidgets.QPushButton(name)
            grid.addWidget(button, *position)
            button.clicked.connect(self.Cli)

        self.show()

    def Cli(self):
        sender = self.sender().text()
        ls = ['/', '*', '-', '=', '+']
        if sender in ls:
            self.lcd.display('A')
        else:
            self.lcd.display(sender)


def login():
    dialog = LoginDialog()
    if dialog.exec_(): return True
    return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if login():
        cal = Calculator()
        sys.exit(app.exec_())
