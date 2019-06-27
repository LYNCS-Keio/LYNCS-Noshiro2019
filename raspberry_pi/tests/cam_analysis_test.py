# -*- coding: utf-8 -*-
import unittest
import cv2
from lib import camera


class TestCamAnalysis(unittest.TestCase):
    def test_(self):
        stream = cv2.imread('lib/camera/sample.png', 1)
        cam = camera.CamAnalysis()
        cam.morphology_extract(stream)
        coord = cam.contour_find()
        self.assertTrue((500 < coord[0] and coord[0] < 750) and (100 < coord[1] and coord[1] < 300))


if __name__ == "__main__":
    unittest.main()