ifneq ($(KYTEA_DIR),)
  include_dir = $(KYTEA_DIR)/include
else
  include_dir = /usr/local/include
endif

all:
	swig -Wall -c++ -python -shadow -I$(include_dir) lib/kytea/mykytea.i
	python setup.py build_ext --inplace

install:
	python setup.py install

test:
	python ./lib/test/mykytea_test.py

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete
	rm -f lib/kytea/Mykytea.py
	rm -rf build
	rm -rf dist
