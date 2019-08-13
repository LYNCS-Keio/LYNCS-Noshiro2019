# -*- coding: utf-8 -*- 
from lib import BME280 as BME

class median_filter:
    """
    メジアンフィルター
    """
    def __init__(self):
        pass
    
    def input_data(self,list):
        """
        フィルターしたいリスト型変数を入力する。
        Returns
        -------
        なし
        """
        self.list_ = sorted(list)
        self.size = len(list)
        
    def get_data(self):
        """
        フィルターの結果を出力する。
        Returns
        -------
        フィルターの結果
        """
        return float((self.list_[self.size/2] + self.list_[self.size/2 - 1]))/2


try:
    data = []
    while 1:
        bmedata = BME.readData()
        print(bmedata)
        data += [bmedata[1]]

finally:
    med = median_filter()
    med.input_data()
    print(med.get_data())
