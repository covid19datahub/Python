
from datetime import datetime,timedelta
import unittest

import pandas as pd

from covid19dh import covid19


class TestMain(unittest.TestCase):
    def test_main_all(self):
        # fetch
        x = covid19(verbose = False, vintage = True, end = datetime.today() - timedelta(days = 8))
        # test
        self.assertIsInstance(x, pd.DataFrame)
        for col in ["id","date","tests","confirmed","recovered","deaths","hosp","vent","icu"]:
            self.assertIn(col, x.columns)
        
        
        
        
            
            
            

__all__ = ["TestMain"]