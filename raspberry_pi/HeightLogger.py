from lib import HCSR04
from lib import BME280 as BME
import time
import csv
import os
import RPi.GPIO as GPIO
current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

DMUX_pin=[11,9,10]
DMUX_out = [1, 0, 0]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DMUX_pin[0], GPIO.OUT)
GPIO.setup(DMUX_pin[1], GPIO.OUT)
GPIO.setup(DMUX_pin[2], GPIO.OUT)

GPIO.output(DMUX_pin[0], DMUX_out[0])
GPIO.output(DMUX_pin[1], DMUX_out[1])
GPIO.output(DMUX_pin[2], DMUX_out[2])

class servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.srv = GPIO.PWM(self.pin, 50)
        self.srv.start(7.5)

    def __enter__(self):
        return self

    def rotate(self, duty):
        self.srv.ChangeDutyCycle(duty)

    def stop(self):
        self.srv.stop()

    def __del__(self):
        self.srv.stop()

    def __exit__(self, exception_type, exception_value, traceback):
        pass

svP = servo(12)
index = 0
filename = 'hlog' + '%04d' % index
while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
    index += 1
    filename = 'hlog' + '%04d' % index

try:
    with open(current_dir + '/' + filename + '.csv', 'w') as c:
        f = csv.writer(c, lineterminator='\n')
        with HCSR04.HCSR04(19, 26) as hcs:
            svP.rotate(7.8)
            time.sleep(0.2)
            while 1:
                height_hcs = [hcs.readData(34300)]
                height_BME = BME.readData()
                row = [time.time()]
                row.extend(height_hcs)
                row.extend(height_BME)
                f.writerow(row)
                time.sleep(0.01)
except:
    pass
finally:
    svP.rotate(7.2)
    time.sleep(0.5)
    svP.stop()
    print("final!l!!)
    GPIO.cleanup()
