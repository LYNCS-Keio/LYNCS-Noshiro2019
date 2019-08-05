# -*-coding: utf-8 -*-

from lib import pid_controll
from lib import MPU6050
import RPi.GPIO as gpio
import time


rotation = 0
drift = 1.092913

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup([11, 9, 10, 13, 12], gpio.OUT)
gpio.output(11, False)
gpio.output(9, False)
gpio.output(10, False)
svL, svR = gpio.PWM(13, 50), gpio.PWM(12, 50)
svL.start(6.9)
svR.start(6.9)

mpu = MPU6050.MPU6050(0x68)
p = pid_controll.pid(0.004, 0.02365, 0.0002436)
#p = pid_controll.pid(4.8, 23.65, 0.2436)
pt = time.time()


def rotate(self, duty):
    self.srv.ChangeDutyCycle(duty)


try:
    while True:
        gyro = mpu.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        rotation += gyro * dt
        m = p.update_pid(0, rotation, dt)

        m1 = min([max([m, -1]), 1])

        dL, dR = 6.835 + 1.25 * (1 - m1), 6.86 - 1.25 * (1 + m1)
        svL.ChangeDutyCycle(dL)
        svR.ChangeDutyCycle(dR)
        print([m, dL, dR, rotation])
        time.sleep(0.01)

finally:
    svL.stop()
    svR.stop()
    gpio.cleanup()
