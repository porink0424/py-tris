from typing import List

class Evalparam():
    def __init__(self, 
        EVAL_LINE_CLEAR:List[int], 
        EVAL_HEIGHT:int,
        EVAL_ROUGHNESS:int,
        EVAL_BLANK_UNDER_BLOCK:int,
        EVAL_T_SPIN_SINGLE:int,
        EVAL_T_SPIN_DOUBLE:int,
        EVAL_T_SPIN_TRIPLE:int,
        EVAL_T_SPIN_MINI_SINGLE:int,
        EVAL_T_SPIN_MINI_DOUBLE:int):
        
        self.EVAL_LINE_CLEAR = EVAL_LINE_CLEAR
        self.EVAL_HEIGHT = EVAL_HEIGHT 
        self.EVAL_ROUGHNESS = EVAL_ROUGHNESS
        self.EVAL_BLANK_UNDER_BLOCK = EVAL_BLANK_UNDER_BLOCK
        self.EVAL_T_SPIN_SINGLE = EVAL_T_SPIN_SINGLE 
        self.EVAL_T_SPIN_DOUBLE = EVAL_T_SPIN_DOUBLE
        self.EVAL_T_SPIN_TRIPLE = EVAL_T_SPIN_TRIPLE
        self.EVAL_T_SPIN_MINI_SINGLE = EVAL_T_SPIN_MINI_SINGLE
        self.EVAL_T_SPIN_MINI_DOUBLE = EVAL_T_SPIN_MINI_DOUBLE 