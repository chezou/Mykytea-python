#!/bin/bash
set -euo pipefail

KYTEA_VERSION=0.4.7

# SWIG comes from PyPI as a build dependency (see pyproject.toml), and the
# manylinux image already has curl and autotools, so nothing is installed with
# yum: refreshing its metadata alone can take over 15 minutes on a slow mirror.

# Build and install kytea
curl -fsSL --retry 3 -o kytea-${KYTEA_VERSION}.tar.gz \
    https://www.phontron.com/kytea/download/kytea-${KYTEA_VERSION}.tar.gz
echo "534a33d40c4dc5421f053c71a75695c377df737169f965573175df5d2cff9f46  kytea-${KYTEA_VERSION}.tar.gz" \
    | sha256sum -c -
tar zxf kytea-${KYTEA_VERSION}.tar.gz
pushd kytea-${KYTEA_VERSION}
autoreconf -i
./configure && make -j"$(nproc)" && make install
ldconfig
popd
rm -rf kytea-${KYTEA_VERSION} kytea-${KYTEA_VERSION}.tar.gz
