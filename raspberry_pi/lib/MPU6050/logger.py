# -*- coding: utf-8 -*-
import core
import time
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

mpu = core.MPU6050(0x68)

index = 0
filename = 'mpulog' + '%04d' % index
while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
    index += 1
    filename = 'mpulog' + '%04d' % index

with open(current_dir + '/' + filename + '.csv', 'w') as c:
    f = csv.writer(c, lineterminator='\n')
    while True:
        gyro = mpu.get_gyro_data_lsb()
        accel = mpu.get_accel_data_lsb()
        row = [time.time()]
        row.extend(gyro)
        row.extend(accel)
        f.writerow(row)
        time.sleep(0.01)
