# -*- coding: utf-8 -*-
import unittest
from lib import RoverFuncs

class TestBMEJudge(unittest.TestCase):
    def test_in_case_not_at_the_top(self):
        bme_judge = RoverFuncs.BME_Judge()
        reached_flag = False
        for i in range(bme_judge.limit_bme()):
            reached_flag = bme_judge.is_reached_top(bme_judge.height_high() - 1)
        self.assertTrue(not reached_flag)
    
    def test_in_case_at_the_top(self):
        bme_judge = RoverFuncs.BME_Judge()
        reached_flag = False
        for i in range(bme_judge.limit_bme()):
            reached_flag = bme_judge.is_reached_top(bme_judge.height_high() - 1)
        for i in range(bme_judge.limit_bme()):
            reached_flag = bme_judge.is_reached_top(bme_judge.height_high())
        self.assertTrue(reached_flag)

if __name__ == "__main__":
    unittest.main()