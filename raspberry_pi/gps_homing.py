# -*- coding:utf-8 -
from lib import rover_gps as GPS
from lib import servo
from lib import MPU6050
import RPi.GPIO as GPIO
import math
import time

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
cam_dis = 0

dutyL = 9.0
dutyR = 5.2
pinL = 13
pinR = 18
#PID
M = 0.00
M1 =  0.00
goal = 0.00
e = 0.00
e_prev = 0.00
integral = 0.0
dt = 0.01
Kp = 0.1
Ki = 0.1
Kd = 0.1

#goalの座標
goal_lat = 35.555437
goal_long = 139.655772

#位置座標を保存
#回転角度
def cal_rotation_angle(preT,p_g):
    nowT = time.time() #現在時刻
    now_gyro = MPU.get_gyro_data_lsb()[2] #現在の角速度

    #積分して回転角度を求める
    now_rotation_angle = (now_gyro + p_g) * (nowT - preT) / 2
    return [nowT, now_gyro, now_rotation_angle]

#着地
pre=[None,None]
while pre[0] is None:
    pre = GPS.lat_long_measurement()

try:
    with servo.servo(pinL) as svL, servo.servo(pinR) as svR:
        svL.rotate(dutyL)
        svR.rotate(dutyR)
        MPU = MPU6050.MPU6050(0x68)
        time.sleep(10)
        to_goal , rotation_angle = [1,0] , 0
        flag = 0
        #goalとの距離が10m以下になったら画像での誘導
        while 1:
            now = [None, None]
            now = GPS.lat_long_measurement()
            if now[0] != None and now[1] != None:
                to_goal[0] =  GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[0]
                if flag == 0:
                    to_goal[1] =  GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)[1]
                    rotation_angle = GPS.convert_lat_long_to_r_theta(pre[0],pre[1],now[0],now[1])[1]
                    preT = time.time()
                    pre_gyro = math.radians(MPU.get_gyro_data_lsb()[2])
                pre = now
                flag = 1
                if to_goal[0] < cam_dis:
                    svR.rotate(7.5)
                    svL.rotate(7.5)
                    break

            if flag == 1:
                preT, pre_gyro, now_rotation_angle = cal_rotation_angle(preT, pre_gyro)
                rotation_angle += now_rotation_angle
                while 1:
                    if rotation_angle > math.pi:
                        rotation_angle -= 2*math.pi
                    elif rotation_angle < -math.pi:
                        rotation_angle += 2*math.pi
                    else:
                        break

            #dutyLを変える
            e = to_goal[1] - rotation_angle
            integral += e * dt
            M = Kp * e + Ki * integral + Kd * (e - e_prev) / dt
            e_prev = e

            zenshin = 1

            #if M > 1:
            #    M = 1
            #if M < -1:
            #    M = -1

            dutyL = 7.5 + 2.5*((zenshin + M) / 2)
            dutyR = 7.5 - 2.5*((zenshin - M) / 2)

            svL.rotate(dutyL)
            svR.rotate(dutyR)
            print(M,rotation_angle)
finally:
    GPIO.cleanup()
    svL = None
    svR = None
