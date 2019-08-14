# -*- coding: utf-8 -*-

from lib import rover_gps as GPS
from lib import pid_controll
from lib import BME280 as BME
from lib import MPU6050
import pigpio
import time
import csv
import os
import math
import threading

time_range = 5
mpu_break_time=120                          #加速度が落ち着いている判定の判定時間
bme_break_time=30                           #キャリア判定からの経過時間による着陸判定用
extent=0.02                                 #MPUの誤差込みの判定にするための変数
DMUX_pin=[11,9,10]                          #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0]                            #出力ピン指定のHIGH,LOWデータ
PWM_pin=12                                  #マルチプレクサ側PWMのピン

current_dir = os.path.dirname(os.path.abspath(__file__))
pi = pigpio.pi()
pi.set_mode(PWM_pin, pigpio.OUTPUT)
duty_lock = 68500
duty_release = 62500

mpu = MPU6050.MPU6050(0x68)

for pin in range(0,2):
    pi.set_mode(DMUX_pin[pin], pigpio.OUTPUT)
    pi.write(DMUX_pin[pin], DMUX_out[pin])  # 分離サーボの出力指定
pi.hardware_PWM(PWM_pin, 50, duty_lock)
time.sleep(0.5)

#goal_lat, goal_long = 35.5550, 139.6555 #自販機横
count = 0
count_BME = 10                              #BMEがn回範囲内になったらbreak

try:
    index = 0
    filename = 'landinglog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'landinglog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        csv_writer = csv.writer(c, lineterminator='\n')
        count_mpu = 0
        start_t = time.time()
        while 1:
            accel3 = mpu.get_accel_data_lsb()
            g = (accel3[0]**2 + accel3[1]**2 + accel3[2]**2)**0.5
            if g <= 0.5:
                count_mpu += 1
            else:
                count_mpu = 0
            if count_mpu >= 10:
                break
            elif time.time() - start_t >= mpu_break_time:
                break
        release_t = time.time()
        time.sleep(2)
        while 1:
            height_BME = BME.readData()
            row = [time.time() - start_t]
            print(height_BME)
            row.extend(height_BME)
            if height_BME[0] <= 3: #meter
                count +=1
                row.append(count)
            else:
                count = 0
            if count >= count_BME:
                row.append("release parachute")
                break
            time.sleep(0.0007)
            #elif time.time() - release_t >= bme_break_time:
            #    row.append("timeout")
            #    break
            csv_writer.writerow(row)
        pi.hardware_PWM(PWM_pin, 50, duty_release)
        time.sleep(1)
        csv_writer.writerow(row)
finally:
    pi.hardware_PWM(PWM_pin, 0, 0)
    for pin in range(0, 2):
        pi.write(DMUX_pin[pin], 0)

## multi_gps_homing

#画像誘導に切り替える距離(km)
cam_dis = 0.005
forward_dis = 0.01  # 初めの直進距離(km)

pinL = 13
pinR = 12

m = 0

lock = threading.Lock()

DMUX_pin=[11,9,10]                      #マルチプレクサの出力指定ピンA,B,C
DMUX_out = [1, 0, 0]                    #出力ピン指定のHIGH,LOWデータ
for pin in range(0, 2):
    pi.set_mode(DMUX_pin[pin], pigpio.OUTPUT)
    pi.write(DMUX_pin[pin], DMUX_out[pin])


p = pid_controll.pid(0.004, 0.03, 0.0004)

#goalの座標
goal_lat, goal_long = 35.5545974, 139.6563162 #グラウンド

drift = -1.032555

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
    global to_goal, rotation, dL, dR, m
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
        dL, dR = 75000 + 12500 * (1 - m1), 75000 - 12500 * (1 + m1)
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
    index = 0
    filename = 'gps_hom_log' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'gps_hom_log' + '%04d' % index


    DMUX_out = [0,0,0]
    for pin in range(0, 2):
        pi.write(DMUX_pin[pin], DMUX_out[pin])
    MPU = MPU6050.MPU6050(0x68)
    pi.set_mode(pinL, pigpio.OUTPUT)
    pi.set_mode(pinR, pigpio.OUTPUT)
    to_goal , rotation = [1, 0] , 0
    t1 = threading.Thread(target = gps_get)
    t2 = threading.Thread(target = gyro_get)
    t1.start()
    t2.start()


    with open(current_dir + '/' + filename + f'.csv', 'w') as c:
        csv_writer = csv.writer(c, lineterminator='\n')
        while 1:
            pi.hardware_PWM(pinL, 50, int(dL))
            pi.hardware_PWM(pinR, 50, int(dR))
            if to_goal[0] < cam_dis:
                pi.hardware_PWM(pinL, 50, 75000)
                pi.hardware_PWM(pinR, 50, 75000)
                break
            csv_writer.writerow([time.time(), m, rotation, to_goal[1] - rotation])


finally:
    pi.hardware_PWM(pinL, 0, 0)
    pi.hardware_PWM(pinR, 0, 0)
