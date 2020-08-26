
# requirements
try:
  with open('requirements.txt') as f:
    reqs = f.read().splitlines()
except:
  reqs = []

import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'covid19dh',
  version = '1.1.4',
  author = 'Covid-19 Data Hub',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Unified data hub for a better understanding of COVID-19 https://covid19datahub.io',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='GPL',
  url = 'https://www.covid19datahub.io/',
  download_url = 'https://github.com/covid19datahub/Python/archive/1.1.4.tar.gz',
  keywords = ['2019-nCov', 'coronavirus', 'covid-19', 'covid-data', 'covid19-data'],
  install_requires=reqs,
  package_dir={'': '.'},
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Other Audience',
    'Topic :: Database',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
