from lib import MPU6050
import time
rotation_angle = 0
def cal_rotation_angle(preT,p_g):
    nowT = time.time()
    now_gyro = MPU.get_gyro_data_lsb()[2]
    now_rotation_angle = (now_gyro + p_g) * (nowT - preT) / 2 - 0.775
    print("変化率:",now_rotation_angle/(nowT - preT))
    return [nowT, now_gyro, now_rotation_angle]

MPU = MPU6050.MPU6050(0x68)
preT = time.time()
pre_gyro = MPU.get_gyro_data_lsb()[2]

while 1:
    preT, pre_gyro , now_rotation_angle = cal_rotation_angle(preT, pre_gyro)
    rotation_angle += now_rotation_angle
    print("rotation_angle:" , rotation_angle)
    time.sleep(0.5)
