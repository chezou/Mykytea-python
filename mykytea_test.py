#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Mykytea

def showTags(t):
    for word in t:
        out = word.surface + "\t"
        for t1 in word.tag:
            for t2 in t1:
                for t3 in t2:
                    out = out + "/" + str(t3)
                out += "\t"
            out += "\t"
        print out


opt = "-model /usr/local/share/kytea/model.bin -deftag UNKNOWN!!"
mk = Mykytea.Mykytea(opt)

s = "今日はいい天気です。1999"

#分かち書きを取得
for word in mk.getWS(s):
    print word

#解析結果を文字列で取得
print mk.getTagsToString(s)

#1位のタグを取得
t = mk.getTags(s)
showTags(t)

#すべてのタグを取得
tt = mk.getAllTags(s)
showTags(tt)
