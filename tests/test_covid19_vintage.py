
from datetime import datetime,timedelta
import unittest

import pandas as pd

import covid19dh

class TestCovid19Vintage(unittest.TestCase):
    def _covid19(self, *args, **kw):
        x, src = covid19dh.covid19(*args, **kw, vintage=True, verbose=False) # fetch
        # test
        self.assertIsInstance(x, pd.DataFrame)
        for col in ["id", "date", "tests", "confirmed", "recovered", "deaths", "hosp", "vent", "icu"]:
            self.assertIn(col, x.columns)
        for col in ["population", "latitude", "longitude"]:
            self.assertIn(col, x.columns)
        for col in ["school_closing", "workplace_closing", "cancel_events",
                    "gatherings_restrictions", "transport_closing", "testing_policy",
                    "stay_home_restrictions", "internal_movement_restrictions",
                    "international_movement_restrictions", "information_campaigns",
                    "contact_tracing", "stringency_index", "key", "key_apple_mobility",
                    "key_google_mobility"]:
            self.assertIn(col, x.columns)
        for col in ["iso_alpha_3", "iso_alpha_2", "iso_numeric", "currency", "administrative_area_level",
                    "administrative_area_level_1", "administrative_area_level_2", "administrative_area_level_3"]:
            self.assertIn(col, x.columns)
        return x,src

    def test_vintage(self):
        # fetch
        _, src1 = self._covid19("DE", end=datetime(2020, 7, 10))
        _, src2 = self._covid19("DE", end=datetime(2020, 7, 20))


__all__ = ["TestCovid19Vintage"]