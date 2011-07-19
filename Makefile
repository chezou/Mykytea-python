all:
	swig -Wall -c++ -python -shadow -c++ -I/usr/local/include mykytea.i
	python setup.py build_ext --inplace

.PHONY: clean
clean:
	rm -f mykytea_wrap.cxx Mykytea.py _Mykytea.so