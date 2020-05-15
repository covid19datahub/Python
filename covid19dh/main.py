
from io import StringIO
import pandas as pd
import requests

def covid19(file="data-1.csv"):
    # download
    url = f"https://storage.covid19datahub.io/{file}"
    response = requests.get(url)
    # parse
    df = pd.read_csv( StringIO(response.text) )
    return df

__all__ = ["covid19"]