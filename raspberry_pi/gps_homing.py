# -*- coding:utf-8 -
from lib import rover_gps as GPS
from lib import servo
from lib import MPU6050
import RPi.GPIO as GPIO
import math
import time

pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
GPIO.setmode(GPIO.BCM)
for count in range(3):
    GPIO.setup(pinDMUX[count],GPIO.OUT)
    GPIO.output(pinDMUX[count],DMUX_out[count]) #分離サーボの出力指定

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
e1 = 0.00
e2 = 0.00
Kp = 0.1
Ki = 0.1
Kd = 0.1

#goalの座標
goal_lat = 35.555437
goal_long = 139.655772

#位置座標を保存
#回転角度
def cal_rotation_angle(preT,pre_gyro):
    nowT = time.time() #現在時刻
    now_gyro = MPU.get_gyro_data_lsb()[2] #現在の角速度

    #積分して回転角度を求める
    now_rotation_angle = (now_gyro + pre_gyro) * (nowT - preT) / 2
    return [nowT, now_gyro, now_rotation_angle]

#着地
pre=[None,None]
while pre[0] is None:
    pre = GPS.lat_long_measurement()

with servo.servo(pinL) as svL, servo.servo(pinR) as svR:
    svL.rotate(dutyL)
    svR.rotate(dutyR)
    MPU = MPU6050.MPU6050(0x68)
    to_goal , rotation_angle = [1,0] , 0
    flag = 0
    #goalとの距離が10m以下になったら画像での誘導
    while 1:
        now = [None, None]
        now = GPS.lat_long_measurement()
        if now[0] != None and now[1] != None:
            convert_now = GPS.convert_lat_long_to_r_theta(pre[0],pre[1],now[1],now[2])
            rotation_angle = convert_now[1]
            to_goal =  GPS.convert_lat_long_to_r_theta(now[0],now[1],goal_lat,goal_long)
            pre = now
            flag = 1
            if to_goal[0] < cam_dis:
                svR.rotate(7.5)
                svL.rotate(7.5)
                break

        elif flag == 1:
            #回転
            pre_gyro = math.radians(MPU.get_gyro_data_lsb()[2]) #degree to radian
            preT, pre_gyro, now_rotation_angle = cal_rotation_angle(preT, pre_gyro)
            rotation_angle += now_rotation_angle

        #dutyLを変える
        e2 = e1
        e1 = e
        e = to_goal[1] - rotation_angle
        M += Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))

        if e < math.pi/2 and e > -math.pi/2:
            zenshin = 1
        else:
            zenshin = 0

        if M > 1:
            M = 1
        if M < -1:
            M = -1

        dutyL = 7.5 + 2.5*((zenshin + M) / 2)
        dutyR = 7.5 - 2.5*((zenshin - M) / 2)

        svL.rotate(dutyL)
        svR.rotate(dutyR)
