# -*- coding: utf-8 -*-
#!usr/bin/python

import time

__all__ = ['readData']

def writeReg(reg_address, data):
    pass


def get_calib_param():
    pass

_dummy_bme_count = 0
_ascend_descend_flag = False    ## False::上昇 True::降下
_dummy_gravity = 0.2

def readData():
    global _dummy_bme_count
    global _ascend_descend_flag
    global _gnd_flag
    
    mesure_high = _dummy_bme_count
    
    if _ascend_descend_flag:˙
        _dummy_bme_count -= _dummy_gravity
    
    if not _ascend_descend_flag:
        _dummy_bme_count += _dummy_gravity
        if _dummy_bme_count >= 50:
             _ascend_descend_flag = True
    
    if _dummy_bme_count < 0:
        _dummy_bme_count = 0
    
    time.sleep(0.0005)
    return [mesure_high, 0, 0]


if __name__ == '__main__':
    try:
        while True:
            print(readData())
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
