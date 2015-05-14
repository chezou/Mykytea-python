#!/usr/bin/env python

try:
    from setuptools import setup, Extension, find_packages
except ImportError:
    from distutils.core import setup, Extension, find_packages

ext_module = Extension('_Mykytea',
                       sources=['lib/kytea/mykytea_wrap.cxx', 'lib/kytea/mykytea.cpp'],
                       libraries=["kytea"],
                       )

import os
import sys

libdir = 'lib/kytea'

import info
import version

setup(
      name='kytea',
      version='0.1.0',
      author='Michiaki Ariga',
      author_email='chezou@gmail.com',
      description = ('An text analysis toolkit KyTea binding'),
      license = 'MIT',
      keywords = 'KyTea NLP',
      url = 'https://github.com/chezou/Mykytea-python',
      ext_modules=[ext_module],
      packages= find_packages(libdir),
      package_dir={"": libdir},
      py_modules=['Mykytea'],
      )
