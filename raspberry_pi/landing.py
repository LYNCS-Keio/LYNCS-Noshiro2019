# -*- coding: utf-8 -*-

from lib import BME280 as BME
#from lib import HCSR04
from lib import MPU6050
import pigpio
import time
import csv
import os


#sound_velocity = 34300
time_range = 5
mpu_break_time=120                                #加速度が落ち着いている判定の判定時間
bme_break_time=30                               #キャリア判定からの経過時間による着陸判定用
extent=0.02                                 #MPUの誤差込みの判定にするための変数
DMUX_pin=[11,9,10]                          #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0]                            #出力ピン指定のHIGH,LOWデータ
PWM_pin=12                                  #マルチプレクサ側PWMのピン
#trigger, echo = 19, 26
current_dir = os.path.dirname(os.path.abspath(__file__))

pi = pigpio.pi()

pi.set_mode(PWM_pin, pigpio.OUTPUT)
#GPIO.setup(trigger, GPIO.OUT)
#GPIO.setup(echo, GPIO.IN)

duty_lock = 68500
duty_release = 62500


mpu = MPU6050.MPU6050(0x68)


for pin in range(0,2):
    pi.set_mode(DMUX_pin[pin], pigpio.OUTPUT)
    pi.write(DMUX_pin[pin], DMUX_out[pin])  # 分離サーボの出力指定

pi.hardware_PWM(PWM_pin, 50, duty_lock)
time.sleep(0.5)


#BME.setup()
#BME.get_calib_param()

count = 0
count_BME = 10                              #BMEがn回範囲内になったらbreak


try:
    index = 0
    filename = 'landinglog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'landinglog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        f = csv.writer(c, lineterminator='\n')

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
        while 1:
            height_BME = BME.readData()
            row = [time.time() - start_t]
            print(height_BME)
            row.extend(height_BME)
            if height_BME[0] <= 3: #meter
                count +=1
                row.append(count)
            if count == count_BME:
                row.append("release parachute")
                break
            time.sleep(0.01)
            #elif time.time() - release_t >= bme_break_time:
            #    row.append("timeout")
            #    break
            f.writerow(row)

            '''
            GPIO.output(trigger, True)
            time.sleep(0.000010)
            GPIO.output(trigger, False)

            GPIO.wait_for_edge(echo, GPIO.RISING, timeout=10)
            time_1 = time.time()
            GPIO.wait_for_edge(echo, GPIO.FALLING, timeout=15)
            delta = time.time() - time_1 + 0.0002
            distance = (delta * sound_velocity) / 2
            print(distance)
            if (time.time()-now_t > break_time) or ((70 <= distance) and (distance <= 200)):
                break
            time.sleep(0.01)
            '''

        pi.hardware_PWM(PWM_pin, 50, duty_release)
        time.sleep(1)
        f.writerow(row)

finally:
    pi.hardware_PWM(PWM_pin, 0, 0)
    for pin in range(0, 2):
        pi.write(DMUX_pin[pin], 0)
