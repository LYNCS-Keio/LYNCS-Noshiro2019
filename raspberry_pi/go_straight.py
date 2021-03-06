# -*-coding: utf-8 -*-

from lib import pid_controll
from lib import MPU6050
import pigpio
import time


rotation = 0
drift = -1.032555


pi = pigpio.pi()

pi.set_mode(11, pigpio.OUTPUT)
pi.set_mode(9, pigpio.OUTPUT)
pi.set_mode(10, pigpio.OUTPUT)
pi.set_mode(13, pigpio.OUTPUT)
pi.set_mode(12, pigpio.OUTPUT)
pi.write(11, 0)
pi.write(9, 0)
pi.write(10, 0)
svL, svR = pi.hardware_PWM(13, 50, 75000), pi.hardware_PWM(12, 50, 75000)


mpu = MPU6050.MPU6050(0x68)
p = pid_controll.pid(0.004, 0.03, 0.0004)
#p = pid_controll.pid(4.8, 23.65, 0.2436)
pt = time.time()


try:
    while True:
        gyro = mpu.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        rotation += gyro * dt
        m = p.update_pid(0, rotation, dt)

        m1 = min([max([m, -1]), 1])

        dL, dR = 75000 + 12500 * (1 - m1), 75000 - 12500 * (1 + m1)
        pi.hardware_PWM(13, 50, int(dL))
        pi.hardware_PWM(12, 50, int(dR))
        print([m, dL, dR, rotation])
        time.sleep(0.01)

finally:
    pi.hardware_PWM(12, 0, 0)
    pi.hardware_PWM(13, 0, 0)
