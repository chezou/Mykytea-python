#!/usr/bin/env python

import os
import sys
from setuptools import setup, Extension, find_packages

is_windows = os.name == 'nt'

lib = ["libkytea"] if is_windows else ["kytea"]

include_dirs = ['lib/kytea', 'include']
library_dirs = ["lib/kytea"]

kytea_dir = os.environ.get("KYTEA_DIR")
if kytea_dir:
    include_dirs.append(os.path.join(kytea_dir, "include"))
    library_dirs.append(os.path.join(kytea_dir, "lib"))

ext_module = Extension('_Mykytea',
                       sources=['lib/kytea/mykytea_wrap.cxx', 'lib/kytea/mykytea.cpp'],
                       library_dirs=library_dirs,
                       libraries=lib,
                       include_dirs=include_dirs
                       )

libdir = 'lib/kytea'
sys.path.append('./lib/kytea')
sys.path.append('./lib/test')
VERSION = "0.1.7"

setup(
      name='kytea',
      version=VERSION,
      author='Michiaki Ariga',
      author_email='chezou@gmail.com',
      description=('An text analysis toolkit KyTea binding'),
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      license='MIT License',
      keywords=['KyTea', 'NLP', 'Japanese morphological analyzer'],
      url='https://github.com/chezou/Mykytea-python',
      download_url='https://github.com/chezou/Mykytea-python/tarball/{}'.format(VERSION),
      classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
      ],
      ext_modules=[ext_module],
      packages=find_packages(libdir),
      package_dir={"": libdir},
      py_modules=['Mykytea'],
      test_suite='mykytea_test.suite'
      )
