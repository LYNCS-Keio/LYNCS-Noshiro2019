#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
-----Usage--------------
with servo(pin) as sv:
    servo.rotate(dutyCycle)
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

    def __enter__(self):
        return self

    def rotate(self, duty):
        self.srv.ChangeDutyCycle(duty)

    def __exit__(self, exception_type, exception_value, traceback):
        self.srv.stop()
        GPIO.cleanup(self.pin)

if __name__ == "__main__":
    args = sys.argv
    with servo(int(args[1])) as sv:
        sv.rotate(5)
        time.sleep(1)
        sv.rotate(10)
        time.sleep(1)
