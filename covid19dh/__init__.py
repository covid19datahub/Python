# -*- coding: utf-8 -*-
"""Unified data hub for a better understanding of COVID-19.

For more information check README.md.
 
Reference: https://covid19datahub.io/
Todo:
    * caching
"""

import pkg_resources
from .main import *

__version__ = pkg_resources.get_distribution("covid19dh").version

