__author__ = 'Hk4Fun'
__date__ = '2018/5/24 0:29'

import logging

from AirConditioningV2.settings import *


def sendLog(func):
    def wrapper(*args, **kwargs):
        self, packet = args
        data = '|'.join(map(str, packet))
        if packet[0] == OPEN_CODE:
            logging.debug('sendOpen: %s -> server', data)
        elif packet[0] == CLOSE_CODE:
            logging.debug('sendClose: %s -> server', data)
        elif packet[0] == SPEED_CODE:
            logging.debug('sendSpeed: %s -> server', data)
        elif packet[0] == TEMP_CODE:
            logging.debug('sendTemp: %s -> server', data)
        elif packet[0] == TEMP_BACK_CODE:
            logging.debug('sendTempBack: %s -> server', data)
        elif packet[0] == STATE_CODE:
            logging.debug('sendState: %s -> client:%s', data, self.ac.roomId)
        elif packet[0] == OPEN_ACK_CODE:
            logging.debug('sendOpenACK: %s -> client:%s', data, self.ac.roomId)
        elif packet[0] == CLOSE_ACK_CODE:
            logging.debug('sendCloseACK: %s -> client:%s', data, self.ac.roomId)
        elif packet[0] == SPEED_ACK_CODE:
            logging.debug('sendSpeedACK: %s -> client:%s', data, self.ac.roomId)
        elif packet[0] == TEMP_ACK_CODE:
            logging.debug('sendTempACK: %s -> client:%s', data, self.ac.roomId)
        elif packet[0] == HALT_CODE:
            logging.debug('sendHalt: %s -> client:%s', data, self.ac.roomId)

        return func(*args, **kwargs)

    return wrapper


def recvLog(func):
    def wrapper(*args, **kwargs):
        self, data = args
        code, data = int(data[0]), '|'.join(data)
        if code == OPEN_ACK_CODE:
            logging.debug('recvOpenACK: %s <- server', data)
        elif code == CLOSE_ACK_CODE:
            logging.debug('recvCloseACK: %s <- server', data)
        elif code == SPEED_ACK_CODE:
            logging.debug('recvSpeedACK: %s <- server', data)
        elif code == TEMP_ACK_CODE:
            logging.debug('recvTempACK: %s <- server', data)
        elif code == STATE_CODE:
            logging.debug('recvState: %s <- server', data)
        elif code == HALT_CODE:
            logging.debug('recvHalt: %s <- server', data)
        elif code == OPEN_CODE:
            logging.debug('recvOpen: %s <- client:%s', data, self.ac.roomId)
        elif code == SPEED_CODE:
            logging.debug('recvSpeed: %s <- client:%s', data, self.ac.roomId)
        elif code == TEMP_CODE:
            logging.debug('recvTemp: %s <- client:%s', data, self.ac.roomId)
        elif code == TEMP_BACK_CODE:
            logging.debug('recvTemBack: %s <- client:%s', data, self.ac.roomId)
        elif code == CLOSE_CODE:
            logging.debug('recvClose: %s <- client:%s', data, self.ac.roomId)
        return func(*args, **kwargs)

    return wrapper


def protocolErrorLog(func):
    def wrapper(*args, **kwargs):
        logging.error('severity error in protocol!')
        return func(*args, **kwargs)

    return wrapper


def queueFullLog(func):
    def wrapper(*args, **kwargs):
        logging.info('service queue is full!')
        return func(*args, **kwargs)

    return wrapper


def listenLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        self, = args
        logging.info('server is listening at %s:%s', self.serverIP.toString(), self.port)
        return res

    return wrapper


def newClientLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logging.info('new connection: %s:%s', res.peerAddress().toString(), res.peerPort())
        return res

    return wrapper


def disconFromClientLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logging.info('client %s:%s disconnected', res.peerAddress().toString(), res.peerPort())
        return res

    return wrapper


def closeServerLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logging.info('server is shut down')
        return res

    return wrapper


def connectHostLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        self, = args
        logging.info('connecting to the server %s:%s', self.serverIP.toString(), self.port)
        return res

    return wrapper


def connectedLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        self, = args
        logging.info('successfully connected to the server %s:%s', self.serverIP.toString(), self.port)
        return res

    return wrapper


def disconFromServerLog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        self, = args
        logging.info('server %s:%s disconnected', self.serverIP.toString(), self.port)
        return res

    return wrapper


def errorLog(func):
    def wrapper(*args, **kwargs):
        _, socketError = args
        if socketError == 0:
            logging.warning('ConnectionRefusedError: the connection was refused by the peer (or timed out)')
        elif socketError == 1:
            logging.error('RemoteHostClosedError: the remote host closed the connection')
        return func(*args, **kwargs)

    return wrapper
