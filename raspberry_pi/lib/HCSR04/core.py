#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        SOUND_VELOCITY = 34000
        HC_TRIG = 2
        HC_ECHO = 3

        GPIO.setup(HC_TRIG, GPIO.OUT)
        GPIO.setup(HC_ECHO, GPIO.IN)

    def readData(self):
        GPIO.output(HC_TRIG, True)
        time.sleep(0.000010)
        GPIO.output(HC_TRIG, False)

        while GPIO.input(HC_ECHO) == GPIO.LOW:
            S_OFF = time.time()
        while GPIO.input(HC_ECHO) == GPIO.HIGH:
            S_ON = time.time()

        D_TIME = S_ON - S_OFF
        distance = (D_TIME * SOUND_VELOCITY)/2
        if distance >= 400:
            distance = 400
        elif distance <= 20:
            distance = 20
        else:
            distance = distance
        return distance

    def __del__(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        HCS = HCSR04()
        print(HCS.readData())
    finally:
        del HCS