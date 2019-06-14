# -*- coding: utf-8 -*-
import unittest
import cv2
import lib


class TestCamAnalysis(unittest.TestCase):
    def test_(self):
        stream = cv2.imread('lib/camera/sample.png', 1)
        cam = lib.CamAnalysis()
        cam.morphology_extract(stream)
        coord = cam.contour_find()
        self.assertTrue((500 < coord[0] & coord < 750) & (100 < coord[0] & coord < 300))


if __name__ == "__main__":
    unittest.main()