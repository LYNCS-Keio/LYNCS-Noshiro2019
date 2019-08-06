# -*- coding: utf-8 -*-
#!/usr/bin/python

# import module
import smbus		# use I2C
import math  # mathmatics
import time

__all__ = ['MPU6050']

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

class MPU6050():
    def __init__(self,device):
        self.bus = smbus.SMBus(1)
        time.sleep(0.1)
        self.DEV_ADDR = device
        self.bus.write_byte_data(self.DEV_ADDR, PWR_MGMT_1, 0)

    # 1byte read
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.DEV_ADDR, adr)

    # 2byte read
    def read_word(self,adr):
        self.high = self.bus.read_byte_data(self.DEV_ADDR, adr)
        self.low = self.bus.read_byte_data(self.DEV_ADDR, adr+1)
        self.val = (self.high << 8) + self.low
        return self.val

    # Sensor data read
    def read_word_sensor(self,adr):
        self.val = self.read_word(adr)
        if (self.val >= 0x8000):
        # minus
            return -((65535 - self.val) + 1)
        else:
        # plus
            return self.val

    #
    # gyro
    #
    # get gyro data
    def get_gyro_data_lsb(self):
        self.x = self.read_word_sensor(GYRO_XOUT)
        self.y = self.read_word_sensor(GYRO_YOUT)
        self.z = self.read_word_sensor(GYRO_ZOUT)
        # show gyro
        self.x /= 131.0
        self.y /= 131.0
        self.z /= 131.0

        return [self.x, self.y, self.z]

    #
    # accel
    #
    # get accel data
    def get_accel_data_lsb(self):
        self.x = self.read_word_sensor(ACCEL_XOUT)
        self.y = self.read_word_sensor(ACCEL_YOUT)
        self.z = self.read_word_sensor(ACCEL_ZOUT)
        # show accel
        self.x /= 16384.0
        self.y /= 16384.0
        self.z /= 16384.0

        return [self.x, self.y, self.z]

    #
    # slope
    # theta : horizon - x_axis
    # psi : horizon - y_axis
    # phi : perpendicular - z_axis
    #

    def slope_accel(self, x, y, z):   #radian
        self.theta = math.atan(x / (y*y + z*z)**0.5)
        self.psi = math.atan(y / (x*x + z*z)**0.5)
        self.phi = math.atan((x*x + y*y)**0.5 / z)

        return [self.theta, self.psi, self.phi]



if __name__ == '__main__':
    while True:
        mpu = MPU6050(0x68)
        gyro_x, gyro_y, gyro_z = mpu.get_gyro_data_lsb()
        accel_x, accel_y, accel_z = mpu.get_accel_data_lsb()
        slope_theta, slope_psi, slope_phi = mpu.slope_accel(accel_x, accel_y, accel_z)

        print (accel_z)
        time.sleep(0.1)
