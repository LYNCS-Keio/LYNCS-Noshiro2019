# -*- coding: utf-8 -*-
from lib import camera as cam_analy
from lib import servo
import picamera

with servo(13) as svl, servo(18) as svr: