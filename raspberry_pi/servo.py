import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)

def servo_pulse(h):
    
    servo.start(h/20000)
    time.sleep(0.5)
    servo.stop()

GPIO.cleanup()