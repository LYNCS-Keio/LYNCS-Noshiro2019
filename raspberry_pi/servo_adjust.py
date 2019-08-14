# -*- coding: utf-8 -*-

import pigpio
import sys
import time

pi = pigpio.pi()


try:
    DMUX_pin=[11,9,10]
    DMUX_out = [1, 0, 0]
    for pin in range(0, 2):
        pi.set_mode(DMUX_pin[pin], pigpio.OUTPUT)
        pi.write(DMUX_pin[pin], DMUX_out[pin])

    args = sys.argv
    pi.set_mode(13, pigpio.OUTPUT)

    pi.hardware_PWM(13, 50, int(args[1]))
    time.sleep(1)

finally:
    pi.hardware_PWM(12, 0, 0)

    for pin in range(0, 2):
        pi.write(DMUX_pin[pin], 0)
