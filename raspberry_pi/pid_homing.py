# -*- coding:utf-8 -
from lib import rover_gps as GPS
from lib import MPU6050
from lib import pid_controll
import RPi.GPIO as GPIO
import math
import time

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
cam_dis = 0

neutralL = 6.835
dutyL = neutralL + 1.5
neutralR = 6.86
dutyR = neutralR - 1.5
pinL = 13
pinR = 18
#PID
p = pid_controll.pid(0.004, 0.02365, 0.0002436)

#goalの座標
goal_lat = 35.554506
goal_long = 139.656850

correction = 0.91031267 #MPU補正値

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


#位置座標を保存
#回転角度
def cal_rotation_angle(preT,p_g):
    nowT = time.time() #現在時刻
    now_gyro = math.radians(MPU.get_gyro_data_lsb()[2]  + correction)#現在の角速度

    #積分して回転角度を求める
    now_rotation_angle = (now_gyro + p_g) * (nowT - preT) / 2
    return [nowT, now_gyro, now_rotation_angle]

#着地
pre=[None,None]
while pre[0] is None:
    pre = GPS.lat_long_measurement()

pt = time.time()
try:
    with servo(pinL) as svL, servo(pinR) as svR:
        svL.rotate(dutyL)
        svR.rotate(dutyR)
        MPU = MPU6050.MPU6050(0x68)
        time.sleep(10)
        to_goal , rotation = [1,0] , 0
        flag = 0
        #goalとの距離が10m以下になったら画像での誘導
        while 1:
            now = [None, None]
            now = GPS.lat_long_measurement()
            if now[0] != None and now[1] != None:
                to_goal[0] =  GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[0]
                if flag == 0:
                    to_goal[1] =  GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[1]
                    rotation = GPS.convert_lat_long_to_r_theta(pre[0],pre[1],now[0],now[1])[1]
                    preT = time.time()
                    pre_gyro = math.radians(MPU.get_gyro_data_lsb()[2] + correction)
                    flag = 1
                pre = now
                if to_goal[0] < cam_dis:
                    svR.rotate(neutralR)
                    svL.rotate(neutralL)
                    break

            #dutyLを変える
            gyro = mpu.get_gyro_data_lsb()[2] + drift
            nt = time.time()
            dt = nt - pt
            pt = nt
            rotation += gyro * dt
            m = p.update_pid(to_goal[1] - rotation, rotation, dt)
            m1 = min([max([m, -1]), 1])

            dL, dR = 6.835 + 1.25 * (1 - m1), 6.86 - 1.25 * (1 + m1)
            svL.ChangeDutyCycle(dL)
            svR.ChangeDutyCycle(dR)
            print([m, dL, dR, rotation])
            time.sleep(0.01)
finally:
    GPIO.cleanup()
    svL = None
    svR = None
