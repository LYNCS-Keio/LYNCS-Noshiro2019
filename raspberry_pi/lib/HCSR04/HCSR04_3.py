#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

HC_RESULT = 0
SOUND_VELOCITY = 34000
HC_TRIG = 2
HC_ECHO = 3

GPIO.setup(HC_TRIG, GPIO.OUT)
GPIO.setup(HC_ECHO, GPIO.IN)

try:
    while True:
        GPIO.output(HC_TRIG, True)
        time.sleep(0.000010)
        GPIO.output(HC_TRIG, False)

        while GPIO.input(HC_ECHO) == GPIO.LOW:
            SIGNALOFF = time.time()
        while GPIO.input(HC_ECHO) == GPIO.HIGH:
            SIGNALON = time.time()

        DELTATIME = SIGNALON - SIGNALOFF
        TEMP = (DELTATIME / 2) * SOUND_VELOCITY
        if TEMP >= 400:
            HC_RESULT = 400
        else:
            HC_RESULT = TEMP
        print('distance: %d cm' % HC_RESULT)
        time.sleep(0.1)
except:
    time.sleep(0.1)
finally:
    GPIO.cleanup()
