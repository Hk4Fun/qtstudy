__author__ = 'Hk4Fun'
__date__ = '2018/5/15 17:24'

from AirConditioning.settings import *


def mapWindSpeed(wind_speed):
    return {LOW_WIND: '低风', MID_WIND: '中风', HIGH_WIND: '高风'}[wind_speed]

def mapMode(mode):
    return {COLD_MODE: '制冷', WARM_MODE: '制热'}[mode]


