#!/usr/bin/env python

try:
    from setuptools import setup, Extension, find_packages
except ImportError:
    from distutils.core import setup, Extension, find_packages

ext_module = Extension('_Mykytea',
                       sources=['lib/kytea/mykytea_wrap.cxx', 'lib/kytea/mykytea.cpp'],
                       libraries=["kytea"],
                       include_dirs=['lib/kytea']
                       )

import os
import sys

libdir = 'lib/kytea'
sys.path.append('./lib/kytea')
sys.path.append('./lib/test')
VERSION = "0.1.3"

setup(
      name='kytea',
      version=VERSION,
      author='Michiaki Ariga',
      author_email='chezou@gmail.com',
      description = ('An text analysis toolkit KyTea binding'),
      license = 'MIT License',
      keywords = ['KyTea', 'NLP', 'Japanese morphological analyzer'],
      url = 'https://github.com/chezou/Mykytea-python',
      download_url = 'https://github.com/chezou/Mykytea-python/tarball/0.1.3',
      classifier    = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
      ],
      ext_modules=[ext_module],
      packages= find_packages(libdir),
      package_dir={"": libdir},
      py_modules=['Mykytea'],
      test_suite= 'mykytea_test.suite'
      )
