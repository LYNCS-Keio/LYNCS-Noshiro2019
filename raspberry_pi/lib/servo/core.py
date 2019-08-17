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
import sys

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

    def __del__(self):
        self.srv.stop()
        GPIO.cleanup(self.pin)

    def __exit__(self, exception_type, exception_value, traceback):
        pass

if __name__ == "__main__":
    args = sys.argv
    DMUX_pin=[11,9,10]
    DMUX_out = [1, 0, 0]
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DMUX_pin[0], GPIO.OUT)
    GPIO.setup(DMUX_pin[1], GPIO.OUT)
    GPIO.setup(DMUX_pin[2], GPIO.OUT)

    GPIO.output(DMUX_pin[0], DMUX_out[0])
    GPIO.output(DMUX_pin[1], DMUX_out[1])
    GPIO.output(DMUX_pin[2], DMUX_out[2])
    with servo(int(args[1])) as sv:
        while True:
            sv.rotate(float(args[2]))
