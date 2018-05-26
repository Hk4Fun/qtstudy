__author__ = 'Hk4Fun'
__date__ = '2018/5/26 2:33'
import sys

from PyQt5.QtWidgets import (QMessageBox)
from PyQt5 import QtSql

sys.path.append('..')
from AirConditioningV2.logger import *


class Database:
    def __init__(self, server):
        self.server = server
        self.initDb()
        self.query = QtSql.QSqlQuery()

    @dbConnectLog
    def initDb(self):
        self.dbh = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.dbh.setDatabaseName(DATABASE_NAME)
        res = self.dbh.open()
        if not res:
            msg = '数据库连接异常: 无法打开数据库 {}'.format(DATABASE_NAME)
            QMessageBox().critical(self.server, '数据库连接异常', msg, QMessageBox.Yes, QMessageBox.Yes)
            self.server.close()
        return res

    @sqlLog
    def sqlPrepare(self, sql):
        return self.query.prepare(sql)

    @sqlLog
    def sqlExec(self, sql=None):
        if sql and not self.sqlPrepare(sql):
            return False
        return self.query.exec_()
