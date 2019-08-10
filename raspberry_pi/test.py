import time
import RPi.GPIO as GPIO
import pigpio

GPIO.setmode(GPIO.BCM)
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=12 #マルチプレクサ側PWMのピン
for pin in range(0,2):
    GPIO.setup(pinDMUX[pin],GPIO.OUT)
    GPIO.output(pinDMUX[pin],DMUX_out[pin]) #分離サーボの出力指定
pi = pigpio.pi()
pi.set_mode(12,pigpio.OUTPUT)

#for x in range(0,10):
y = 71000 #- x*0.05
pi.hardware_PWM(12, 50, y)
time.sleep(1)

y = 60000#- x*0.05
pi.hardware_PWM(12, 50, y)
time.sleep(1)

time.sleep(3)
GPIO.cleanup()
pi.stop()
