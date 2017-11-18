#!/bin/bash

set -ex

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew update
    brew outdated pyenv || brew upgrade pyenv
    brew outdated swig || brew upgrade swig
    brew install swig
    swig -version
    brew install pyenv-virtualenv
    pyenv install $PYTHON
    export PYENV_VERSION=$PYTHON
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    python --version
fi
wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz
tar zxf kytea-0.4.7.tar.gz
pushd kytea-0.4.7 && ./configure && make && sudo make install && popd
rm -r kytea-0.4.7
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then sudo ldconfig; fi 
