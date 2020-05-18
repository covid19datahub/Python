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

## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

The goal of [COVID-19 Data Hub](https://covid19datahub.io/) is to provide the research community with a unified data hub by collecting worldwide fine-grained case data, merged with exogenous variables helpful for a better understanding of COVID-19.

Join us on [GitHub](https://github.com/covid19datahub/Python).



