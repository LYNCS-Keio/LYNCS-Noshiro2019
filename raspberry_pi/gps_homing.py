from lib import rover_gps as GPS
from lib import servo
from lib import MPU6050 as MPU
import math
import time
import queue

#画像誘導に切り替える距離(km)
cam_dis = 0.01

dutyL = 9.0
dutyR = 9.0

#PID
M = 0.00 
M1 =  0.00 
goal = 0.00  
e = 0.00 
e1 = 0.00 
e2 = 0.00 
Kp = 0.1 
Ki = 0.1 
Kd = 0.1

#goalの座標
#goal_lat =
#goal_lng = 

#位置座標を保存
position_memo = queue.Queue()

#回転角度
def cal_rotation_angle(preT,pre_gyro):
    nowT = time.time()　#現在時刻
    now_gyro = MPU.get_gyro_data_lsb()[2] #現在の角速度

    #積分して回転角度を求める
    now_rotation_angle = (now_gyro + pre_gyro) * (nowT - preT) / 2
    return [nowT, now_gyro, now_rotation_angle]

def cal_average(x):
    sum = 0
    for i range(5):
        sum += x[i]
    return sum / 5

#着地
pre = [None, None]
while pre is None:
    pre = GPS.lat_long_measurement()

#5回座標が取れるまで進む
with servo(pinL) as svL, servo(pinR) as svR:
    svL.rotate(dutyL)
    svR.rotate(dutyR)

for i in range(5):
    now = [None, None]
    while now is None:
        now = GPS.lat_long_measurement()
    position_memo.put(GPS.convert_lat_long_to_r_theta(pre[0], pre[1], now[0], now[1]))
    pre = now

#現在の方位角
now_azimuth = cal_average(position_memo)
#回転角度
rotation_angle = now_azimuth

#goalまでの距離と方位角
to_goal = [None, None]
while (to_goal[0] is None) or (to_goal[1] is None)
    to_goal = GPS.r_theta_to_goal(goal_lat, goal_long)

#goal方角と進んでいる方角の差
difference = to_goal[1]    

#goalとの距離が10m以下になったら画像での誘導
while to_goal[0] > cam_dis:
    
    now = [None, None]
    now = GPS.lat_long_measurement()
    if now[0] != None or now[1] != None:

        position_memo.get()
        position_memo.put(GPS.convert_lat_long_to_r_theta(pre[0], pre[1], now[0], now[1]))

        pre = now

        #現在向いている方角
        #azimuth（方位角）
        now_azimuth = cal_average(position_memo)
        #回転角度
        rotation_angle = now_azimuth

    else:
        #回転
        preT = time.time()
        pre_gyro = math.radians(MPU.get_gyro_data_lsb()[2]) #degree to radian

        preT, pre_gyro, now_rotation_angle = cal_rotation_angle(preT, pre_gyro)
        rotation_angle += now_rotation_angle

    #goalまでの距離と方位角
    to_goal = GPS.r_theta_to_goal(goal_lat, goal_long)
    #goal方角と進んでいる方角のずれ
    difference = to_goal[1] - rotation_angle 

    #dutyLを変える
    M1 = M
    e1 = e
    e2 = e1
    e = goal - M
    M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
    
    if difference < math.pi and difference > -math.pi:
        zenshin = 1
    else:
        zenshin = 0

    if M > 1:
        M = 1
    if M < -1:
        M = -1

    dutyL = 7.5 + 2.5*((zenshin + M) / 2)
    dutyR = 7.5 + 2.5*((zenshin - M) / 2)
    
    with servo(pinL) as svL, servo(pinR) as svR:
        svL.rotate(dutyL)
        svR.rotate(dutyR)