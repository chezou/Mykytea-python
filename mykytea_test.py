#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

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

def list_tags(t):
    def convert(t2):
        return (t2[0], type(t2[1]))
    return [(word.surface, [[convert(t2) for t2 in t1] for t1 in word.tag]) for word in t]

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

class SimpleTest(unittest.TestCase):
    """最低限のテスト"""

    def test_word_separation(self):
        """分かち書きを取得"""
        self.assertEqual(
            [elem for elem in mk.getWS(s)],
            ['今日', 'は', 'い', 'い', '天気', 'で', 'す', '。', '1999'])

    def test_as_string(self):
        """解析結果を文字列で取得"""
        self.assertEqual(mk.getTagsToString(s),
                         '今日/名詞/きょう は/助詞/は い/形容詞/い い/語尾/い 天気/名詞/てんき で/助動詞/で す/語尾/す 。/補助記号/。 1999/名詞/１９９９ ')
        
    def test_get_tags(self):
        """1位のタグを取得"""
        self.assertEqual(list_tags(mk.getTags(s)),
                         [('今日', [[('名詞', float)], [('きょう', float)]]),
                          ('は', [[('助詞', float)], [('は', float)]]),
                          ('い', [[('形容詞', float)], [('い', float)]]),
                          ('い', [[('語尾', float)], [('い', float)]]),
                          ('天気', [[('名詞', float)], [('てんき', float)]]),
                          ('で', [[('助動詞', float)], [('で', float)]]),
                          ('す', [[('語尾', float)], [('す', float)]]),
                          ('。', [[('補助記号', float)], [('。', float)]]),
                          ('1999', [[('名詞', float)], [('１９９９', float)]])])

    def test_get_all_tags(self):
        """すべてのタグを取得"""
        self.assertEqual(list_tags(mk.getAllTags(s)),
                         [('今日', [[('名詞', float),
                                     ('ローマ字文', float),
                                     ('代名詞', float)],
                                    [('きょう', float),
                                     ('こんにち', float)]]),
                          ('は', [[('助詞', float),
                                   ('ローマ字文', float),
                                   ('言いよどみ', float)],
                                  [('は', float)]]),
                          ('い', [[('形容詞', float),
                                   ('動詞', float),
                                   ('ローマ字文', float)],
                                  [('い', float)]]),
                          ('い', [[('語尾', float),
                                   ('ローマ字文', float),
                                   ('接頭辞', float)],
                                  [('い', float)]]),
                          ('天気', [[('名詞', float),
                                     ('ローマ字文', float),
                                     ('代名詞', float)],
                                    [('てんき', float)]]),
                          ('で', [[('助動詞', float),
                                   ('ローマ字文', float),
                                   ('空白', float)],
                                  [('で', float),
                                   ('らで', float)]]),
                          ('す', [[('語尾', float),
                                   ('ローマ字文', float),
                                   ('助詞', float)],
                                  [('す', float),
                                   ('やす', float)]]),
                          ('。', [[('補助記号', float),
                                   ('ローマ字文', float),
                                   ('空白', float)],
                                  [('。', float)]]),
                          ('1999', [[('名詞', float),
                                     ('補助記号', float),
                                     ('URL', float)],
                                    [('１９９９', float)]])])


if __name__ == '__main__':
    unittest.main()
