# -*- coding: utf-8 -*-

#from lib import BME280 as BME
#from lib import HCSR04
from lib import MPU6050
#from lib import servo
import RPi.GPIO as GPIO
import time
sound_velocity = 34300
time_range=5 #加速度が落ち着いている判定の判定時間
break_time=30 #キャリア判定からの経過時間による着陸判定用
extent=0.02 #MPUの誤差込みの判定にするための変数
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=18 #マルチプレクサ側PWMのピン
trigger, echo = 19, 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(pinPWM, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

for index in range(0,2):
    GPIO.setup(pinDMUX[index],GPIO.OUT)
    GPIO.output(pinDMUX[index],DMUX_out[index]) #分離サーボの出力指定

'''
BME.setup()
BME.get_calib_param()
'''

count_BME = 3 #BMEがn回連続で範囲内になったらbreak

try:
    sv = GPIO.PWM(pinPWM, 50)
    sv.start(7.5)

    sv.ChangeDutyCycle(8.5)

    '''
    #キャリア判定
    with MPU6050.MPU6050(0x68) as mpu:
        pre_g = mpu.get_accel_data_lsb()[2]
        while 1:
            g = mpu.get_accel_data_lsb()[2]
            if g <= 0.5 and pre_g < 0.5:
                break
            pre_g = g
    '''

    now_t = time.time()

    '''
    count = 0
    while 1: #meter
        height = BME.readData()
        if height <= 5:
            count += 1
        else :
            count = 0
        if count >= count_BME:
            break
    '''

    while 1:
        GPIO.output(trigger, True)
        time.sleep(0.000010)
        GPIO.output(trigger, False)

        GPIO.wait_for_edge(echo, GPIO.RISING, timeout=10)
        time_1 = time.time()
        GPIO.wait_for_edge(echo, GPIO.FALLING, timeout=15)
        delta = time.time() - time_1 + 0.0002

        distance = (delta * sound_velocity) / 2
        print(distance)
        if (time.time()-now_t > break_time) or ((50 <= distance) and (distance <= 200)):
            break
    sv.ChangeDutyCycle(7.6)
"""
#着陸判定

while 1:
    a_x,a_y,a_z = MPU.get_accel_data_lsb()
    accel=((a_x-a_y)**2+(a_y-a_z)**2+(a_z-a_x)**2)**0.5
    if 1+extent > accel and accel > 1-extent :
        if flag == 0:
            flag=1
            _time = time.time()
    else:
        flag=0
        _time=0

    if time.time()-now_t > break_time or time.time()-_time <= time_range :
        break
"""
finally:
    sv.stop()
    GPIO.cleanup()