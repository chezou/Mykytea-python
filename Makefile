# Set KYTEA_DIR if KyTea is installed outside /usr/local, e.g.
#   KYTEA_DIR=$(brew --prefix) make
PYTHON ?= python

all:
	$(PYTHON) -m pip install -e .

install:
	$(PYTHON) -m pip install .

build:
	$(PYTHON) -m build

test:
	$(PYTHON) -m pytest

.PHONY: all install build test clean
clean:
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete
	rm -f lib/kytea/Mykytea.py lib/kytea/mykytea_wrap.cpp lib/kytea/_version.py
	rm -rf build dist wheelhouse *.egg-info lib/kytea/*.egg-info
