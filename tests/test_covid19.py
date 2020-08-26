
from datetime import datetime,timedelta
import unittest

import pandas as pd

import covid19dh

class TestCovid19(unittest.TestCase):
    def _covid19(self, *args, **kw):
        x,src = covid19dh.covid19(*args, **kw, verbose = False) # fetch
        # test
        self.assertIsInstance(x, pd.DataFrame)
        for col in ["id","date","tests","confirmed","recovered","deaths","hosp","vent","icu"]:
            self.assertIn(col, x.columns)
        return x,src
    def test_default(self):
        print("default")
        x,src = self._covid19() # fetch
    def test_level1(self):
        print("level1")
        x,src = self._covid19(level = 1) # fetch
    def test_level2(self):
        print("level2")
        x,src = self._covid19(level = 2) # fetch
    def test_level3(self):
        print("level3")
        x,src = self._covid19(level = 3) # fetch
    
    def test_vintage(self):
        print("vintage")
        # fetch
        _,src1 = self._covid19("DE", vintage = True, end = datetime(2020,7,10))
        _,src2 = self._covid19("DE", vintage = True, end = datetime(2020,7,20))
        
        
        
        
            
            
            

__all__ = ["TestCovid19"]