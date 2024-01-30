import sys
import unittest

sys.path.append(".")
sys.path.append("tests")

# === unit tests ===
from test_covid19_latest import *
from test_covid19_vintage import *
from test_cite import *
# ==================


# logging
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)

# run unittests
if __name__ == "__main__":
    unittest.main()
