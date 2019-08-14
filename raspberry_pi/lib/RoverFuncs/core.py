from lib import BME280 as BME

_height_high = 40       ## when the rover pass this height, it will be interpretted as reached the top.
_height_low = 3         ## when the rover pass this height, it will sparate the parachute.
_release_timeout =120   ## 
_limit_bme = 10         ##

class BME_Judge():
    def __init__(self):
        self.reach_top = False  ## 頂上に到達したかどうかのフラグ
    def is_reached_top(height):
        if(self.reach_top == False):
            ## _height_highが_limit_bme回以上続くと頂上であると判定する.
            if height >= _height_high: 
                self.count_bme += 1
            else:
                self.count_bme = 0
            if self.count_bme >= _limit_bme:
                self.reach_top = True
        return self.reach_top
    def __del__(self):
        pass
