__author__ = 'Hk4Fun'
__date__ = '2018/5/24 0:29'

import logging

from AirConditioningV2.settings import *

logger = logging.getLogger('log')


def sendLog(func):
    def wrapper(*args, **kwargs):
        protocol, packet = args
        data = '|'.join(map(str, packet))
        if packet[0] == OPEN_CODE:
            logger.debug('roomId %s sendOpen: %s -> server', protocol.ac.roomId, data)
        elif packet[0] == CLOSE_CODE:
            logger.debug('roomId %s sendClose: %s -> server', protocol.ac.roomId, data)
        elif packet[0] == SPEED_CODE:
            logger.debug('roomId %s sendSpeed: %s -> server', protocol.ac.roomId, data)
        elif packet[0] == TEMP_CODE:
            logger.debug('roomId %s sendTemp: %s -> server', protocol.ac.roomId, data)
        elif packet[0] == TEMP_BACK_CODE:
            logger.debug('roomId %s sendTempBack: %s -> server', protocol.ac.roomId, data)
        elif packet[0] == STATE_CODE:
            logger.debug('sendState: %s -> roomId %s', data, protocol.ac.roomId)
        elif packet[0] == OPEN_ACK_CODE:
            logger.debug('sendOpenACK: %s -> roomId %s', data, protocol.ac.roomId)
        elif packet[0] == CLOSE_ACK_CODE:
            logger.debug('sendCloseACK: %s -> roomId %s', data, protocol.ac.roomId)
        elif packet[0] == SPEED_ACK_CODE:
            logger.debug('sendSpeedACK: %s -> roomId %s', data, protocol.ac.roomId)
        elif packet[0] == TEMP_ACK_CODE:
            logger.debug('sendTempACK: %s -> roomId %s', data, protocol.ac.roomId)
        elif packet[0] == HALT_CODE:
            logger.debug('sendHalt: %s -> roomId %s', data, protocol.ac.roomId)

        return func(*args, **kwargs)

    return wrapper


def recvLog(func):
    def wrapper(*args, **kwargs):
        protocol, data = args
        code, data = int(data[0]), '|'.join(data)
        if code == OPEN_ACK_CODE:
            logger.debug('roomId %s recvOpenACK: %s <- server', protocol.ac.roomId, data)
        elif code == CLOSE_ACK_CODE:
            logger.debug('roomId %s recvCloseACK: %s <- server', protocol.ac.roomId, data)
        elif code == SPEED_ACK_CODE:
            logger.debug('roomId %s recvSpeedACK: %s <- server', protocol.ac.roomId, data)
        elif code == TEMP_ACK_CODE:
            logger.debug('roomId %s recvTempACK: %s <- server', protocol.ac.roomId, data)
        elif code == STATE_CODE:
            logger.debug('roomId %s recvState: %s <- server', protocol.ac.roomId, data)
        elif code == HALT_CODE:
            logger.debug('roomId %s recvHalt: %s <- server', protocol.ac.roomId, data)
        elif code == OPEN_CODE:
            logger.debug('recvOpen: %s <- roomId %s', data, protocol.ac.roomId)
        elif code == SPEED_CODE:
            logger.debug('recvSpeed: %s <- roomId %s', data, protocol.ac.roomId)
        elif code == TEMP_CODE:
            logger.debug('recvTemp: %s <- roomId %s', data, protocol.ac.roomId)
        elif code == TEMP_BACK_CODE:
            logger.debug('recvTemBack: %s <- roomId %s', data, protocol.ac.roomId)
        elif code == CLOSE_CODE:
            logger.debug('recvClose: %s <- roomId %s', data, protocol.ac.roomId)
        return func(*args, **kwargs)

    return wrapper


def protocolErrorLog(func):
    def wrapper(*args, **kwargs):
        logger.error('severity error in protocol!')
        return func(*args, **kwargs)

    return wrapper


def queueFullLog(func):
    def wrapper(*args, **kwargs):
        logger.info('service queue is full!')
        return func(*args, **kwargs)

    return wrapper


def listenLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        ac, = args
        logger.info('server is listening at %s:%s', ac.serverIP.toString(), ac.port)
        return ret

    return wrapper


def newClientLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        logger.info('new connection: %s:%s', ret.peerAddress().toString(), ret.peerPort())
        return ret

    return wrapper


def disconFromClientLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        logger.info('client %s:%s disconnected', ret.peerAddress().toString(), ret.peerPort())
        return ret

    return wrapper


def closeServerLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        logger.info('server is shut down')
        return ret

    return wrapper


def connectHostLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret:
            ac, = args
            logger.info('connecting to the server %s:%s', ac.serverIP.toString(), ac.port)
        return ret

    return wrapper


def connectedLog(func):
    def wrapper(*args, **kwargs):
        ac, = args
        logger.info('successfully connected to the server %s:%s', ac.serverIP.toString(), ac.port)
        return func(*args, **kwargs)

    return wrapper


def disconFromServerLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        ac, = args
        logger.info('server %s:%s disconnected', ac.serverIP.toString(), ac.port)
        return ret

    return wrapper


def errorLog(func):
    def wrapper(*args, **kwargs):
        _, socketError = args
        if socketError == 0:
            logger.warning('ConnectionRefusedError: the connection was refused by the peer (or timed out)')
        elif socketError == 1:
            logger.error('RemoteHostClosedError: the remote host closed the connection')
        return func(*args, **kwargs)

    return wrapper


def emptyRoomLog(func):
    def wrapper(*args, **kwargs):
        ac, = args
        if not ac.ui.leRoomId.text():
            logger.warning('roomId is empty!')
        return func(*args, **kwargs)

    return wrapper


def dbConnectLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret:
            logger.info('successfully connecting to the database %s', DATABASE_NAME)
        else:
            logger.error('Unable to connect to the database %s', DATABASE_NAME)
        return ret

    return wrapper

def sqlLog(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        reporter = args[0]
        if not ret:
            logger.error(reporter.query.lastError().text())
        return ret

    return wrapper
