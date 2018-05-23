__author__ = 'Hk4Fun'
__date__ = '2018/5/22 23:03'
import sys

from PyQt5.QtWidgets import (QWidget)

sys.path.append('..')
from AirConditioningV2.ui import ui_Reporter


class Reporter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.ui = ui_Reporter.Ui_Form()
        self.ui.setupUi(self)
        self.show()
