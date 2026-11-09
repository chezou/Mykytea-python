%module Mykytea
%include "stl.i"
%include "exception.i"


%{
#include "mykytea.hpp"
%}


namespace std {
  %template(StringVector) vector<string>;
  %template(Pairsd) pair<string, double>;
  %template(PairVector) vector< pair<string, double> >;
  %template(PairVectorVector) vector< vector< pair<string, double> > >;
  %template(TagsVector) vector<Tags>;

}

%newobject getWS;
%newobject getTags;
%newobject getAllTags;

%exception{
  try{
    $action
  } catch (const std::exception &e){
    SWIG_exception(SWIG_RuntimeError, e.what() );
  } catch (...) {
    SWIG_exception(SWIG_UnknownError, "Unknown exception");
  }
}

%pythoncode %{
import os as _os

# KyTea analysis options that can be passed as keyword arguments.
_FLAG_OPTIONS = ("nows", "notags", "nounk")
_VALUE_OPTIONS = (
    "model", "wsconst", "numtags", "tagmax",
    "unktag", "deftag", "unkbeam", "debug",
)


def _build_args(opt, options):
    """Convert ``Mykytea()`` arguments to a KyTea argv (without argv[0])."""
    if isinstance(opt, str):
        args = opt.split()
    else:
        args = [_os.fspath(a) if isinstance(a, _os.PathLike) else str(a) for a in opt]

    for name, value in options.items():
        if value is None or value is False:
            continue
        if name in _FLAG_OPTIONS:
            args.append("-" + name)
        elif name == "notag":
            for n in [value] if isinstance(value, int) else value:
                args += ["-notag", str(n)]
        elif name == "model":
            args += ["-model", _os.fspath(value)]
        else:
            args += ["-" + name, str(value)]
    return args
%}

%feature("shadow") Mykytea::Mykytea %{
def __init__(
    self,
    opt="",
    *,
    model=None,
    nows=False,
    notags=False,
    notag=None,
    nounk=False,
    wsconst=None,
    numtags=None,
    tagmax=None,
    unktag=None,
    deftag=None,
    unkbeam=None,
    debug=None,
):
    """Create a KyTea analyzer.

    Options can be given as a KyTea command line string or list, as keyword
    arguments, or both. Keyword arguments are applied after ``opt``::

        Mykytea("-model /path/to/model.bin -deftag UNK")
        Mykytea(model="/path/to/model.bin", deftag="UNK")

    :param opt: KyTea command line options as a string or a list of strings.
    :param model: Path to the model file.
    :param nows: Don't do word segmentation.
    :param notags: Do only word segmentation, no tagging.
    :param notag: Skip the n-th tag (starting at 1). An int or a list of ints.
    :param nounk: Don't estimate the pronunciation of unknown words.
    :param wsconst: Character types not to be segmented (e.g. ``"D"`` for digits).
    :param numtags: The number of tags to estimate.
    :param tagmax: The maximum number of tag candidates to keep.
    :param unktag: A tag appended to unknown words.
    :param deftag: A tag for words that cannot be given any tag.
    :param unkbeam: Beam width for unknown word search (0 for full search).
    :param debug: Debugging level (0=silent, 1=simple, 2=detailed).
    """
    args = _build_args(opt, {
        "model": model, "nows": nows, "notags": notags, "notag": notag,
        "nounk": nounk, "wsconst": wsconst, "numtags": numtags,
        "tagmax": tagmax, "unktag": unktag, "deftag": deftag,
        "unkbeam": unkbeam, "debug": debug,
    })
    _Mykytea.Mykytea_swiginit(self, _Mykytea.new_Mykytea(args))
%}

%include kytea/kytea.h
%include kytea/kytea-struct.h
%include mykytea.hpp

