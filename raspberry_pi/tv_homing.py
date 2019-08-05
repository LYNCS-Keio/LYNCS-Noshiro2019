# -*- coding: utf-8 -*-
from lib import camera
from lib import capture
from lib import MPU6050
import RPi.GPIO as gpio
import time
import threading

pinL, pinR = 13, 12

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
AoV = 54  # angle of view
height = 480
width = 640
rotation = 0
drift = 1.092913
cam_interval = 1
rotation_lock = threading.Lock()


class servo:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.srv = gpio.PWM(self.pin, 50)
        self.srv.start(7.5)

    def __enter__(self):
        return self

    def rotate(self, duty):
        self.srv.ChangeDutyCycle(duty)

    def __del__(self):
        self.srv.stop()

    def __exit__(self, exception_type, exception_value, traceback):
        pass


def update_rotation_with_gyro():
    global rotation, nt, pt
    while True:
        gyro = mpu.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        rotation_lock.acquire()
        rotation += gyro * dt
        rotation_lock.release()


def update_rotation_with_cam():
    UAwC_thread = threading.Timer(cam_interval, update_rotation_with_cam)
    UAwC_thread.start()
    global rotation



pt = time.time()
try:
    svL, svR = servo(pinL), servo(pinR)
    cap = capture.capture()
    cam = camera.CamAnalysis()
    mpu = MPU6050.MPU6050(0x68)

    URwG_thread = threading.Thread(target=update_rotation_with_gyro)
    URwG_thread.start()


except:
    pass

finally:
    del svL, svR, cap
    gpio.cleanup()
