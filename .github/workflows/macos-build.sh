#!/bin/bash

X86_TRIPLET=x86_64-apple-macos10.9
ARM_TRIPLET=arm64-apple-macos11

brew install automake libtool autoconf

git clone --depth=1 https://github.com/neubig/kytea.git
cd kytea

rm -rf src/lib/.libs-arm64 src/lib/.libs-x86_64 src/lib/.libs.combined

autoreconf -i
./configure --host="arm-apple-darwin22.1.0 " CXX="clang++ -target $ARM_TRIPLET" CC="clang -target $ARM_TRIPLET"

make clean
make -j$(sysctl -n hw.logicalcpu_max)

mv src/lib/.libs src/lib/.libs-arm64

./configure --host="x86_64-apple-darwin20.6.0" CXX="clang++ -target $X86_TRIPLET" CC="clang -target $X86_TRIPLET"

make clean
make -j$(sysctl -n hw.logicalcpu_max)

mv src/lib/.libs src/lib/.libs-x86_64

rm -rf src/lib/.libs.combined
mkdir src/lib/.libs.combined

lipo -create src/lib/.libs-arm64/libkytea.0.dylib src/lib/.libs-x86_64/libkytea.0.dylib -output src/lib/.libs.combined/libkytea.0.dylib

lipo -create src/lib/.libs-arm64/libkytea.a src/lib/.libs-x86_64/libkytea.a -output src/lib/.libs.combined/libkytea.a

cp src/lib/.libs-arm64/libkytea.lai src/lib/.libs.combined/libkytea.lai

ls -l src/lib/.libs-arm64/*.o | while read line; do
    file=$(basename $file)
    echo $file
    lipo -create src/lib/.libs-arm64/$file src/lib/.libs-x86_64/$file -output src/lib/.libs.combined/$file
done

cd src/lib/.libs.combined
ln -s libkytea.0.dylib libkytea.dylib
ln -s ../libkytea.a libkytea.a
cd ../../..
mv src/lib/.libs.combined src/lib/.libs

sudo make install
cd ..

swig -Wall -c++ -python -shadow -I./kytea/src/include lib/kytea/mykytea.i
python -m cibuildwheel --archs x86_64,arm64,universal2 --output-dir wheelhouse
