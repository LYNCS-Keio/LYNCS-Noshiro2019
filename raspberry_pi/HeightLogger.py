from lib import HCSR04
from lib import BME280 as BME
import time
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

index = 0
filename = 'hlog' + '%04d' % index
while os.path.isfile(current_dir + '/' + filename + '.csv') == True:
    index += 1
    filename = 'hlog' + '%04d' % index

with open(current_dir + '/' + filename + '.csv', 'w') as c:
    f = csv.writer(c, lineterminator='\n')
    with HCSR04(19, 26) as hcs:
        while 1:
            height_hcs = hcs.readData()
            height_BME = BME.readData()
            row = [time.time()]
            row.extend(height_hcs)
            row.extend(height_BME)
            f.writerow(row)
            time.sleep(0.01)
