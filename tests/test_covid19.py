
from datetime import datetime,timedelta
import unittest

import pandas as pd

import covid19dh

class TestCovid19(unittest.TestCase):
    def test_main_all(self):
        # fetch
        x,src = covid19dh.covid19(level = 2, verbose = False)
        # test
        self.assertIsInstance(x, pd.DataFrame)
        for col in ["id","date","tests","confirmed","recovered","deaths","hosp","vent","icu"]:
            self.assertIn(col, x.columns)
    def test_vintage(self):
        # fetch
        _,src1 = covid19dh.covid19("DE", verbose = False, vintage = True, end = datetime(2020,7,10))
        _,src2 = covid19dh.covid19("DE", verbose = False, vintage = True, end = datetime(2020,7,20))
        
        
        
        
            
            
            

__all__ = ["TestCovid19"]