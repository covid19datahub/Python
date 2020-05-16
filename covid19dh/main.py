
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
            # TODO
            raw     = False,
            vintage = False,
            cache   = True):
    # parse arguments
    country = country.upper() if country is not None else None
    end = datetime.datetime.now() if end is None else end
    try:
        end = parseDate(end)
        start = parseDate(start)
    except:
        return None
    if level not in {1,2,3}:
        print("valid options for 'level' are:\n\t1: country-level data\n\t2: state-level data\n\t3: city-level data")
        return None
    
    # cache
    if cache is True and cached[level] is not None:
        print("Using cached data.")
        df = cached[level]
    else:
        # get url from level
        try:
            url = URLs[level]
            filename = files[level]
        except KeyError:
            print("Invalid level.", file=sys.stderr)
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
            df = df[(df['iso_alpha_3'] == country) |
                    (df['iso_alpha_2'] == country) |
                    (df['iso_numeric'] == country)   ]
    if start is not None:
        df = df[df['date'] >= start]
    if end is not None:
        df = df[df['date'] <= end]
    
    return df

__all__ = ["covid19"]