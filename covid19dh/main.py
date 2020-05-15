
import datetime
from io import StringIO,BytesIO
import sys
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

def covid19(country = None,
            level   = 1,
            start   = datetime.date(2019,1,1),
            end     = None, # defaultly today
            raw     = False,
            vintage = False,
            verbose = True,
            cache   = True):
    # default today
    if not end:
        end = datetime.date.today()
    
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
            x = pd.read_csv( fd )
    
    
    return x

__all__ = ["covid19"]