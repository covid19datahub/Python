
from datetime import datetime,timedelta
import unittest

import pandas as pd

import covid19dh

class TestCovid19Latest(unittest.TestCase):
    _sourceless_attributes = [
        'id', 'key_google_mobility', 'key_apple_mobility', 'date',
        'iso_numeric', 'iso_alpha_2', 'iso_alpha_3',
        'administrative_area_level', 'administrative_area_level_3',
        'administrative_area_level_2', 'administrative_area_level_1',
        'gatherings_restrictions', 'stay_home_restrictions', 'iso_currency',
        #
        'people_fully_vaccinated', 'people_vaccinated',
        'vaccination_policy', 'elderly_people_protection', 'facial_coverings',
        'containment_health_index', 'economic_support_index',
        'government_response_index',
    ]
    _numeric_attributes = [
        "tests", "confirmed", "recovered", "deaths", "hosp", "vent", "icu",
    ]
    _constant_attributes = ["population", "latitude", "longitude"]
    _indicator_attributes = [
        "school_closing", "cancel_events", "contact_tracing", "testing_policy",
        "transport_closing", "workplace_closing", "information_campaigns",
        "stringency_index", "international_movement_restrictions",
        "internal_movement_restrictions",
    ]
    _index_attributes = [

    ]
    _src_attributes = [
        "iso_alpha_3", "administrative_area_level", "data_type", "url",
        "title", "year", "bibtype", "author", "institution", "textVersion",
    ]

    def _covid19(self, *args, **kw):
        x, src = covid19dh.covid19(*args, **kw, verbose=False)  # fetch
        # test
        self.assertIsInstance(x, pd.DataFrame)
        cols = (
            set(self._numeric_attributes) |
            set(self._constant_attributes) |
            set(self._sourceless_attributes) |
            set(self._indicator_attributes) |
            set(self._index_attributes)
        )
        for col in cols:
            self.assertIn(col, x.columns)
        return x, src

    def _check_level1(self, x):
        self.assertTrue((x.administrative_area_level == 1).all())
        self.assertTrue(not x.administrative_area_level_1.isnull().any())
        self.assertTrue(x.administrative_area_level_2.isnull().all())
        self.assertTrue(x.administrative_area_level_3.isnull().all())

    def _check_level2(self, x):
        self.assertTrue((x.administrative_area_level == 2).all())
        self.assertTrue(not x.administrative_area_level_1.isnull().any())
        self.assertTrue(not x.administrative_area_level_2.isnull().any())
        self.assertTrue(x.administrative_area_level_3.isnull().all())

    def _check_level3(self, x):
        self.assertTrue((x.administrative_area_level == 3).all())
        self.assertTrue(not x.administrative_area_level_1.isnull().any())
        # self.assertTrue(not x.administrative_area_level_2.isnull().any()) # e.g. Colombia have only levels 1,3
        self.assertTrue(not x.administrative_area_level_3.isnull().any())

    def _check_src(self, x, src):
        # format
        for col in self._src_attributes:
            self.assertIn(col, src.columns)
        # all data types
        data_types = src.data_type.unique()
        # all cols
        cols = set(x.columns) - set(self._sourceless_attributes)
        cols -= set([  # adjust
            'key_alpha_2', 'key_numeric', 'key_jhu_csse',
            'key_nuts', 'key_local', 'key_gadm',
        ])
        for col in cols:
            # empty columns ignored
            if x[col].isnull().all() or (x[col] == 0).all():
                continue

            self.assertIn(col, data_types)  # col in sources

    def test_default(self):
        x, src = self._covid19()  # fetch
        self._check_level1(x)
        self._check_src(x, src)

    def test_level1(self):
        x, src = self._covid19(level=1)  # fetch
        self._check_level1(x)
        self._check_src(x, src)

    def test_level2(self):
        x, src = self._covid19(level=2)  # fetch
        self._check_level2(x)
        self._check_src(x, src)

    # def test_level3(self):
    #     x, src = self._covid19('SE', level=3, start='2023-01-01')  # fetch
    #     self._check_level3(x)
    #     self._check_src(x, src)


__all__ = ["TestCovid19Latest"]
