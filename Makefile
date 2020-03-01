all:
	swig -Wall -c++ -python -shadow -I/usr/local/include lib/kytea/mykytea.i
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
