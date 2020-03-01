#!/bin/bash
set -e -x

# Remove Python 2.7
rm -rf /opt/python/cp27*/

# Install any system packages required here
yum -y update && yum -y install libtool pcre-devel curl make autoconf

# Install swig
SWIG_VER=4.0.1
curl --location-trusted --remote-name https://downloads.sourceforge.net/project/swig/swig/swig-${SWIG_VER}/swig-${SWIG_VER}.tar.gz -o swig-${SWIG_VER}.tar.gz
tar xzf swig-${SWIG_VER}.tar.gz
pushd swig-${SWIG_VER} && ./configure --prefix=/usr && make  && make install && popd
swig -version

#Make kytea
cd /tmp
curl --location-trusted --remote-name http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz -o kytea-0.4.7.tar.gz
tar zxf kytea-0.4.7.tar.gz
cd /tmp/kytea-0.4.7
autoreconf -i
./configure && make && make install
ldconfig
cd /io
swig -Wall -c++ -python -shadow -I/usr/local/include /io/lib/kytea/mykytea.i
cd /

#Compile wheels
for PYBIN in /opt/python/*/bin; do
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
