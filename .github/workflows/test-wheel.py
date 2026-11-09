"""Sanity check for built wheel: import the C extension and run tokenization."""
import sys

import _Mykytea
import Mykytea

model_path = None
opt = "-deftag UNKNOWN!!"
if "--model" in sys.argv:
    model_path = sys.argv[sys.argv.index("--model") + 1].replace("\\", "/")
    opt += f" -model {model_path}"

# Options as a command line string
mk = Mykytea.Mykytea(opt)
words = list(mk.getWS("hello"))
print(f"Tokenization result: {words}")
assert len(words) > 0, "Tokenization returned empty result"

# Options as keyword arguments
mk = Mykytea.Mykytea(deftag="UNKNOWN!!", model=model_path)
assert list(mk.getWS("hello")) == words, "kwargs gave a different result"

try:
    Mykytea.Mykytea(no_such_option=True)
except TypeError:
    pass
else:
    raise AssertionError("unknown keyword argument was accepted")
print("Sanity check passed")
