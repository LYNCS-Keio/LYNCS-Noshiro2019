# -*- coding: utf-8 -*-
#!usr/bin/python

import picamera
import time
import os
import io
import numpy
import cv2

__all__=['capture']

current_dir = os.path.dirname(os.path.abspath(__file__))
class capture:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.start_preview()
        self.stream = io.BytesIO()
    
    def cap(self):
        self.camera.capture(self.stream, 'bgr')
        return self.stream

    def flush(self):
        cv2.imwrite(current_dir + 'capture.png', self.streams)

    def __del__(self):
        self.camera.stop_preview()
        self.camera.close()

if __name__ == '__main__':
    ca = capture()
    time.sleep(2)
    ca.cap()
    ca.flush()
    del ca
