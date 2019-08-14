# -*- coding: utf-8 -*-

from lib import rover_gps as GPS
from lib import pid_controll
from lib import BME280 as BME
from lib import MPU6050
from lib import camera
from lib import capture
import pigpio
import time
import csv
import os
import math
import threading

time_range = 5
release_timeout =120
bme_timeout=30                              #キャリア判定からの経過時間による着陸判定用
extent=0.02                                 #MPUの誤差込みの判定にするための変数
DMUX_pin = [11, 9, 10]                      #マルチプレクサの出力指定ピンA,B,C
DMUX_out = [1, 0, 0]                        #出力ピン指定のHIGH,LOWデータ
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

count = 0
count_bme = 0
limit_bme = 10                              #BMEがn回範囲内になったらbreak

try:
    index = 0
    filename = 'cameralog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'cameralog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        csv_writer = csv.writer(c, lineterminator='\n')
        start_t = time.time()
        while 1:
            """
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
            """
            height_BME = BME.readData()
            print(height_BME)
            if height_BME[0] >= 40: #meter
                count_bme += 1
            else:
                count_bme = 0
            if count_bme >= limit_bme:
                break
            elif time.time() - start_t >= release_timeout:
                break
            time.sleep(0.0007)

        release_time = time.time()
        time.sleep(2)
        while 1:
            height_BME = BME.readData()
            row = [time.time()]
            print(height_BME)
            row.extend(height_BME)
            if height_BME[0] <= 3: #meter
                count +=1
                row.append(count)
            else:
                count = 0
            if count >= limit_bme:
                row.append("release parachute")
                break
            elif time.time() - release_time >= bme_timeout:
                row.append("timeout")
                break
            time.sleep(0.0007)
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
cam_dis = 0.003
forward_dis = 0.01  # 初めの直進距離(km)

pinL = 13
pinR = 12

m = 0

lock = threading.Lock()
p = pid_controll.pid(0.004, 0.03, 0.0004)

#goalの座標
goal_lat, goal_long = 40.1427210, 139.9874711 #本番用

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
        gyro = mpu.get_gyro_data_lsb()[2] + drift
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
    pi.set_mode(pinL, pigpio.OUTPUT)
    pi.set_mode(pinR, pigpio.OUTPUT)
    to_goal , rotation = [1, 0] , 0
    t1 = threading.Thread(target = gps_get)
    t2 = threading.Thread(target = gyro_get)
    t1.start()
    t2.start()

    with open(current_dir + '/' + filename + '.csv', 'w') as c:
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



##tv_homing

AoV = 54  # angle of view
height = 240
width = 320
rotation = 0
cam_interval = 1.5
area = 400
lock = threading.Lock()

URwC_flag = 1


def update_rotation_with_cam():
    global rotation, area
    cap = capture.capture()
    cam = camera.CamAnalysis()
    while URwC_flag == 1:
        stream = cap.cap()
        cam.morphology_extract(stream)
        cam.save_all_outputs()
        coord = cam.contour_find()

        conX = ((coord[0] - width / 2) / (width / 2)) / math.sqrt(3)

        lock.acquire()
        rotation = math.degrees(math.atan(-conX))
        area = coord[2]
        lock.release()

        #print (coord[0], rotation)

try:
    index = 0
    filename = 'cameralog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'cameralog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        csv_writer = csv.writer(c, lineterminator='\n')

    URwC_thread = threading.Thread(target=update_rotation_with_cam)
    URwC_thread.start()
    print('URwC start')
    pt = time.time()
    forward = 0
    count_spin = 0

    while True:
        if URwC_flag == 0 and (rotation <= 0.5 and rotation >= -0.5):
            URwC_flag = 1
            pi.hardware_PWM(pinL, 50, 75000)
            pi.hardware_PWM(pinR, 50, 75000)
            time.sleep(2)
            forward = 1

        if area <= 300 and forward == 1:
            rotation = -45
            URwC_flag = 0
            forward = 0
            count_spin += 1
            if count_spin == 9:
                rotation = 0
                forward = 1
                count_spin = 0
                URwC_flag = 1
        else:
            count_spin == 0
        if area >= 65280:
            URwC_flag = 0
            break

        gyro = mpu.get_gyro_data_lsb()[2] + drift
        nt = time.time()
        dt = nt - pt
        pt = nt
        lock.acquire()
        rotation += gyro * dt
        lock.release()

        m = p.update_pid(0, rotation, dt)
        m1 = min([max([m, -1]), 1])
        dL, dR = 75000 + 12500 * (forward - m1), 75000 - 12500 * (forward + m1)
        print([m1, rotation])

        pi.hardware_PWM(pinL, 50, int(dL))
        pi.hardware_PWM(pinR, 50, int(dR))
        csv_writer.writerow([time.time(), rotation, area])


finally:
    URwC_flag = 0
    pi.hardware_PWM(pinL, 0, 0)
    pi.hardware_PWM(pinR, 0, 0)
