__author__ = 'Hk4Fun'
__date__ = '2018/5/15 17:24'

import time
import datetime

from AirConditioningV2.settings import *


def mapWindSpeed_c2w(wind_speed):
    return {LOW_WIND: '低风', MID_WIND: '中风', HIGH_WIND: '高风'}[wind_speed]


def mapWindSpeed_w2c(wind_speed):
    return {'低风': LOW_WIND, '中风': MID_WIND, '高风': HIGH_WIND}[wind_speed]


def mapMode_c2w(mode):
    return {COLD_MODE: '制冷', WARM_MODE: '制热'}[mode]


def mapUserLevel_c2w(userLevel):
    return {USER_NORMAL: '普通用户', USER_VIP: 'VIP'}[userLevel]


def timeFormat(timeStamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))


def isSettle(orderId):
    return '未结帐' if orderId == '0' else orderId


def mapDiscount(userLevel):
    return {USER_NORMAL: NORMAL_DISCOUNT, USER_VIP: VIP_DISCOUNT}[userLevel]


def discountFormat(discount):
    if discount == 1:
        return '无'
    return str(discount * 100) + '%'


def durationFormat(start, end):  # start,end -- timestamp
    start = datetime.datetime.fromtimestamp(start).replace(microsecond=0)  # microsecond=0忽略毫秒数
    end = datetime.datetime.fromtimestamp(end).replace(microsecond=0)
    return str(end - start)
