import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pinDMUX=[11,9,10] #マルチプレクサの出力指定ピンA,B,C
DMUX_out=[1,0,0] #出力ピン指定のHIGH,LOWデータ
pinPWM=12 #マルチプレクサ側PWMのピン
for pin in range(0,2):
    GPIO.setup(pinDMUX[pin],GPIO.OUT)
    GPIO.output(pinDMUX[pin],DMUX_out[pin]) #分離サーボの出力指定
GPIO.setup(12,GPIO.OUT)
sv = GPIO.PWM(pinPWM, 50)
sv.start(7.1)
time.sleep(0.5)
for x in range(1,10):
    y = 7.1 - x*0.05
    sv.ChangeDutyCycle(y)
    time.sleep(0.1)

sv.stop()
time.sleep(1)
GPIO.cleanup()
