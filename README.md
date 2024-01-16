# KyTea wrapper for Python

[![PyPI version](https://badge.fury.io/py/kytea.svg)](https://badge.fury.io/py/kytea)
[![](https://img.shields.io/badge/-Sponsor-fafbfc?logo=GitHub%20Sponsors
)](https://github.com/sponsors/chezou)

Mykytea-python is a Python wrapper module for KyTea, a general text analysis toolkit.
KyTea is developed by KyTea Development Team.

Detailed information on KyTea can be found at:
http://www.phontron.com/kytea

## Installation

### Install Mykytea-python via pip

You can install Mykytea-python via `pip`.

```sn
pip install kytea
```

You don't have to install KyTea anymore before installing Mykytea-python when you install it by using wheel on PyPI.

You should have any KyTea model on your machine.

### Build Mykytea-python from source

If you want to build from source, you need to install KyTea.

Then, run


```sh
make
```

After make, you can install Mykytea-python by running

```sh
make install
```

If you fail to make, please try to install SWIG and run

```sh
swig -c++ -python -I/usr/local/include mykytea.i
```

Or if you still fail on Max OS X, run with some variables

```sh
$ ARCHFLAGS="-arch x86_64" CC=gcc CXX=g++ make
```

If you compiled kytea with clang, you need ARCHFLAGS only.

Or, you use macOS and Homebrew, you can use `KYTEA_DIR` to pass the directory of KyTea.

```sh
brew install kytea
KYTEA_DIR=$(brew --prefix) make all
```

## How to use it?

Here is the example code to use Mykytea-python.

```python
import Mykytea

def showTags(t):
    for word in t:
        out = word.surface + "\t"
        for t1 in word.tag:
            for t2 in t1:
                for t3 in t2:
                    out = out + "/" + str(t3)
                out += "\t"
            out += "\t"
        print(out)

def list_tags(t):
    def convert(t2):
        return (t2[0], type(t2[1]))
    return [(word.surface, [[convert(t2) for t2 in t1] for t1 in word.tag]) for word in t]

# Pass arguments for KyTea as the following:
opt = "-model /usr/local/share/kytea/model.bin"
mk = Mykytea.Mykytea(opt)

s = "今日はいい天気です。"

# Fetch segmented words
for word in mk.getWS(s):
    print(word)

# Show analysis results
print(mk.getTagsToString(s))

# Fetch first best tag
t = mk.getTags(s)
showTags(t)

# Show all tags
tt = mk.getAllTags(s)
showTags(tt)
```

## License

MIT License
