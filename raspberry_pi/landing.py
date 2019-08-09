# -*- coding: utf-8 -*-

from lib import BME280 as BME
#from lib import HCSR04
from lib import MPU6050
import RPi.GPIO as GPIO
import time
import csv
import os


#sound_velocity = 34300
time_range=5 #加速度が落ち着いている判定の判定時間
break_time=30 #キャリア判定からの経過時間による着陸判定用
extent=0.02 #MPUの誤差込みの判定にするための変数
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=12 #マルチプレクサ側PWMのピン
#trigger, echo = 19, 26
current_dir = os.path.dirname(os.path.abspath(__file__))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(pinPWM, GPIO.OUT)
#GPIO.setup(echo, GPIO.IN)

mpu = MPU6050.MPU6050(0x68)

for pin in range(0,2):
    GPIO.setup(pinDMUX[pin],GPIO.OUT)
    GPIO.output(pinDMUX[pin],DMUX_out[pin]) #分離サーボの出力指定

sv = GPIO.PWM(pinPWM, 50)
sv.start(7.1)
time.sleep(0.5)
'''
BME.setup()
BME.get_calib_param()
'''

count = 0
count_BME = 10 #BMEがn回範囲内になったらbreak

try:
    index = 0
    filename = 'landinglog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
        index += 1
        filename = 'landinglog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        f = csv.writer(c, lineterminator='\n')

        count_mpu = 0
        while 1:
            accel3 = mpu.get_accel_data_lsb()
            g = (accel3[0]**2 + accel3[1]**2 + accel3[2]**2)**0.5
            if g <= 0.5:
                count_mpu += 1
            else:
                count_mpu = 0
            if count_mpu >= 10:
                break
        open_t = time.time()

        while 1:
            height_BME = BME.readData()
            row = [time.time()]
            row.extend(height_BME)
            if height_BME <= 3: #メートル
                count +=1
            if count == count_BME or time.time() - open_t >= break_time:
                    row.append("パラ分離")
                    break
            f.writerow(row)

            #GPIO.output(trigger, True)
            #time.sleep(0.000010)
            #GPIO.output(trigger, False)

            #GPIO.wait_for_edge(echo, GPIO.RISING, timeout=10)
            #time_1 = time.time()
            #GPIO.wait_for_edge(echo, GPIO.FALLING, timeout=15)
            #delta = time.time() - time_1 + 0.0002
            #distance = (delta * sound_velocity) / 2
            #print(distance)
            #if (time.time()-now_t > break_time) or ((70 <= distance) and (distance <= 200)):
            #    break
            #time.sleep(0.01)

        sv.ChangeDutyCycle(6.6)
        time.sleep(1)
        f.writerow(row)

finally:
    time.sleep(1)
    sv.stop()
    GPIO.cleanup()
