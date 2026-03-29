#!/bin/bash
set -euo pipefail

SWIG_VERSION=4.4.1
KYTEA_VERSION=0.4.7

# Install dependencies
yum install -y wget pcre2-devel

# Build and install swig
wget https://downloads.sourceforge.net/project/swig/swig/swig-${SWIG_VERSION}/swig-${SWIG_VERSION}.tar.gz
tar xzf swig-${SWIG_VERSION}.tar.gz
pushd swig-${SWIG_VERSION}
./configure --prefix=/usr/local
make -j$(nproc)
make install
popd
rm -rf swig-${SWIG_VERSION} swig-${SWIG_VERSION}.tar.gz

# Build and install kytea
wget https://www.phontron.com/kytea/download/kytea-${KYTEA_VERSION}.tar.gz
tar zxf kytea-${KYTEA_VERSION}.tar.gz
pushd kytea-${KYTEA_VERSION}
autoreconf -i
./configure && make && make install
ldconfig
popd
rm -rf kytea-${KYTEA_VERSION} kytea-${KYTEA_VERSION}.tar.gz

# Generate SWIG wrapper
swig -Wall -c++ -python -shadow -I/usr/local/include lib/kytea/mykytea.i
