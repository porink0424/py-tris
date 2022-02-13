# 時間計測に利用するモジュール
# 
# 使い方の例:
# 
# a = Timer()
# 
# 時間を計測したい処理
# 
# print(a.Stop())
#

import time

class Timer:
    def __init__ (self):
        self.start = time.perf_counter()
    
    def Stop (self):
        return time.perf_counter() - self.start