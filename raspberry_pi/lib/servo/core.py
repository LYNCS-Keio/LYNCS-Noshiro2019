#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
-----Usage--------------
Initialize:
sv = servo(pin)

Rotate:
sv.rotate(dutycycle)

Destruct:
sv = None
------------------------

PWM signal: 50 Hz
dutyCycle       5    -   7.5   -    10
rotation    backward - nuetral - forward
"""
import RPi.GPIO as GPIO
import time
import sys

__all__ = ['servo_pulse']

class servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.srv = GPIO.PWM(self.pin, 50)
        self.srv.start(7.5)

    def rotate(self, duty):
        self.srv.ChangeDutyCycle(duty)


    def __del__(self):
        self.srv.stop()
        GPIO.cleanup(self.pin)

if __name__ == "__main__":
    args = sys.argv
    try:
        sv = servo(int(args[1]))
        sv.rotate(5)
        time.sleep(1)
        sv.rotate(10)
        time.sleep(1)
    finally:
        sv = None