import time
from lib import HCSR04

with HCSR04.HCSR04(19, 26) as hcs:
    while True:
        print(hcs.readData(34300))
        height = hcs.readData(34300)
        print(height)