import time
from lib import servo

with servo.servo(18) as sv:
    while True:
        sv.rotate(7.5)
        time.sleep(1)
        sv.rotate(9)
        time.sleep(1)