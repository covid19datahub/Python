
from io import StringIO
import math
import re
import warnings

import pandas as pd
import requests

def get_sources():
    url = 'https://storage.covid19datahub.io/src.csv'
    response = requests.get(url) # headers={'User-Agent': 'Mozilla/5.0'}
    return pd.read_csv( StringIO(response.text))

def cite(x, verbose = True, sources = None):
    # all sources if missing
    if sources is None:
        sources = get_sources()
        
    # transform data
    isos = set(x["iso_alpha_3"].unique())
    params = set(x.columns)
    # add universal
    isos.add(math.nan)
    
    # collect used references
    sources = sources[sources["iso_alpha_3"].isin(isos) & sources["data_type"].isin(params)]
    references = sources.fillna("")
    references.url = references.url.apply(
        lambda u: re.sub(
            r"(http://|https://|www\\.)([^/]+)(.*)",
            r"\1\2/",
            u )
        )
    #unique_references = references.groupby(["title"])
    unique_references = references.groupby(["title","author","institution","url","textVersion","bibtype"]) 
    
    # turn references into citations
    citations = []
    for n,g in unique_references:
        for i in range(1):
        #for idx,row in g.iterrows():
            #title = n
            #author = row['author']
            #institution = row['institution']
            #url = row['url']
            #textVersion = row['textVersion']
            #bibtype = row['bibtype']
            #year = row['year']
            (title,author,institution,url,textVersion,bibtype) = n
            year = g.year.max()

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
                    url = re.sub(r"(http://|https://|www\\.)([^/]+)(.*)",
                                 r"\1\2/", url)
                    post += f"{url}"
                else:
                    post += "."
                citation = f"{pre} ({year}), {post}"
        
            citations.append(citation)
    
    if verbose:
        print("\033[1mData References:\033[0m\n", end="")
        for ref in citations:
            print("\t" + ref, end="\n\n")
        print("\033[33mTo hide the data sources use 'verbose = False'.\033[0m")
        
    return sources
        
__all__ = ["cite","get_sources"]