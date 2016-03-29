KyTea wrapper for python
==========================

Mykytea-python is a python wrapper module for KyTea, a general text analysis toolkit.
KyTea is developed by KyTea Development Team

Detailed information of KyTea can be found at
http://www.phontron.com/kytea

Install Dependencies
--------------------

You need to install KyTea before build.

To install Mykytea-python, run
--------------------

    % pip install kytea

To build Mykytea-python, run (if you don't want to use `pip`)
--------------------

    % make

If you want to install, run

    % sudo make install

If you fail to make, please try to install SWIG and run

    % swig -c++ -python -I/usr/local/include mykytea.i

Or if you still fail on Max OS X, run with some variables
    % ARCHFLAGS="-arch x86_64" CC=gcc CXX=g++ make

If you compiled kytea with clang, you need ARCHFLAGS only.

To create wheel
--------------------

To create whl archive, the setuptools and wheel are needed.

   % python setup.py bdist_wheel

How to use?
--------------------

  See 'lib/test/mykytea_test.py' as a sample program.

License
--------------------

MIT License
