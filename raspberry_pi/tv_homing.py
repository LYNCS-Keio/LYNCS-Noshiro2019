# -*- coding: utf-8 -*-
from lib import camera
from lib import capture
from lib import MPU6050
from lib import pid_controll
import pigpio
import math
import time
import threading

pinL, pinR = 13, 12

AoV = 54  # angle of view
height = 240
width = 320
rotation = 0
drift = -1.092913
cam_interval = 1.5
rotation_lock = threading.Lock()

URwC_flag = 1

pi = pigpio.pi()

DMUX_pin = [11, 9, 10]  # マルチプレクサの出力指定ピンA,B,C
DMUX_out = [0, 0, 0]  # 出力ピン指定のHIGH,LOWデータ
for pin in range(0, 2):
    pi.set_mode(DMUX_pin[pin], pigpio.OUTPUT)
    pi.write(DMUX_pin[pin], DMUX_out[pin])
pi.set_mode(pinL, pigpio.OUTPUT)
pi.set_mode(pinR, pigpio.OUTPUT)

pt = time.time()

p = pid_controll.pid(0.004, 0.03, 0.0004)
mpu = MPU6050.MPU6050(0x68)


def update_rotation_with_cam():
    global rotation
    cap = capture.capture()
    cam = camera.CamAnalysis()
    while URwC_flag == 1:
        stream = cap.cap()
        cam.morphology_extract(stream)
        cam.save_all_outputs()
        coord = cam.contour_find()

        conX = ((coord[0] - width / 2) / (width / 2)) / math.sqrt(3)
        rotation_lock.acquire()
        rotation = math.degrees(math.atan(-conX))
        rotation_lock.release()
        print (coord[0], rotation)
    del cap, cam



try:
    URwC_thread = threading.Thread(target=update_rotation_with_cam)
    URwC_thread.start()
    print('URwC start')
    pt = time.time()
    
    while True:
        gyro = mpu.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        rotation_lock.acquire()
        rotation += gyro * dt
        rotation_lock.release()

        m = p.update_pid(0, rotation, dt)
        m1 = min([max([m, -1]), 1])
        dL, dR = 75000 + 12500 * (1 - m1), 75000 - 12500 * (1 + m1)
        print([m1, rotation])
        
        pi.hardware_PWM(pinL, 50, int(dL))
        pi.hardware_PWM(pinR, 50, int(dR))
        

finally:
    URwC_flag = 0
    pi.hardware_PWM(pinL, 0, 0)
    pi.hardware_PWM(pinR, 0, 0)
