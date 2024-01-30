
import datetime
from io import StringIO, BytesIO
import math
import sys
import warnings
import zipfile

import pandas as pd
import requests

from ._cite import get_sources, cite
from ._cache import *


def get_url(level, dt, raw, vintage):
    # dataname
    rawprefix = "raw" if raw else ""
    dataname = f"{rawprefix}data-{level}"
    # vintage
    if vintage:
        # too new
        if dt >= datetime.datetime.now() - datetime.timedelta(days=2):
            warnings.warn("vintage data not available yet", category=ResourceWarning)
            return None, None
        dt_str = dt.strftime("%Y-%m-%d")
        filename = f"{dt_str}.zip"
    # current data
    else:
        filename = f"{dataname}.zip"
    # url, filename
    return f"https://storage.covid19datahub.io/{filename}", f"{dataname}.csv"


def parseDate(dt):
    if isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)
    if isinstance(dt, str):
        try:
            return datetime.datetime.strptime(dt, "%Y-%m-%d")
        except Exception:
            print("Invalid time format.", file=sys.stderr)
            raise
    return dt


def covid19(country=None,
            level=1,
            start=datetime.date(2019, 1, 1),
            end=None,  # defaultly today
            cache=True,
            verbose=True,
            raw=True,
            vintage=False):
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
        verbose (bool, optional): prints sources, default true
        raw (bool, optional): download not cleansed data, defaultly using cleansed
        vintage (bool, optional): use hub data (True) or original source, not available in Python covid19dh (only hub)
    """
    # parse arguments
    if country is not None:
        country = [country] if isinstance(country, str) else country
        country = [c.upper() if isinstance(c,str) else c for c in country]
    end = datetime.datetime.now() if end is None else end
    try:
        end = parseDate(end)
        start = parseDate(start)
    except Exception:
        return None, None
    if level not in {1, 2, 3}:
        warnings.warn("valid options for 'level' are:\n\t1: country-level data\n\t2: state-level data\n\t3: city-level data")
        return None, None
    if start > end:
        warnings.warn("start is later than end")
        return None, None

    # cache
    df = read_cache(level, end, raw, vintage)
    src = None

    if cache is False or df is None:
        # get url from level
        try:
            url, filename = get_url(level=level, dt=end, raw=raw, vintage=vintage)
            if url is None:
                return None, None
        except KeyError:
            warnings.warn("invalid level")
            return None, None
        # download
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except Exception:
            if vintage:
                warnings.warn("vintage data not available yet")
                return None, None
            else:
                warnings.warn("error to fetch data")
                return None, None
        # parse
        with zipfile.ZipFile(BytesIO(response.content)) as zz:
            with zz.open(filename) as fd:
                df = pd.read_csv(fd, low_memory=False)
            # src from vintage archive
            if vintage:
                with zz.open("src.csv") as fd:
                    src = pd.read_csv(fd, low_memory=False)
                    write_src_cache(src, end, vintage)
        # cast columns
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        try:
            df['iso_numeric'] = df['iso_numeric'].apply(lambda x: float(x))
        except Exception:
            pass

        write_cache(df, level, end, raw, vintage)

    # src
    if src is None:
        src = read_src_cache(end, vintage)
        if src is None:
            src = get_sources()
            write_src_cache(src, end, vintage)

    # filter
    if country is not None:
        # elementwise comparison works, but throws warning that it will be working better in the future
        # no idea why, but I found solution to mute it as follows
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)

            country_filter = df['administrative_area_level_1'].map(lambda s: s.upper()).isin(country)
            for feature in ["iso_alpha_2","iso_alpha_3","iso_numeric"]:
                try:
                    country_filter = country_filter | df[feature].isin(country)
                except KeyError:
                    pass
            df = df[country_filter]

            #df = df[(df['iso_alpha_3'].isin(country)) |
            #        (df['iso_alpha_2'].isin(country)) |
            #        (df['iso_numeric'].isin(country)) |
            #        (df['administrative_area_level_1'].map(lambda s: s.upper()).isin(country))  ]
    if start is not None:
        df = df[df['date'] >= start]
    if end is not None:
        df = df[df['date'] <= end]

    # detect empty
    if df.empty:
        warnings.warn("no data for given settings", category=ResourceWarning)
        return None, None
    # sort
    df = df.sort_values(by=["id","date"])

    # cite
    src = cite(x=df, sources=src, verbose=False)

    if verbose:
        # construct message
        message = "We have invested a lot of time and effort in creating COVID-19 Data Hub, please cite the following when using it:\n\n"
        message += "\t\033[1mGuidotti, E., Ardia, D., (2020), \"COVID-19 Data Hub\", Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.\033[0m\n\n"
        message += "A BibTeX entry for LaTeX users is\n\n"
        message += "\t@Article{,\n"
        message += "\t\ttitle = {COVID-19 Data Hub},\n"
        message += "\t\tyear = {2020},\n"
        message += "\t\tdoi = {10.21105/joss.02376},\n"
        message += "\t\tauthor = {Emanuele Guidotti and David Ardia},\n"
        message += "\t\tjournal = {Journal of Open Source Software},\n"
        message += "\t\tvolume = {5},\n"
        message += "\t\tnumber = {51},\n"
        message += "\t\tpages = {2376},\n"
        message += "\t}\n\n"
        message += "\033[33mTo hide this message use 'verbose = False'.\033[0m"
        # print
        print(message)

    return df, src



__all__ = ["covid19"]