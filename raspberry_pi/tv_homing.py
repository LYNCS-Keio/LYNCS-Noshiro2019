# -*- coding: utf-8 -*-
from lib import camera
from lib import servo
from lib import capture

pinL, pinR = 13, 18

try:
    svl, svr = servo.servo(pinL), servo.servo(pinR)
    cap = capture.capture()
    cam_analy = camera.CamAnalysis()
    while True:
        cam_analy.morphology_extract(cap.cap())
        x,y = cam_analy.contour_find()
        if (x != -1)and(y != -1):
            pass
        else:
            pass

except:
    pass

finally:
    del svl, svr, cap
