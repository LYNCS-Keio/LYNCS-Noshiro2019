import time
import RPi.GPIO as GPIO
import pigpio

GPIO.setmode(GPIO.BCM)
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[0,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=12 #マルチプレクサ側PWMのピン
for pin in range(0,2):
    GPIO.setup(pinDMUX[pin],GPIO.OUT)
    GPIO.output(pinDMUX[pin],DMUX_out[pin]) #分離サーボの出力指定
pi = pigpio.pi()
pi.set_mode(12,pigpio.OUTPUT)
pi.set_mode(13,pigpio.OUTPUT)
#for x in range(0,10):
y1 = 90000 #- x*0.05
y2 = 60000
pi.hardware_PWM(13, 50, y1)
pi.hardware_PWM(12, 50, y2)
time.sleep(30)


y = 75000#- x*0.05
pi.hardware_PWM(12, 50, y)
pi.hardware_PWM(13, 50, y)
time.sleep(3)

GPIO.cleanup()
pi.hardware_PWM(12, 0, 0)
pi.hardware_PWM(13, 0, 0)
pi.stop()
