all:
	swig -Wall -c++ -python -shadow -c++ mykytea.i
	python setup.py build_ext --inplace

.PHONY: clean
clean:
	rm -f mykytea_wrap.cxx Mykytea.py _Mykytea.so