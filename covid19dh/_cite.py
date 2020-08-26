
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

def sources_to_citations(sources):
    # shorten URL
    sources.url = sources.url.apply(
        lambda u: re.sub(
            r"(http://|https://|www\\.)([^/]+)(.*)",
            r"\1\2/",
            u )
        )
    # remove duplicit
    unique_references = sources.groupby(["title","author","institution","url","textVersion","bibtype"]) 
    
    # format
    citations = []
    for n,g in unique_references:
        for i in range(1):
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
    return citations

def cite(x, verbose = True, sources = None):
    # all sources if missing
    if sources is None:
        sources = get_sources()
    
    # hash data stats
    isos = set(x["iso_alpha_3"].unique())
    isos.add(math.nan)
    params = set(x.columns)
    # prefilter
    sources = sources[
        sources["iso_alpha_3"].isin(isos) &
        sources["data_type"].isin(params) ]
    sources = sources.fillna("")
    
    # filter
    def is_source_used(ref):
        # data type not present
        if not ref['data_type'] in params: return False
        # fallbacks
        if not ref['iso_alpha_3'] or not ref['administrative_area_level']: return True
        
        # check both equal
        return ((x.iso_alpha_3 == ref.iso_alpha_3) & (x.administrative_area_level == ref.administrative_area_level)).any()
    
    sources = sources[sources.apply(is_source_used, axis=1)]
    
    # drop fallback
    for p in params:
        non_fallback = (sources.data_type == p) & (sources.iso_alpha_3 != '')
        fallback = (sources.data_type == p) & (sources.iso_alpha_3 == '')
        if non_fallback.any():
            sources.drop(fallback.index[fallback].tolist(), inplace=True)
    
    #citations = sources_to_citations(sources)
    
    #if verbose:
    #    print("\033[1mData References:\033[0m\n", end="")
    #    for ref in citations:
    #        print("\t" + ref, end="\n\n")
    #    print("\033[33mTo hide the data sources use 'verbose = False'.\033[0m")
    
    sources.replace(r'^\s*$', math.nan, regex=True, inplace=True)  
    return sources
        
__all__ = ["cite","get_sources"]