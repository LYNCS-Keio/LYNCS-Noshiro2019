# -*- coding: utf-8 -*-
from lib import camera
from lib import capture
from lib import MPU6050
import RPi.GPIO as GPIO
import time

pinL, pinR = 13, 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
AoV = 54  # angle of view
height = 480
width = 640


class servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.srv = GPIO.PWM(self.pin, 50)
        self.srv.start(7.5)

    def __enter__(self):
        return self

    def rotate(self, duty):
        self.srv.ChangeDutyCycle(duty)

    def __del__(self):
        self.srv.stop()

    def __exit__(self, exception_type, exception_value, traceback):
        pass


try:
    svL, svR = servo(pinL), servo(pinR)
    cap = capture.capture()
    cam = camera.CamAnalysis()
    while True:
        stream = cap.cap()
        cam.morphology_extract(stream)
        coord = cam.contour_find()
        azimuth = AoV/2 - (54/width)*coord[0]


except:
    pass

finally:
    del svL, svR, cap
    GPIO.cleanup()
