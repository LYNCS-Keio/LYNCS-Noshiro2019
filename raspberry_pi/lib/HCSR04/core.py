#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
"""
initialize:
hcs = HCSR04(trig_pin, echo_pin, sound_velocity)

read data:
hcs.readData() -> distsnce /cm
"""

class HCSR04:
    def __init__(self, tri, ech, vel):
        self.trig = tri
        self.echo = ech
        self.sound_velocity = vel
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def readData(self):
        GPIO.output(self.trig, True)
        time.sleep(0.000010)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo) == GPIO.LOW:
            self.time_1 = time.time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            self.delta = time.time() - self.time_1

        self.distance = (self.delta * self.sound_velocity)/2
        if self.distance >= 400:
            self.distance = 400
        elif self.distance <= 20:
            self.distance = 20
        else:
            pass
        return self.distance

    def __del__(self):
        GPIO.cleanup()

if __name__ == "__main__":
    args = sys.argv
    try:
        HCS = HCSR04(args[1], args[2], 34300)
        print(HCS.readData())
    finally:
        del HCS