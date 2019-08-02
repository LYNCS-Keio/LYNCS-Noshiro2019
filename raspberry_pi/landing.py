# -*- coding: utf-8 -*-

#from lib import BME280 as BME
#from lib import HCSR04
from lib import MPU6050
#from lib import servo
import RPi.GPIO as GPIO
import time
import csv
import os


sound_velocity = 34300
time_range=5 #加速度が落ち着いている判定の判定時間
break_time=30 #キャリア判定からの経過時間による着陸判定用
extent=0.02 #MPUの誤差込みの判定にするための変数
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=18 #マルチプレクサ側PWMのピン
trigger, echo = 19, 26
current_dir = os.path.dirname(os.path.abspath(__file__))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(pinPWM, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

for index in range(0,2):
    GPIO.setup(pinDMUX[index],GPIO.OUT)
    GPIO.output(pinDMUX[index],DMUX_out[index]) #分離サーボの出力指定

sv = GPIO.PWM(pinPWM, 50)
sv.start(8.5)

'''
BME.setup()
BME.get_calib_param()
'''

count_BME = 3 #BMEがn回連続で範囲内になったらbreak

try:
    index = 0
    filename = 'mpulog' + '%04d' % index
    while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
    index += 1
    filename = 'mpulog' + '%04d' % index
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        f = csv.writer(c, lineterminator='\n')
        
        now_t = time.time()

        while 1:
            gyro = mpu.get_gyro_data_lsb()
            accel = mpu.get_accel_data_lsb()
            row = [time.time()]
            row.extend(gyro)
            row.extend(accel)
            f.writerow(row)
            time.sleep(0.01)

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
        sv.ChangeDutyCycle(7.6)
  
finally:
    time.sleep(1)
    sv.stop()
    GPIO.cleanup()