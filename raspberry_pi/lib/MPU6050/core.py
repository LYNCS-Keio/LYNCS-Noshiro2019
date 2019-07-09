# -*- coding: utf-8 -*-
#!/usr/bin/python

# import module
import smbus		# use I2C
import math		# mathmatics

__all__ = ['get_gyro_data_lsb', 'get_accel_data_lsb', 'slope']


# slave address
DEV_ADDR = 0x68		# device address
# register address
ACCEL_XOUT = 0x3b	#
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
PWR_MGMT_1 = 0x6b	# PWR_MGMT_1
PWR_MGMT_2 = 0x6c	# PWR_MGMT_2

bus = smbus.SMBus(1)
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

# 1byte read
def read_byte(adr):
    return bus.read_byte_data(DEV_ADDR, adr)
# 2byte read
def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val
# Sensor data read
def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):
    # minus
        return -((65535 - val) + 1)
    else:
    # plus
        return val

#
# 角速度
#
# get gyro data
def get_gyro_data_lsb():
    x = read_word_sensor(GYRO_XOUT)
    y = read_word_sensor(GYRO_YOUT)
    z = read_word_sensor(GYRO_ZOUT)
    # 角速度表示
    x /= 131.0
    y /= 131.0
    z /= 131.0

    return [x, y, z]

#
# 加速度
#
# get accel data
def get_accel_data_lsb():
    x = read_word_sensor(ACCEL_XOUT)
    y = read_word_sensor(ACCEL_YOUT)
    z = read_word_sensor(ACCEL_ZOUT)
    # 加速度表示
    x /= 16384.0
    y /= 16384.0
    z /= 16384.0

    return [x, y, z]

#
# 傾き
# θ = 水平線とx軸との角度
# ψ = 水平線とy軸との角度
# φ = 重力ベクトルとz軸との角度
# 

def slope(x, y, z):   #radian
    theta = math.atan(x / (y*y + z*z)**0.5)
    psi = math.atan(y / (x*x + z*z)**0.5)
    phi = math.atan((x*x + y*y)**0.5 / z)

    return [theta, psi, phi]

if __name__ == '__main__':
    while 1:
        gyro_x, gyro_y, gyro_z = get_gyro_data_lsb()
        accel_x, accel_y, accel_z = get_accel_data_lsb()
        slope_theta, slope_psi, slope_phi = slope(accel_x, accel_y, accel_z)

        print'gyro_x=%8.3f' % gyro_x     
        print'gyro_y=%8.3f' % gyro_y     
        print'gyro_z=%8.3f' % gyro_z

        print'accel_x=%6.3f' % accel_x     
        print'accel_y=%6.3f' % accel_y     
        print'accel_z=%6.3f' % accel_z

        print'θ=%6.3f' % slope_theta
        print'ψ=%6.3f' % slope_psi
        print'φ=%6.3f' % slope_phi
