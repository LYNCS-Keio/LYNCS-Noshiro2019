__all__ = [median_filter]

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


if __name__ == "__main__":
    med = median_filter()
    med.input_data([4,7,3,1,5,9,2,8,6,10]) # 1 2 3 4 5 6 7 8 9 10
    print(med.get_data())
    pass
