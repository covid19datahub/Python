<a href="https://covid19datahub.io"><img src="https://storage.covid19datahub.io/logo.svg" align="right" height="128"/></a>

# Python Interface to COVID-19 Data Hub

Python package [covid19dh](https://covid19datahub.io/) provides access to COVID-19 data from unified data hub.

It is part of *COVID-19 Data Hub* project.

## Setup and usage

Install from [pip](https://pypi.org/project/covid19dh/) with

```python
pip install covid19dh
```

Importing main `covid19()` function with 

```python
from covid19dh import covid19

x = covid19("ITA") # load data
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19dh
```

## Parametrization

### Country

Country specifies an administrative region, that the data are fetched from.
This is connected with source data comes from. It can be given as
ISO3, ISO2, numeric ISO or country name (case-insensitively). 

Fetching data from a particular country is done with

```python
x = covid19("ESP")
```

List of ISO codes can be found [here](https://github.com/covid19datahub/COVID19/blob/master/inst/extdata/src.csv).

Filter can also specify multiple countries at the same time

```python
x = covid19(["ESP","PT","andorra",250])
```

Country can be omitted, then whole world data is used.

```python
x = covid19()
```

### Date filter

Date can be specified with `datetime.datetime`, `datetime.date`
or as a `str` in format `YYYY-mm-dd`.

```python
from datetime import datetime

x = covid19("SWE", start = datetime(2020,4,1), end = "2020-05-01")
```

### Level

Levels work the same way as in all the other our data fetchers.

1. Country level
2. State, region or canton level
3. City or municipality level

```python
from datetime import date

x = covid19("USA", level = 2, start = date(2020,5,1))
```

### Cache

Library keeps downloaded data in simple way during runtime. By default, using the cached data is enabled.

Caching can be disabled (e.g. for long running programs) by

```python
x = covid19("FRA", cache=False)
```

### Citations

Dataset [citations](https://github.com/covid19datahub/COVID19/blob/master/inst/extdata/src.csv) are printed by default on `stdout`.

``` python
from covid19dh import covid19
x = covid19("CZE") 
```

```
Czech Statistical Office (2018), https://www.czso.cz/csu/czso/demograficka-rocenka-kraju-2009-az-2018

Johns Hopkins Center for Systems Science and Engineering (2020), https://github.com/CSSEGISandData/COVID-19

Ministery of Health of Czech Republic (2020), https://onemocneni-aktualne.mzcr.cz/

Our World in Data (2020), https://github.com/owid/covid-19-data

Hale Thomas, Sam Webster, Anna Petherick, Toby Phillips, and Beatriz Kira (2020). Oxford COVID-19 Government Response Tracker, Blavatnik School of Government.

World Bank Open Data (2018), https://data.worldbank.org/indicator/SP.POP.TOTL

Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Working paper, doi: 10.13140/RG.2.2.11649.81763.
```

This feature can be turned off by setting `verbose` to `False`.

```python
from covid19dh import covid19
x = covid19("CZE", verbose = False) 
```

You can separately get the reference data or the string citations as

```python
from covid19dh import covid19,cite
x = covid19("ITA")
refs = cite(x, raw=True)
citations = cite(x)
```

Pandas dataframe `refs` has following structure

```
                                               title                                             author  year                     institution  ... bibtype iso_alpha_3 administrative_area_level  data_type
0                           Czech Statistical Office                                                     2018                                  ...                   1                         1          1
1  Johns Hopkins Center for Systems Science and E...                                                     2020                                  ...                   5                         5          5
2              Ministery of Health of Czech Republic                                                     2020                                  ...                   2                         2          2
3                                  Our World in Data                                                     2020                                  ...                   1                         1          1
4        Oxford COVID-19 Government Response Tracker  Hale Thomas, Sam Webster, Anna Petherick, Toby...  2020  Blavatnik School of Government  ...                  10                        10         10
5                               World Bank Open Data                                                     2018                                  ...                   1                         1          1

[6 rows x 10 columns]
```

List `citations` is equal to

```python
[
    'Czech Statistical Office (2018), https://www.czso.cz/csu/czso/demograficka-rocenka-kraju-2009-az-2018',
    'Johns Hopkins Center for Systems Science and Engineering (2020), https://github.com/CSSEGISandData/COVID-19',
    'Ministery of Health of Czech Republic (2020), https://onemocneni-aktualne.mzcr.cz/',
    'Our World in Data (2020), https://github.com/owid/covid-19-data',
    'Hale Thomas, Sam Webster, Anna Petherick, Toby Phillips, and Beatriz Kira (2020). Oxford COVID-19 Government Response Tracker, Blavatnik School of Government.',
    'World Bank Open Data (2018), https://data.worldbank.org/indicator/SP.POP.TOTL',
    'Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Working paper, doi: 10.13140/RG.2.2.11649.81763.'
]
```



## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

The goal of [COVID-19 Data Hub](https://covid19datahub.io/) is to provide the research community with a unified data hub by collecting worldwide fine-grained case data, merged with exogenous variables helpful for a better understanding of COVID-19.

Join us on [GitHub](https://github.com/covid19datahub/Python).



