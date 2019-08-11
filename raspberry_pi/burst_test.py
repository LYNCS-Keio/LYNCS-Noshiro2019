from lib import camera 
from lib import capture
import time

try:
    cap = capture.capture()
    cam = camera.CamAnalysis()
    time.sleep(2)
    while True:
        stream = cap.cap()
        cam.morphology_extract(stream)
        coord = cam.contour_find()
        cam.save_all_outputs()
        row = [time.time()]
        row.extend(coord)
        print(row)

finally:
    del cap