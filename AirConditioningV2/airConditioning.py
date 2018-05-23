__author__ = 'Hk4Fun'
__date__ = '2018/5/23 21:29'

import sys
import logging
import argparse

from PyQt5.QtWidgets import QApplication

sys.path.append('..')
from AirConditioningV2.controller import Controller
from AirConditioningV2.subMachine import SubMachine

if __name__ == '__main__':
    des = 'A distributed air conditioning temperature control system'
    ap = argparse.ArgumentParser(description=des)

    ap.add_argument('-m', dest='mode', choices=['server', 'client'],
                    required=True, help='start as a server or client')

    ap.add_argument('-q', '--quiet', action='store_const', const=0,
                    dest='level', default=2, help='only log errors')

    ap.add_argument('-v', '--verbose', action='count', dest='level',
                    default=2, help='verbose logging (repeat for more verbose)')

    args = ap.parse_args()
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[min(args.level, len(levels) - 1)],
                        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

    app = QApplication(sys.argv)
    if args.mode == 'server':
        controller = Controller()
    else:
        subMachine = SubMachine()
    app.exit(app.exec_())
