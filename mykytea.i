%module Mykytea
%include "stl.i"
%include "exception.i"

%{
#include "mykytea.hpp"
%}

typedef struct{
  std::string surface;
  tags tag;
} Tags;

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

%include kytea/kytea.h
%include kytea/kytea-struct.h
%include mykytea.hpp

