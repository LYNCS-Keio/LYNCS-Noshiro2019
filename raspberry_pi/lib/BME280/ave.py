# -*- coding: utf-8 -*-

import core
import time

index = 1
pressure_sum = 0

try:
    while True:
        index += 1
        pressure_sum += core.readData()
        time.sleep(0.001)

finally:
    print(pressure_sum / index)
