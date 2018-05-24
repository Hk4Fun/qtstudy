__author__ = 'Hk4Fun'
__date__ = '2018/5/23 21:29'

import sys
import logging
import argparse

from PyQt5.QtWidgets import QApplication

sys.path.append('..')
from AirConditioningV2.controller import Controller
from AirConditioningV2.subMachine import SubMachine


def setArgs():
    des = 'A distributed air conditioning temperature control system'
    ap = argparse.ArgumentParser(description=des)

    group = ap.add_mutually_exclusive_group(required=True)

    group.add_argument('-s', '--server', action='store_true',
                       help='start as a server')

    group.add_argument('-c', '--client', action='store_true',
                       help='start as a client')

    ap.add_argument('-q', '--quiet', action='store_const', const=0,
                    dest='level', default=2, help='only log errors')

    ap.add_argument('-v', '--verbose', action='count', dest='level',
                    default=2, help='verbose logging (repeat for more verbose)')

    ap.add_argument('-l', '--log', type=argparse.FileType('w'), help='log file')

    return ap.parse_args()


def setLog(args):
    # 不同文件间的log系统是相互影响的!!! 通过logging.getLogger('log')来使用同一份log配置
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger = logging.getLogger('log')
    logger.setLevel(levels[min(args.level, len(levels) - 1)])
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S'))
    logger.addHandler(ch)
    if args.log:
        fh = logging.FileHandler(args.log.name)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(fh)


if __name__ == '__main__':
    args = setArgs()
    setLog(args)
    app = QApplication(sys.argv)
    if args.server:
        server = Controller()
    elif args.client:
        client = SubMachine()
    app.exit(app.exec_())
