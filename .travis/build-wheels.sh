#!/bin/bash
set -e -x

# Install any system packages required here
yum -y update && yum -y install libtool pcre-devel curl make autoconf

# Install swig
curl --location-trusted --remote-name https://downloads.sourceforge.net/project/swig/swig/swig-3.0.12/swig-3.0.12.tar.gz -o swig-3.0.12.tar.gz
tar xzf swig-3.0.12.tar.gz
pushd swig-3.0.12 && ./configure --prefix=/usr && make  && make install && popd
swig -version

# Remove old Python
rm -rf /opt/python/cpython-2.6.9-ucs2
rm -rf /opt/python/cpython-2.6.9-ucs4
rm -rf /opt/python/cp33-cp33m

#Make kytea
cd /io/kytea-0.4.7
autoreconf -i
./configure && make distclean && make && make install
ldconfig
cd /io
swig -Wall -c++ -python -shadow -I/usr/local/include /io/lib/kytea/mykytea.i
cd /

#Compile wheels
for PYBIN in /opt/python/*/bin; do
    #"${PYBIN}/pip" install -r /io/requirements.txt   
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install kytea --no-index -f /io/wheelhouse
    (cd "$HOME"; "${PYBIN}/python" /io/lib/test/mykytea_test.py)
done

mv /io/wheelhouse /io/dist
