#!/usr/bin/python

# requirements
try:
    with open('requirements.txt') as f:
        reqs = f.read().splitlines()
except Exception:
    reqs = []

import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='covid19dh',
    version='2.3.1',
    author='Martin Beneš',
    author_email='martinbenes1996@gmail.com',
    description='Unified data hub for a better understanding of COVID-19 https://covid19datahub.io',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://www.covid19datahub.io',
    download_url='https://github.com/covid19datahub/Python/archive/2.3.0.tar.gz',
    keywords=['2019-nCov', 'coronavirus', 'covid-19', 'covid-data', 'covid19-data'],
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
