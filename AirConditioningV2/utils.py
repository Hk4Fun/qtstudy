__author__ = 'Hk4Fun'
__date__ = '2018/5/15 17:24'

from AirConditioningV2.settings import *


def mapWindSpeed_c2w(wind_speed):
    return {LOW_WIND: '低风', MID_WIND: '中风', HIGH_WIND: '高风'}[wind_speed]


def mapWindSpeed_w2c(wind_speed):
    return {'低风': LOW_WIND, '中风': MID_WIND, '高风': HIGH_WIND}[wind_speed]


def mapMode_c2w(mode):
    return {COLD_MODE: '制冷', WARM_MODE: '制热'}[mode]


def mapUserLevel_c2w(userLevel):
    return {USER_NORMAL: '普通用户', USER_VIP: 'VIP'}[userLevel]
