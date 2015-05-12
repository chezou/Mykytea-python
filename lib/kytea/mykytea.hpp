// mykytea.hpp
#ifndef MYKYTEA_HPP
#define MYKYTEA_HPP

#include <vector>
#include <string>
#include <map>

#include <kytea/kytea.h>
#include <kytea/kytea-struct.h>
#include <kytea/string-util.h>


using namespace std;
using namespace kytea;

typedef vector< vector< pair<string, double> > > tags;

struct Tags{
  string surface;
  tags tag;
};

class Mykytea
{
public:

  Mykytea(char* str);
  ~Mykytea();

  //単語境界を取得する

  vector<string>* getWS(string str);

  //尤もらしいタグを取得する

  vector<Tags>* getTags(string str);

  //すべてのタグを取得する

  vector<Tags>* getAllTags(string str);

  //タグを文字列で取得する

  string getTagsToString(string str);

private:
  Kytea* kytea;
  StringUtil* util;
  KyteaConfig* config;
};
#endif
