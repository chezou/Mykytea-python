"""Build the _Mykytea extension.

Project metadata lives in pyproject.toml. This file only describes the C++
extension, whose SWIG wrapper is generated at build time.
"""

import os

from setuptools import Extension, setup
from setuptools.command.build_py import build_py as _build_py

SRC_DIR = os.path.join("lib", "kytea")

include_dirs = [SRC_DIR, "include"]
library_dirs = [SRC_DIR]

kytea_dir = os.environ.get("KYTEA_DIR")
if kytea_dir:
    include_dirs.append(os.path.join(kytea_dir, "include"))
    library_dirs.append(os.path.join(kytea_dir, "lib"))
elif os.name != "nt":
    # Compilers search /usr/local/include by default, but SWIG does not.
    include_dirs.append("/usr/local/include")


class build_py(_build_py):
    """Run build_ext first so the SWIG-generated Mykytea.py exists."""

    def run(self):
        self.run_command("build_ext")
        super().run()


ext_module = Extension(
    "_Mykytea",
    sources=[os.path.join(SRC_DIR, "mykytea.i"), os.path.join(SRC_DIR, "mykytea.cpp")],
    depends=[os.path.join(SRC_DIR, "mykytea.hpp")],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=["libkytea" if os.name == "nt" else "kytea"],
    swig_opts=["-c++", "-Wall", "-outdir", SRC_DIR]
    + [f"-I{d}" for d in include_dirs],
)

setup(ext_modules=[ext_module], cmdclass={"build_py": build_py})
