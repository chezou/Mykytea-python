from pathlib import Path

import pytest

# CI downloads the model to the project root on Windows. Elsewhere the model
# installed with KyTea (or the one in $KYTEA_MODEL) is used.
_LOCAL_MODEL = Path(__file__).resolve().parents[1] / "model.bin"


@pytest.fixture(scope="session")
def Mykytea():
    import Mykytea

    return Mykytea


@pytest.fixture(scope="session")
def new(Mykytea):
    """Create a Mykytea.Mykytea with the test model."""

    def factory(opt="", **options):
        if _LOCAL_MODEL.exists():
            options.setdefault("model", _LOCAL_MODEL)
        return Mykytea.Mykytea(opt, **options)

    return factory


@pytest.fixture(scope="session")
def mk(new):
    return new("-deftag UNKNOWN!!")
