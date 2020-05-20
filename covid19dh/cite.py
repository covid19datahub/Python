
import math
import warnings

import pandas as pd
import requests

def cite(x):
    # get sources
    url = 'https://raw.githubusercontent.com/covid19datahub/COVID19/master/inst/extdata/src.csv'
    sources = pd.read_csv(url)
    
    # transform data
    isos = set(x["iso_alpha_3"].unique())
    params = set(x.columns)
    # add universal
    isos.add(math.nan)
    
    # collect used references
    sources = sources[sources["iso_alpha_3"].isin(isos) & sources["data_type"].isin(params)]
    unique_sources = sources.fillna("").groupby(["title","author","year","institution","url","textVersion","bibtype"])

    # turn references into citations
    citations = []
    for n,g in unique_sources:
        (title,author,year,institution,url,textVersion,bibtype) = n
        
        if not author and not title:
            warnings.warn("reference does not specify author nor title, omitting")
            continue
        if not year:
            warnings.warn("reference does not specify year, omitting")
            continue
        refinfo = [bool(title),bool(author),bool(year),bool(institution),bool(url),bool(textVersion)]
        
        if textVersion:
            citation = textVersion
        else:
            # pre,post
            if author:
                pre = author
                if title:
                    post = f"{title}"
            elif title:
                pre = title
                post = ""
            # post
            if institution:
                if post:
                    post += ", "
                post += f"{institution}"
            if url:
                if post:
                    post += ", "
                post += f"{url}"
            else:
                post += "."
            citation = f"{pre} ({year}), {post}"
        
        citations.append(citation)
    
    citations.append("Guidotti, E., Ardia, D., (2020), \"COVID-19 Data Hub\", Working paper, doi: 10.13140/RG.2.2.11649.81763.")
    return citations

__all__ = ["cite"]