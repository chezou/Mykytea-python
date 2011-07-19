KyTea wrapper for python
==========================
2011/07/20 chezou

Mykytea-python is a python wrapper module for KyTea, a general text analysis toolkit.

KyTea is developed by KyTea Development Team

Detailed information of KyTea can be found at
http://www.phontron.com/kytea

Install Dependencies
--------------------
You need install KyTea before build.

To build Mykytea-python, run
--------------------

   % python setup.py build
   % sudo python setup.py install


  (If you fail to make, please try to install SWIG and run)
   % swig -Wall -c++ -python -shadow -c++ -I/usr/local/include mykytea.i

How to use?
--------------------

  See 'mykytea_test.py' as a sample program.

License
--------------------
MIT License