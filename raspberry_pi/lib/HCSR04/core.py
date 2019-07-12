#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
"""
-----Usage--------------
with HCSR04(trigger, echo) as hcs:
    print(hcs.readData())
------------------------
"""

class HCSR04:
    def __init__(self, tri, ech):
        self.trig = tri
        self.echo = ech
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)


    def __enter__(self):
        return self

        
    def readData(self, vel):
        self.sound_velocity = vel
        #self.outrange = 400 / self.sound_velocity
        GPIO.output(self.trig, True)
        time.sleep(0.000010)
        GPIO.output(self.trig, False)

        GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=10)
        self.time_1 = time.time()
        GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=15)
        self.delta = time.time() - self.time_1 + 0.0002

        self.distance = (self.delta * self.sound_velocity)/2
        return self.distance


    def __exit__(self, exception_type, exception_value, traceback):
        self.__del__()


    def __del__(self):
        GPIO.cleanup(self.trig)
        GPIO.cleanup(self.echo)



if __name__ == "__main__":
    args = sys.argv
    print args[1]
    with HCSR04(int(args[1]), int(args[2])) as hcs:
        while True:
            print(hcs.readData(34300))
            time.sleep(0.06)
