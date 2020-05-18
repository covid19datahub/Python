
import datetime
from io import StringIO,BytesIO
import sys
import warnings
import zipfile

import pandas as pd
import requests

URLs = {
    1: 'https://storage.covid19datahub.io/data-1.zip',
    2: 'https://storage.covid19datahub.io/data-2.zip',
    3: 'https://storage.covid19datahub.io/data-3.zip'
}
files = {
    1: 'data-1.csv',
    2: 'data-2.csv',
    3: 'data-3.csv'
}
cached = {
    1: None,
    2: None,
    3: None
}

def parseDate(dt):
    if isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)
    if isinstance(dt, str):
        try:
            return datetime.datetime.strptime(dt, "%Y-%m-%d")
        except:
            print("Invalid time format.", file=sys.stderr)
            raise
    return dt

def covid19(country = None,
            level   = 1,
            start   = datetime.date(2019,1,1),
            end     = None, # defaultly today
            cache   = True,
            # will not be done unless architecture changed
            raw     = False, 
            vintage = True):
    """Main function for module. Fetches data from hub.
    
    Args:
        country (str, optional): ISO country code, defaultly all countries
        level (int, optional): level of data, default 1
            * country-level (1)
            * state-level (2)
            * city-level (3)
        start (datetime | date | str, optional): start date of data (as str in format [%Y-%m-%d]),
                                                 default 2019-01-01
        end (datetime | date | str, optional): end date of data (as str in format [%Y-%m-%d]),
                                               default today (sysdate)
        cache (bool, optional): use cached data if available, default yes
        raw (bool, optional): do not perform cleansing, not available in Python covid19dh (precleansed data used)
        vintage (bool, optional): use hub data (True) or original source, not available in Python covid19dh (only hub)
    """
    # parse arguments
    if country is not None:
        country = [country] if isinstance(country, str) else country
        country = [c.upper() for c in country]
    end = datetime.datetime.now() if end is None else end
    try:
        end = parseDate(end)
        start = parseDate(start)
    except:
        return None
    if level not in {1,2,3}:
        warnings.warn("valid options for 'level' are:\n\t1: country-level data\n\t2: state-level data\n\t3: city-level data")
        return None
    if start > end:
        warnings.warn("start is later than end")
        return None
    if raw:
        warnings.warn("raw data not available for covid19dh, fetching precleaned vintage", category=ResourceWarning)
    if not vintage:
        warnings.warn("only vintage data available for covid19dh, fetching vintage", category=ResourceWarning)
    
    # cache
    if cache is True and cached[level] is not None:
        df = cached[level]
    else:
        # get url from level
        try:
            url = URLs[level]
            filename = files[level]
        except KeyError:
            warnings.warn("invalid level")
            return None
        # download
        response = requests.get(url)
        # parse
        with zipfile.ZipFile( BytesIO(response.content) ) as zz:
            with zz.open(filename) as fd:
                df = pd.read_csv( fd, low_memory = False)
        # cast columns
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

        cached[level] = df

    # filter
    if country is not None:
        # elementwise comparison works, but throws warning that it will be working better in the future
        # no idea why, but I found solution to mute it as follows
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            df = df[(df['iso_alpha_3'].isin(country)) |
                    (df['iso_alpha_2'].isin(country)) |
                    (df['iso_numeric'].isin(country)) |
                    (df['administrative_area_level_1'].map(lambda s: s.upper()).isin(country))  ]
    if start is not None:
        df = df[df['date'] >= start]
    if end is not None:
        df = df[df['date'] <= end]
    
    # detect empty
    if df.empty:
        warnings.warn("no data for given settings", category=ResourceWarning)
        return None
    # sort
    df = df.sort_values(by="date")
    
    return df

__all__ = ["covid19"]