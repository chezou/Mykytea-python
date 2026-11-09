// mykytea.hpp
#ifndef MYKYTEA_HPP
#define MYKYTEA_HPP

#include <vector>
#include <string>
#include <map>
#include <cstdlib>

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

  // args are KyTea command line options, e.g. {"-model", "model.bin"}.
  Mykytea(const vector<string>& args);
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
  // Segment and tag str, honoring -nows, -notags and -notag.
  KyteaSentence analyze(const string& str);
  size_t numTagLevels();

  Kytea* kytea;
  StringUtil* util;
  KyteaConfig* config;
};
#endif
