#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from pathlib import Path

from setuptools import find_packages, setup


# Package meta-data.
NAME = 'scania_truck_air_presure_fault_detector'
DESCRIPTION = 'classification model for scania truck air pressure fault detection.'
URL = 'https://github.com/Damisss/defect_detection_in_air_presure_system_of_truck'
EMAIL = 'sam@sam.com'
AUTHOR = 'Damisss'
REQUIRES_PYTHON = '>=3.6.0'

# Load the package's __version__.py module as a dictionary.
ROOT_DIR = Path(__file__).resolve().parent

#Packages that are required for this module to be executed
def list_reqs(fname=ROOT_DIR / 'requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the
# Trove Classifier for that!

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(ROOT_DIR / 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError: 
    long_description = DESCRIPTION

PACKAGE_DIR = ROOT_DIR / 'scania_truck_air_presure_fault_detector'
about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'] ,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests')),
    package_data={'scania_truck_air_presure_fault_detector': ['VERSION']},
    include_package_data=True,
    install_requires=list_reqs(),
    extras_require={},
    license='BSD-3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)