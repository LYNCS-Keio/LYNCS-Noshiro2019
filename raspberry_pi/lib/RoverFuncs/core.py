_height_high = 40       ## when the rover pass this height, it will be interpretted as reached the top.
_height_low = 3         ## when the rover pass this height, it will sparate the parachute.
_release_timeout =120   ## 
_limit_bme = 10         ## 

__all__ = ['BME_Judge']

class BME_Judge():
    def __init__(self):
        self.reach_top = False  ## 頂上に到達したかどうかのフラグ
        self.count_bme_t = 0    ## 頂上に到達したかどうかのカウンタ
        
        self.reach_gnd = False  ## 地上付近に到達したかどうかのフラグ
        self.count_bme_g = 0    ## 地上付近に到達したかどうかのカウンタ
        
    def height_high(self):
        return _height_high
    def height_low(self):
        return _height_low
    def limit_bme(self):
        return _limit_bme
    
    def is_reached_top(self,height):
        if not self.reach_top:
            ## _height_highが_limit_bme回以上続くと頂上であると判定する.
            if height >= _height_high:
                self.count_bme_t += 1
            else:
                self.count_bme_t = 0
            if self.count_bme_t >= _limit_bme:
                self.reach_top = True
        return self.reach_top
    
    def is_reached_gnd(self,height):
        if not self.reach_gnd:
            ## _height_highが_limit_bme回以上続くと地上であると判定する.
            if height <= _height_low:
                self.count_bme_l +=1
            else:
                self.count_bme_t = 0
            if self.count_bme_t >= limit_bme:
                self.reach_gnd = True
        return self.reach_gnd
        
    def __del__(self):
        pass
