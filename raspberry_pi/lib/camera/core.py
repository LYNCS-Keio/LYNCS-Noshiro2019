# -*- coding: utf-8 -*-
#!usr/bin/python

import os
import cv2
import numpy as np
import time
import traceback

current_dir = os.path.dirname(os.path.abspath(__file__))
class CamAnalysis:
    def __init__(self):
        pass
    
    def morphology_extract(self,stream):
        self.stream = stream
        self.stream_hsv = cv2.cvtColor(self.stream, cv2.COLOR_BGR2HSV)
        # Target Finder
        UPPER_THRESHOLD = (220, 255, 255)
        LOWER_THRESHOLD = (140, 40, 40)
        self.mask = cv2.inRange(self.stream_hsv, LOWER_THRESHOLD, UPPER_THRESHOLD)
        # Remove Noises
        kernel = np.ones((9, 9))
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, kernel)
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_CLOSE, kernel)
        
    def contour_find(self):
        contours = cv2.findContours(self.mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        if len(contours) == 0:
            print("-1")
        else:
            areas = list(map(lambda contour: cv2.contourArea(contour), contours))
            max_area_index = areas.index(max(areas))
            #    #max_area_contour = contours[max_area_index]
            #    # Find center of gravity
            m = cv2.moments(contours[max_area_index])
            x, y = (m['m10'] / m['m00']), (m['m01'] / m['m00'])
            cv2.drawContours(self.stream, contours, -1, (255, 255, 255), 2)
            cv2.circle(self.stream, (int(x), int(y)), 30, (0, 255, 0), 2)
            return [x,y]
            
    def save_all_outputs(self):
        cv2.imwrite(current_dir + '/bgr2hsv.png', self.stream_hsv)
        cv2.imwrite(current_dir + '/morpho.png', self.mask)
        cv2.imwrite(current_dir + '/contour.png', self.stream)


if __name__ == '__main__':
    try:
            stream = cv2.imread(current_dir + '/sample.png', 1)
            cam = CamAnalysis()
            cam.morphology_extract(stream)
            coord = cam.contour_find()
            cam.save_all_outputs()
            print(coord)
    except:
        traceback.print_exc()
