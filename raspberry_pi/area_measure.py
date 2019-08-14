# -*- coding: utf-8 -*-
from lib import camera
from lib import capture

cap = capture.capture()
cam = camera.CamAnalysis()
stream = cap.cap()
cam.morphology_extract(stream)
cam.save_all_outputs()
coord = cam.contour_find()

print(coord[2])
