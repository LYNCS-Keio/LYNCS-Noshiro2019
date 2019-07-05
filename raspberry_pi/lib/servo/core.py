#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
PWM signal: 50 Hz
dutyCycle       5    -   7.5   -    10
rotation    backward - nuetral - forward
"""
import RPi.GPIO as GPIO
import time

pin1 = 12
pin2 = 18

__all__ = ['servo_pulse']

class servo:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        servo1 = GPIO.PWM(pin1, 50)
        servo2 = GPIO.PWM(pin2, 50)
        servo1.start(7.5)
        servo2.start(7.5)

    def rotate(select,duty):
        if select == 0:
            servo1.changeDutyCycle(duty)
        elif select == 1:
            servo2.changeDutyCycle(duty)
        else:
            pass

    def __del__():
        servo1.stop()
        servo2.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        srv = servo()
        srv.rotate(0, 5)
        time.sleep(1)
        srv.rotate(0, 10)
        time.sleep(1)
    finally:
        del srv