// mykytea.cpp
#include <iostream>
#include "mykytea.hpp"


Mykytea::Mykytea(char* str)
{
    kytea.readModel(str);
    util = kytea.getStringUtil(); 

    // 設定クラスKyteaConfigは様々な設定を格納する
    config = kytea.getConfig();

}

Mykytea::~Mykytea()
{
}

vector<string>* Mykytea::getWS(string str){
    vector<string>* vec = new vector<string>;

    // 一文を表すオブジェクトを作る
    KyteaSentence sentence(util->mapString(str));

    // 単語境界を推定する
    kytea.calculateWS(sentence);

    // 各単語に対して
    const KyteaSentence::Words & words =  sentence.words;


    for(int i = 0; i < (int)words.size(); i++) {
        // 単語を出力する
         (*vec).push_back(util->showString(words[i].surf));
    }
    return vec;
}

vector<Tags>* Mykytea::getTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;

    // 一文を表すオブジェクトを作る
    KyteaSentence sentence(util->mapString(str));

    // 単語境界を推定する
    kytea.calculateWS(sentence);

    // 各タグ種類に対してタグ付与を行う
    for(int i = 0; i < config->getNumTags(); i++)
        kytea.calculateTags(sentence,i);

    // 各単語に対して
    const KyteaSentence::Words & words =  sentence.words;

    for(int i = 0; i < (int)words.size(); i++) {
        tags vec_tag;
        // 各タグ種に対して
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            //cout << "\t";
            // タグと信頼度を出力
            vector< pair<string, double> > vec_tmp;
            //for(int k = 0; k < (int)words[i].tags[j].size(); k++) {
            for(int k = 0; k < 1; k++) {
                vec_tmp.push_back( make_pair(util->showString(words[i].tags[j][k].first), words[i].tags[j][k].second) );
            }
            vec_tag.push_back( vec_tmp );
        }
        struct Tags t = { util->showString(words[i].surf), vec_tag };
        (*ret_words).push_back( t );
    }
    return ret_words;
}

vector<Tags>* Mykytea::getAllTags(string str){
    vector<Tags>* ret_words = new vector<Tags>;

    // 一文を表すオブジェクトを作る
    KyteaSentence sentence(util->mapString(str));

    // 単語境界を推定する
    kytea.calculateWS(sentence);

    // 各タグ種類に対してタグ付与を行う
    for(int i = 0; i < config->getNumTags(); i++)
        kytea.calculateTags(sentence,i);

    // 各単語に対して
    const KyteaSentence::Words & words =  sentence.words;

    for(int i = 0; i < (int)words.size(); i++) {
        tags vec_tag;
        // 各タグ種に対して
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            //cout << "\t";
            // タグと信頼度を出力
            vector< pair<string, double> > vec_tmp;
            for(int k = 0; k < (int)words[i].tags[j].size(); k++) {
                vec_tmp.push_back( make_pair(util->showString(words[i].tags[j][k].first), words[i].tags[j][k].second) );
            }
            vec_tag.push_back( vec_tmp );
        }
        struct Tags t = { util->showString(words[i].surf), vec_tag };
        (*ret_words).push_back( t );
    }
    return ret_words;
}

string Mykytea::getTagsToString(string str)
{
    // 一文を表すオブジェクトを作る
    KyteaSentence sentence(util->mapString(str));

    // 単語境界を推定する
    kytea.calculateWS(sentence);

    // 各タグ種類に対してタグ付与を行う
    for(int i = 0; i < config->getNumTags(); i++)
        kytea.calculateTags(sentence,i);

    // 各単語に対して
    const KyteaSentence::Words & words =  sentence.words;

    string ret_str;
    for(int i = 0; i < (int)words.size(); i++) {
        ret_str += util->showString(words[i].surf);
        // 各タグ種に対して
        for(int j = 0; j < (int)words[i].tags.size(); j++) {
            //cout << "\t";
            // タグを出力
            for(int k = 0; k < 1; k++) {
                ret_str += "/";
                ret_str += util->showString(words[i].tags[j][k].first);
            }
        }
        ret_str += " ";
    }
    return ret_str;
  
}
