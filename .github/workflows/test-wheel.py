"""Sanity check for built wheel: import the C extension and run tokenization."""
import sys

import _Mykytea
import Mykytea

opt = "-deftag UNKNOWN!!"
if "--model" in sys.argv:
    model_path = sys.argv[sys.argv.index("--model") + 1].replace("\\", "/")
    opt += f" -model {model_path}"

mk = Mykytea.Mykytea(opt)
words = list(mk.getWS("hello"))
print(f"Tokenization result: {words}")
assert len(words) > 0, "Tokenization returned empty result"
print("Sanity check passed")
