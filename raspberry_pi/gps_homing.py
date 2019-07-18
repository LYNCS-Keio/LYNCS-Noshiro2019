#!/usr/bin/python
# -*- coding:utf-8 -*-

from lib import rover_gps
from lib import camera
from lib import capture
from lib import servo
from lib import MPU6050
from lib import pid
import time
import threading
import queue

Kp, Ki, Kd = 0.1, 0.1, 0.1
goal_pos = [0, 0]
position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pinL, pinR = 13, 18

timeout = 5

pos1 = [None, None]
r_theta_to_goal = [None, None]
azimuth_lock = threading.Lock()



class update_azimuth_with_gyro(threading.Thread):
    def __init__(self):
        super(update_azimuth_with_gyro, self).__init__()
        self.preT = time.time()
        self.pre_gyro = mpu.get_gyro_data_lsb()[2]
        self.azimuth = 0

    def run(self):
        while True:
            global r_theta_to_goal, azimuth_lock
            self.nowT = time.time()
            self.gyro = mpu.get_gyro_data_lsb()[2]

            azimuth_lock.acquire()
            r_theta_to_goal[1] += (self.gyro + self.pre_gyro) * (self.nowT - self.preT) / 2
            azimuth_lock.release()

            self.pre_gyro, self.preT = self.gyro, self.nowT



def update_azimuth_with_gps(pos1):
    UAwG_thread = threading.Timer(5, update_azimuth_with_gps)
    UAwG_thread.start()
    t = time.time()
    try:
        global r_theta_to_goal, azimuth_lock
        pos2 = [None, None]
        while (pos2[0] is None) and (pos2[1] is None):
            if (time.time() - t) > timeout:
                raise TimeoutError
            pos2 = gps.lat_long_measurement()            

        azimuth_lock.acquire()
        r_theta_to_goal = gps.convert_lat_long_to_r_theta(pos1[0], pos1[1], pos2[0], pos2[1])
        azimuth_lock.release()

        pos1 = pos2
    except:
        pass
    finally:
        pass





try:
    svL, svR = servo(pinL), servo(pinR)
    pid = pid(0.1, 0.1, 0.1)
    gps = rover_gps()
    mpu = MPU6050(0x68)
    '''
    release detection
    ↓
    release parachute
    ↓
    landing detection
    ↓
    GPS/GYRO Navigation
    ↓
    TV Navigation
    '''
    while (pos1[0] is None) and (pos1[1] is None):
        pos1 = gps.lat_long_measurement()


except:
    pass

finally:
    del svL, svR, pid
