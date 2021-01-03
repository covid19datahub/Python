<a href="https://covid19datahub.io"><img src="https://storage.covid19datahub.io/logo.svg" align="right" height="128"/></a>

# Python Interface to COVID-19 Data Hub

[![](https://img.shields.io/pypi/v/covid19dh.svg?color=brightgreen)](https://pypi.org/pypi/covid19dh/) [![](https://img.shields.io/pypi/dm/covid19dh.svg?color=blue)](https://pypi.org/pypi/covid19dh/) [![DOI](https://joss.theoj.org/papers/10.21105/joss.02376/status.svg)](https://doi.org/10.21105/joss.02376) [![](https://github.com/covid19datahub/Python/workflows/utests_on_commit/badge.svg)](https://github.com/covid19datahub/Python)

Download COVID-19 data across governmental sources at national, regional, and city level, as described in [Guidotti and Ardia (2020)](https://www.doi.org/10.21105/joss.02376). Includes the time series of vaccines, tests, cases, deaths, recovered, hospitalizations, intensive therapy, and policy measures by [Oxford COVID-19 Government Response Tracker](https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker). Please agree to the [Terms of Use](https://covid19datahub.io/LICENSE.html) and cite the following reference when using it:

**Reference**

Guidotti, E., Ardia, D., (2020).      
COVID-19 Data Hub       
_Journal of Open Source Software_, **5**(51):2376   
[https://doi.org/10.21105/joss.02376](https://doi.org/10.21105/joss.02376)  

## Setup and usage

Install from [pip](https://pypi.org/project/covid19dh/) with

```python
pip install covid19dh
```

Importing the main function `covid19()`   

```python
from covid19dh import covid19
x, src = covid19() 
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19dh
```

## Return values

The function `covid19()` returns 2 pandas dataframes:
* the data and
* references to the data sources.

## Parametrization

### Country

List of country names (case-insensitive) or ISO codes (alpha-2, alpha-3 or numeric). The list of ISO codes can be found [here](https://github.com/covid19datahub/COVID19/blob/master/inst/extdata/db/ISO.csv).

Fetching data from a particular country:

```python
x, src = covid19("USA") # Unites States
```

Specify multiple countries at the same time:

```python
x, src = covid19(["ESP","PT","andorra",250])
```

If `country` is omitted, the whole dataset is returned:

```python
x, src = covid19()
```

### Raw data

Logical. Skip data cleaning? Default `True`. If `raw=False`, the raw data are cleaned by filling missing dates with `NaN` values. This ensures that all locations share the same grid of dates and no single day is skipped. Then, `NaN` values are replaced with the previous non-`NaN` value or `0`.  

```python
x, src = covid19(raw = False)
```

### Date filter

Date can be specified with `datetime.datetime`, `datetime.date` or as a `str` in format `YYYY-mm-dd`.

```python
from datetime import datetime
x, src = covid19("SWE", start = datetime(2020,4,1), end = "2020-05-01")
```

### Level

Integer. Granularity level of the data:

1. Country level
2. State, region or canton level
3. City or municipality level

```python
from datetime import date
x, src = covid19("USA", level = 2, start = date(2020,5,1))
```

### Cache

Logical. Memory caching? Significantly improves performance on successive calls. By default, using the cached data is enabled.

Caching can be disabled (e.g. for long running programs) by:

```python
x, src = covid19("FRA", cache = False)
```

### Vintage

Logical. Retrieve the snapshot of the dataset that was generated at the `end` date instead of using the latest version. Default `False`.

To fetch e.g. US data that were accessible on *22th April 2020* type

```python
x, src = covid19("USA", end = "2020-04-22", vintage = True)
```

The vintage data are collected at the end of the day, but published with approximately 48 hour delay,
once the day is completed in all the timezones.

Hence if `vintage = True`, but `end` is not set, warning is raised and `None` is returned.

```python
x, src = covid19("USA", vintage = True) # too early to get today's vintage
```

```
UserWarning: vintage data not available yet
```

### Data Sources

The data sources are returned as second value.

```python
from covid19dh import covid19
x, src = covid19("USA")
print(src)
```

### Additional information

Find out more at https://covid19datahub.io

## Acknowledgements

Developed and maintained by [Martin Benes](https://pypi.org/user/martinbenes1996/).

## Cite as

*Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.*

A BibTeX entry for LaTeX users is

```latex
@Article{,
    title = {COVID-19 Data Hub},
    year = {2020},
    doi = {10.21105/joss.02376},
    author = {Emanuele Guidotti and David Ardia},
    journal = {Journal of Open Source Software},
    volume = {5},
    number = {51},
    pages = {2376}
}
```