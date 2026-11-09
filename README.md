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

Mykytea-python supports Python 3.11 or later.

To build from source, install KyTea first, then run

```sh
pip install .
```

SWIG is installed automatically as a build dependency from PyPI, and the
wrapper is generated during the build. You don't need to run `swig` yourself.

If KyTea is installed outside `/usr/local`, pass its prefix with `KYTEA_DIR`.
For example, with Homebrew on macOS:

```sh
brew install kytea
KYTEA_DIR=$(brew --prefix) pip install .
```

For development, `make` installs the package in editable mode and `make test` runs the tests.

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

# Pass options for KyTea as keyword arguments:
mk = Mykytea.Mykytea(model="/usr/local/share/kytea/model.bin")
# or as a KyTea command line string:
# mk = Mykytea.Mykytea("-model /usr/local/share/kytea/model.bin")

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

### Options

`Mykytea.Mykytea()` accepts these KyTea analysis options as keyword arguments.
Keyword arguments are applied after the option string, if both are given.

| Keyword | KyTea option | Description |
| --- | --- | --- |
| `model` | `-model` | Path to the model file |
| `nows` | `-nows` | Don't do word segmentation (`True`/`False`) |
| `notags` | `-notags` | Do only word segmentation, no tagging (`True`/`False`) |
| `notag` | `-notag` | Skip the n-th tag, starting at 1 (an int or a list of ints). A skipped tag is an empty list in `getTags()` and omitted in `getTagsToString()` |
| `nounk` | `-nounk` | Don't estimate the pronunciation of unknown words (`True`/`False`) |
| `wsconst` | `-wsconst` | Character types not to be segmented (e.g. `"D"` for digits) |
| `numtags` | `-numtags` | The number of tags to estimate |
| `tagmax` | `-tagmax` | The maximum number of tag candidates |
| `unktag` | `-unktag` | A tag appended to unknown words |
| `deftag` | `-deftag` | A tag for words that cannot be given any tag |
| `unkbeam` | `-unkbeam` | Beam width for unknown word search (0 for full search) |
| `debug` | `-debug` | Debugging level (0=silent, 1=simple, 2=detailed) |

An unknown keyword argument raises `TypeError`.

## License

MIT License
