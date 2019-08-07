# -*- coding: utf-8 -*-
from lib import camera
from lib import capture
from lib import MPU6050
from lib import pid_controll
import RPi.GPIO as gpio
import math
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

DMUX_pin = [11, 9, 10]  # マルチプレクサの出力指定ピンA,B,C
DMUX_out = [0, 0, 0]  # 出力ピン指定のHIGH,LOWデータ
GPIO.setup(DMUX_pin[0], GPIO.OUT)
GPIO.setup(DMUX_pin[1], GPIO.OUT)
GPIO.setup(DMUX_pin[2], GPIO.OUT)

GPIO.output(DMUX_pin[0], DMUX_out[0])
GPIO.output(DMUX_pin[1], DMUX_out[1])
GPIO.output(DMUX_pin[2], DMUX_out[2])

p = pid_controll.pid(0.004, 0.03, 0.0002436)


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
    stream = cap.cap()
    cam.morphology_extract(stream)
    coord = cam.contour_find()

    conX = ((coord[0] - width / 2) / (width / 2)) / math.sqrt(3)
    rotation_lock.acquire()
    rotation = math.atan(conX)
    rotation_lock.release()



pt = time.time()
try:
    svL, svR = servo(pinL), servo(pinR)
    cap = capture.capture()
    cam = camera.CamAnalysis()
    mpu = MPU6050.MPU6050(0x68)

    URwG_thread = threading.Thread(target=update_rotation_with_gyro)
    URwC_thread = threading.Thread(target=update_rotation_with_cam)
    URwG_thread.start()
    URwC_thread.start()

    while True:
        m = p.update_pid(to_goal[1], rotation, dt)
        m1 = min([max([m, -1]), 1])
        dL, dR = neutralL + 1.25 * (1 - m1), neutralR - 1.25 * (1 + m1)
        print([m, rotation, to_goal[1] - rotation])

        svL.rotate(dL)
        svR.rotate(dR)


except:
    pass

finally:
    del svL, svR, cap
    gpio.cleanup()
