# -*- coding:utf-8 -
from lib import rover_gps as GPS
from lib import MPU6050
from lib import pid_controll
import RPi.GPIO as GPIO
import math
import time
import threading

DMUX_pin=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out = [1, 0, 0]  #出力ピン指定のHIGH,LOWデータ
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DMUX_pin[0], GPIO.OUT)
GPIO.setup(DMUX_pin[1], GPIO.OUT)
GPIO.setup(DMUX_pin[2], GPIO.OUT)

GPIO.output(DMUX_pin[0], DMUX_out[0])
GPIO.output(DMUX_pin[1], DMUX_out[1])
GPIO.output(DMUX_pin[2], DMUX_out[2])

#画像誘導に切り替える距離(km)
cam_dis = 0.01
forward_dis = 0.01#初めの直進距離(km)

neutralL = 6.9
neutralR = 6.9
pinL = 13
pinR = 12
#PID

#p = pid_controll.pid(0.003, 0.03365, 0.0002436)
#p = pid_controll.pid(0.004, 0.02365, 0.0002436)
p = pid_controll.pid(0.004, 0.03, 0.0004)

#goalの座標
goal_lat, goal_long = 35.554506, 139.656850 #グラウンド
#goal_lat, goal_long = 35.5550, 139.6555 #自販機横

drift = -1.032555

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

def gps_get():
    global to_goal, rotation, pre
    flag = 0
    while 1:
        now = GPS.lat_long_measurement()
        if now[0] != None and now[1] != None:
            to_goal[0] = GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[0]
            print(to_goal[0])
            if flag == 0 and GPS.convert_lat_long_to_r_theta(pre[0], pre[1], now[0], now[1])[0] >= forward_dis:
                lock.acquire()
                to_goal[1] = -math.degrees(GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[1])
                rotation = -math.degrees(GPS.convert_lat_long_to_r_theta(pre[0], pre[1], now[0], now[1])[1])
                lock.release()
                print("count!!!", now)
                pre = now
                flag = 1
            if to_goal[0] < cam_dis:
                break

def gyro_get():
    global to_goal, rotation, dL, dR
    pt = time.time()
    while 1:
        #dutyLを変える
        gyro = MPU.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        rotation += gyro * dt
        m = p.update_pid(to_goal[1] , rotation, dt)
        m1 = min([max([m, -1]), 1])
        dL, dR = neutralL + 1.25 * (1 - m1), neutralR - 1.25 * (1 + m1)
        print([m, rotation, to_goal[1] - rotation])
        time.sleep(0.01)

        if to_goal[0] < cam_dis:
            break


#着地
while 1:
    pre = GPS.lat_long_measurement()
    if pre[0] != None:
        break
print(pre)
try:
    with servo(pinR) as svR:
        svR.rotate(7.8)
        time.sleep(4)
        svR.rotate(7.2)
        time.sleep(0.2)
        DMUX_out = [0,0,0]
        GPIO.output(DMUX_pin[0], DMUX_out[0])
        GPIO.output(DMUX_pin[1], DMUX_out[1])
        GPIO.output(DMUX_pin[2], DMUX_out[2])
        svR.rotate(neutralR)
        MPU = MPU6050.MPU6050(0x68)
        to_goal , rotation = [1, 0] , 0
        with servo(pinL) as svL:
                lock=threading.Lock()
                t1 = threading.Thread(target = gps_get)
                t2 = threading.Thread(target = gyro_get)
                t1.start()
                t2.start()
                while 1:
                    svL.rotate(dL)
                    svR.rotate(dR)
                    if to_goal[0] < cam_dis:
                        svR.rotate(neutralR)
                        svL.rotate(neutralL)
                        break

finally:
    GPIO.cleanup()
    svL = None
    svR = None
