#!/bin/bash
set -euo pipefail

KYTEA_VERSION=0.4.7

# SWIG comes from PyPI as a build dependency (see pyproject.toml).
yum install -y wget

# Build and install kytea
wget https://www.phontron.com/kytea/download/kytea-${KYTEA_VERSION}.tar.gz
tar zxf kytea-${KYTEA_VERSION}.tar.gz
pushd kytea-${KYTEA_VERSION}
autoreconf -i
./configure && make -j"$(nproc)" && make install
ldconfig
popd
rm -rf kytea-${KYTEA_VERSION} kytea-${KYTEA_VERSION}.tar.gz
