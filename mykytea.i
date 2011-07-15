%module Mykytea
%include "stl.i"

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

%include kytea.h
%include kytea-struct.h
%include mykytea.hpp

