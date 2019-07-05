from lib import BME280 as BME
from lib import HCSR04 as HCSR
from lib import MPU6050 as MPU
import time
time_range=5 #加速度が落ち着いている判定判定時間
break_time=30 #キャリア判定からの経過時間による着陸判定用
extent=0.02 #MPUの誤差込みの判定にするための変数

#キャリア判定
now_t = time()
height = BME.readData()

while height>5: #meter
    height = BME.readData()

while height>200:
    height = HCSR.readData()

#パラ分離
#着陸判定

while time()-_time <= time_range :
    a_x,a_y,a_z = MPU.get_accel_data_lsb()
    accel=((a_x-a_y)**2+(a_y-a_z)**2+(a_z-a_x)**2)**0.5
    if 1+extent > accel and accel > 1-extent :
        if flag == 0:
            flag=1
            _time=time()
    else:
        flag=0
        _time=0

    if time()-now_t > break_time :
        break
