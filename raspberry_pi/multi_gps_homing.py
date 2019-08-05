# -*- coding:utf-8 -
from lib import rover_gps as GPS
from lib import MPU6050
from lib import pid_controll
import RPi.GPIO as GPIO
import math
import time
import threading

DMUX_pin=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out = [0, 0, 0]  #出力ピン指定のHIGH,LOWデータ
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

neutralL = 6.835
dutyL = neutralL + 1.5
neutralR = 6.86
dutyR = neutralR - 1.5
pinL = 13
pinR = 18
#PID

#p = pid_controll.pid(0.003, 0.03365, 0.0002436)
p = pid_controll.pid(0.004, 0.02365, 0.0002436)

#goalの座標
goal_lat = 35.554506
goal_long = 139.656850

drift = 0.91031267 #MPU補正値

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

def GPS():
    while 1:
        now = [None, None]
        now = GPS.lat_long_measurement()
            if now[0] != None and now[1] != None:
                to_goal[0] = GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[0]
                count += 1

                if count == 30:
                    to_goal[1] = -math.degrees(GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[1])
                    rotation = -math.degrees(GPS.convert_lat_long_to_r_theta(pre_30[0], pre_30[1], now[0], now[1])[1])
                    print("count!!!")
                    pre = now
                    #count = 0
                    pre_30 = now
                    return to_goal, rotation

                if to_goal[0] < cam_dis:
                    svR.rotate(neutralR)
                    svL.rotate(neutralL)
                    break

def gyro(to_goal, rotation):
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
        svL.rotate(dL)
        svR.rotate(dR)
        print([m, dL, dR, rotation])
        time.sleep(0.01)

        if to_goal[0] < cam_dis:
            svR.rotate(neutralR)
            svL.rotate(neutralL)
            break


#着地
pre=[None,None]
while pre[0] is None:
    pre = GPS.lat_long_measurement()
pre_30 = pre

pt = time.time()
try:
    with servo(pinR) as svR:
        '''
        svR.rotate(7.6)
        time.sleep(4)
        svR.rotate(6.9)
        time.sleep(0.2)
        DMUX_out = [0,0,0]
        GPIO.output(DMUX_pin[0], DMUX_out[0])
        GPIO.output(DMUX_pin[1], DMUX_out[1])
        GPIO.output(DMUX_pin[2], DMUX_out[2])
        svR.rotate(neutralR)
        '''
        MPU = MPU6050.MPU6050(0x68)
        to_goal , rotation = [1, 0] , 0
        count = 0
        #goalとの距離が10m以下になったら画像での誘導
        with servo(pinL) as svL:
            GPS()
            gyro()
                
finally:
    GPIO.cleanup()
    svL = None
    svR = None