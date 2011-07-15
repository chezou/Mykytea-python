_mykytea.so: mykytea.o mykytea_wrap.o
	g++ -shared mykytea.o mykytea_wrap.o -o _Mykytea.so -lkytea

mykytea.o: mykytea.cpp
	g++ -c mykytea.cpp 

mykytea_wrap.o: mykytea_wrap.cxx
	g++ -c mykytea_wrap.cxx -I/usr/include/python2.7

mykytea_wrap.cxx: mykytea.i mykytea.cpp mykytea.hpp
	swig -c++ -python mykytea.i

.PHONY: clean
clean:
	rm -f mykytea.o mykytea_wrap.o mykytea_wrap.cxx Mykytea.py Mykytea.pyc _Mykytea.so