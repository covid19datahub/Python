<a href="https://covid19datahub.io"><img src="https://storage.covid19datahub.io/logo.svg" align="right" height="128"/></a>

# Python Interface to COVID-19 Data Hub

[![](https://img.shields.io/pypi/v/covid19dh.svg?color=brightgreen)](https://pypi.org/pypi/covid19dh/) [![](https://img.shields.io/pypi/dm/covid19dh.svg?color=blue)](https://pypi.org/pypi/covid19dh/) [![DOI](https://joss.theoj.org/papers/10.21105/joss.02376/status.svg)](https://doi.org/10.21105/joss.02376) [![](https://github.com/covid19datahub/Python/workflows/utests_on_commit/badge.svg)](https://github.com/covid19datahub/Python)

The goal of COVID-19 Data Hub is to provide the research community with a [unified dataset](https://covid19datahub.io/articles/data.html) by collecting worldwide fine-grained case data, merged with exogenous variables helpful for a better understanding of COVID-19. Please agree to the [Terms of Use](https://covid19datahub.io/LICENSE.html) and cite the following reference when using it:

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

Importing main `covid19()` function with 

```python
from covid19dh import covid19

x,src = covid19("ITA") # load data
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19dh
```

## Return values

Call of `covid19()` returns in all cases 2 arguments, pandas dataframes,
* the data and
* references to the sources.

## Parametrization

### Country

Country specifies an administrative region, that the data are fetched from.
This is connected with source data comes from. It can be given as
ISO3, ISO2, numeric ISO or country name (case-insensitively). 

Fetching data from a particular country is done with

```python
x,src = covid19("ESP")
```

List of ISO codes can be found [here](https://github.com/covid19datahub/COVID19/blob/master/inst/extdata/src.csv).

Filter can also specify multiple countries at the same time

```python
x,src = covid19(["ESP","PT","andorra",250])
```

Country can be omitted, then whole world data is used.

```python
x,src = covid19()
```

### Date filter

Date can be specified with `datetime.datetime`, `datetime.date`
or as a `str` in format `YYYY-mm-dd`.

```python
from datetime import datetime

x,src = covid19("SWE", start = datetime(2020,4,1), end = "2020-05-01")
```

### Level

Levels work the same way as in all the other our data fetchers.

1. Country level
2. State, region or canton level
3. City or municipality level

```python
from datetime import date

x,src = covid19("USA", level = 2, start = date(2020,5,1))
```

### Cache

Library keeps downloaded data and sources in simple way during runtime. By default, using the cached data is enabled.

Caching can be disabled (e.g. for long running programs) by

```python
x,src = covid19("FRA", cache=False)
```

*More advanced caching is coming.*

### Vintage

Data Hub enables to fetch the vintage data, data archive collected on each day. The data collecting is stable.

To fetch e.g. US data that were accessible on *10th April 2020* type

```python
x,src = covid19("USA", end = "2020-04-22", vintage = True)
```

The vintage data are collected at the end of the day, but published with approximately 48 hour delay,
once the day is completed in all the timezones.

Hence if `vintage = True`, but `end` is not set, warning is raised and `None` is returned.

```python
x,src = covid19("USA", vintage=True) # too early to get today's vintage
```

```
UserWarning: vintage data not available yet
```

### Citations

Sources to data is returned as a second value.

```python
from covid19dh import covid19
x,src = covid19("CZE")
```

Apart from that a following message is printed on `covid19()` call.

```
We have invested a lot of time and effort in creating COVID-19 Data Hub, please cite the following when using it:

        Guidotti, E., Ardia, D., (2020), "COVID-19 Data Hub", Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.

A BibTeX entry for LaTeX users is

        @Article{,
                title = {COVID-19 Data Hub},
                year = {2020},
                doi = {10.21105/joss.02376},
                author = {Emanuele Guidotti and David Ardia},
                journal = {Journal of Open Source Software},
                volume = {5},
                number = {51},
                pages = {2376},
        }

To hide this message use 'verbose = FALSE'.
```

This feature can be turned off by setting `verbose` to `False`.

```python
from covid19dh import covid19
x,src = covid19("CZE", verbose = False) 
```

<!--
To get the data sources of the data that has been acquired use function `cite()`.
It will return only the relevant sources, filtering the irrelevant out.

```python
src = cite(x) # get sources of x
```

Function prints formatted citations to stdout.

```
Data References:
        Czech Statistical Office (2018), https://www.czso.cz/

        Johns Hopkins Center for Systems Science and Engineering (2020), https://github.com/

        Ministery of Health of Czech Republic (2020), https://onemocneni-aktualne.mzcr.cz/

        Our World in Data (2020), https://github.com/

        Hale Thomas, Sam Webster, Anna Petherick, Toby Phillips, and Beatriz Kira (2020). Oxford COVID-19 Government Response Tracker, Blavatnik School of Government.

        World Bank Open Data (2018), https://data.worldbank.org/
```

Switch the printing off by setting `verbose` parameter to `False`.

```python
src = cite(x, verbose = False)
```
-->

Pandas dataframe `src` has following structure

```
    iso_alpha_3  administrative_area_level  ...                     institution                                        textVersion
137         CZE                        1.0  ...                             NaN                                                NaN
138         CZE                        1.0  ...                             NaN                                                NaN
139         CZE                        2.0  ...                             NaN                                                NaN
140         CZE                        2.0  ...                             NaN                                                NaN
141         CZE                        2.0  ...                             NaN                                                NaN
142         CZE                        2.0  ...                             NaN                                                NaN
143         CZE                        3.0  ...                             NaN                                                NaN
144         CZE                        3.0  ...                             NaN                                                NaN
145         CZE                        3.0  ...                             NaN                                                NaN
539         NaN                        NaN  ...                             NaN                                                NaN
540         NaN                        NaN  ...                             NaN                                                NaN
541         NaN                        NaN  ...                             NaN                                                NaN
542         NaN                        NaN  ...                             NaN                                                NaN
543         NaN                        NaN  ...                             NaN                                                NaN
544         NaN                        NaN  ...                             NaN                                                NaN
545         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
546         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
547         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
548         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
549         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
550         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
551         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
552         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
553         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
554         NaN                        NaN  ...  Blavatnik School of Government  Hale Thomas, Sam Webster, Anna Petherick, Toby...
555         NaN                        NaN  ...                             NaN                                                NaN
```

Dataframe columns are
* *iso_alpha_3*, *administrative_area_level*,
* *data_type*
* *url*
* *title*, *author*, *institution*
* *year*
* *bibtype*, *textVersion*

In progress
* conversion of the sources
  * printed list of references
  * BibTeX format
  
<!--
*All sources* can be acquired with

```python
src_all = get_sources() # get all sources
```
-->


## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996)

