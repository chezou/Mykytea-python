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

vector<string>* Mykytea::getWS(string str){
    vector<string>* vec = new vector<string>;
    KyteaString surface_string = util->mapString(str);
    KyteaSentence sentence(surface_string, util->normalize(surface_string));
    kytea->calculateWS(sentence);

    const KyteaSentence::Words & words =  sentence.words;

    for(int i = 0; i < (int)words.size(); i++) {
         (*vec).push_back(util->showString(words[i].surface));
    }
    return vec;
}

vector<Tags>* Mykytea::getTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;

    KyteaString surface_string = util->mapString(str);
    KyteaSentence sentence(surface_string, util->normalize(surface_string));
    kytea->calculateWS(sentence);

    for(int i = 0; i < config->getNumTags(); i++)
        kytea->calculateTags(sentence,i);

    const KyteaSentence::Words & words =  sentence.words;

    for(int i = 0; i < (int)words.size(); i++) {
        tags vec_tag;
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            vector< pair<string, double> > vec_tmp;
            for(int k = 0; k < 1; k++) {
                vec_tmp.push_back( make_pair(util->showString(words[i].tags[j][k].first), words[i].tags[j][k].second) );
            }
            vec_tag.push_back( vec_tmp );
        }
        struct Tags t = { util->showString(words[i].surface), vec_tag };
        (*ret_words).push_back( t );
    }
    return ret_words;
}

vector<Tags>* Mykytea::getAllTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;

    KyteaString surface_string = util->mapString(str);
    KyteaSentence sentence(surface_string, util->normalize(surface_string));
    kytea->calculateWS(sentence);

    for(int i = 0; i < config->getNumTags(); i++)
        kytea->calculateTags(sentence,i);

    const KyteaSentence::Words & words =  sentence.words;

    for(int i = 0; i < (int)words.size(); i++) {
        tags vec_tag;
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            vector< pair<string, double> > vec_tmp;
            for(int k = 0; k < (int)words[i].tags[j].size(); k++) {
                vec_tmp.push_back( make_pair(util->showString(words[i].tags[j][k].first), words[i].tags[j][k].second) );
            }
            vec_tag.push_back( vec_tmp );
        }
        struct Tags t = { util->showString(words[i].surface), vec_tag };
        (*ret_words).push_back( t );
    }
    return ret_words;
}

string Mykytea::getTagsToString(string str)
{
    KyteaString surface_string = util->mapString(str);
    KyteaSentence sentence(surface_string, util->normalize(surface_string));
    kytea->calculateWS(sentence);

    for(int i = 0; i < config->getNumTags(); i++)
        kytea->calculateTags(sentence,i);

    const KyteaSentence::Words & words =  sentence.words;

    string ret_str;
    for(int i = 0; i < (int)words.size(); i++) {
        ret_str += util->showString(words[i].surface);
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            for(int k = 0; k < 1; k++) {
                ret_str += "/";
                ret_str += util->showString(words[i].tags[j][k].first);
            }
        }
        ret_str += " ";
    }
    return ret_str;
}
