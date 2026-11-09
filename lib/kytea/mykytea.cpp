// mykytea.cpp
#include <iostream>
#include <cstring>
#include <cstdlib>
#include "mykytea.hpp"

Mykytea::Mykytea(const vector<string>& args)
{
  // Build an argv; argv[0] is the program name and is ignored by KyTea.
  vector<const char*> argv;
  argv.push_back("");
  for(size_t i = 0; i < args.size(); i++)
    argv.push_back(args[i].c_str());

  config = new KyteaConfig;
  config->setDebug(0);
  config->setOnTraining(false);
  config->parseRunCommandLine((int)argv.size(), argv.data());

  kytea = new Kytea(config);
  kytea->readModel(config->getModelFile().c_str());
  util = kytea->getStringUtil();
}

Mykytea::~Mykytea()
{
  if(kytea != NULL) delete kytea;
}

KyteaSentence Mykytea::analyze(const string& str)
{
    KyteaString surface_string = util->mapString(str);
    KyteaSentence sentence(surface_string, util->normalize(surface_string));
    kytea->calculateWS(sentence);

    // Same conditions as Kytea::analyze()
    if(config->getDoTags())
        for(int i = 0; i < config->getNumTags(); i++)
            if(config->getDoTag(i))
                kytea->calculateTags(sentence, i);

    return sentence;
}

// Convert the tags of a word; max_cands limits the candidates per tag level
// (0 for all). The result has at least num_levels levels so that a skipped
// tag level (-notag) is always an empty list at its position; KyTea itself
// does not create trailing levels that were not calculated.
static tags convertTags(StringUtil* util, const KyteaWord& word, size_t max_cands, size_t num_levels)
{
    tags vec_tag;
    size_t levels = word.tags.size() > num_levels ? word.tags.size() : num_levels;
    for(size_t j = 0; j < levels; j++) {
        vector< pair<string, double> > vec_tmp;
        size_t n = j < word.tags.size() ? word.tags[j].size() : 0;
        if(max_cands > 0 && n > max_cands)
            n = max_cands;
        for(size_t k = 0; k < n; k++)
            vec_tmp.push_back( make_pair(util->showString(word.tags[j][k].first), word.tags[j][k].second) );
        vec_tag.push_back( vec_tmp );
    }
    return vec_tag;
}

// Number of tag levels in getTags/getAllTags results (none with -notags).
size_t Mykytea::numTagLevels()
{
    return config->getDoTags() ? (size_t)config->getNumTags() : 0;
}

vector<string>* Mykytea::getWS(string str){
    vector<string>* vec = new vector<string>;
    KyteaSentence sentence = analyze(str);
    const KyteaSentence::Words & words = sentence.words;

    for(size_t i = 0; i < words.size(); i++)
        vec->push_back(util->showString(words[i].surface));
    return vec;
}

vector<Tags>* Mykytea::getTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;
    KyteaSentence sentence = analyze(str);
    const KyteaSentence::Words & words = sentence.words;

    for(size_t i = 0; i < words.size(); i++) {
        struct Tags t = { util->showString(words[i].surface), convertTags(util, words[i], 1, numTagLevels()) };
        ret_words->push_back( t );
    }
    return ret_words;
}

vector<Tags>* Mykytea::getAllTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;
    KyteaSentence sentence = analyze(str);
    const KyteaSentence::Words & words = sentence.words;

    for(size_t i = 0; i < words.size(); i++) {
        struct Tags t = { util->showString(words[i].surface), convertTags(util, words[i], 0, numTagLevels()) };
        ret_words->push_back( t );
    }
    return ret_words;
}

string Mykytea::getTagsToString(string str)
{
    KyteaSentence sentence = analyze(str);
    const KyteaSentence::Words & words = sentence.words;

    string ret_str;
    for(size_t i = 0; i < words.size(); i++) {
        ret_str += util->showString(words[i].surface);
        // Skipped tag levels are omitted, as in the kytea command output.
        for(size_t j = 0; j < words[i].tags.size(); j++) {
            if(words[i].tags[j].size() == 0)
                continue;
            ret_str += "/";
            ret_str += util->showString(words[i].tags[j][0].first);
        }
        ret_str += " ";
    }
    return ret_str;
}
