#!/usr/bin/env python

import os
import sys
from setuptools import setup, Extension, find_packages

is_windows = os.name == "nt"

lib = ["libkytea"] if is_windows else ["kytea"]

include_dirs = ["lib/kytea", "include"]
library_dirs = ["lib/kytea"]

kytea_dir = os.environ.get("KYTEA_DIR")
if kytea_dir:
    include_dirs.append(os.path.join(kytea_dir, "include"))
    library_dirs.append(os.path.join(kytea_dir, "lib"))

ext_module = Extension(
    "_Mykytea",
    sources=["lib/kytea/mykytea_wrap.cxx", "lib/kytea/mykytea.cpp"],
    library_dirs=library_dirs,
    libraries=lib,
    include_dirs=include_dirs,
)

libdir = "lib/kytea"
sys.path.append("./lib/kytea")
sys.path.append("./lib/test")

setup_args = dict(
    ext_modules=[ext_module],
    packages=find_packages(libdir),
    package_dir={"": libdir},
    py_modules=["Mykytea"],
    test_suite="mykytea_test.suite",
)

setup(**setup_args)
