#!/usr/bin/env python

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

ext_module = Extension('_Mykytea',
                       sources=['mykytea_wrap.cxx', 'mykytea.cpp'],
                       libraries=["kytea"],
                       )

setup(name='kytea-python',
      version='0.1',
      author='chezou',
      author_email='chezou@gmail.com',
      ext_modules=[ext_module],
      py_modules=['Mykytea'],
      )
