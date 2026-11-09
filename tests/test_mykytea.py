"""Tests for the Mykytea extension. They need a KyTea model (see conftest.py)."""

import pytest

S = "今日はいい天気です。1999"


def list_tags(words):
    def convert(tag):
        return (tag[0], type(tag[1]))

    return [(w.surface, [[convert(t) for t in level] for level in w.tag]) for w in words]


def test_import():
    import _Mykytea  # noqa: F401


class TestAnalysis:
    def test_word_separation(self, mk):
        assert list(mk.getWS(S)) == ["今日", "は", "い", "い", "天気", "で", "す", "。", "1999"]

    def test_as_string(self, mk):
        assert mk.getTagsToString(S) == (
            "今日/名詞/きょう は/助詞/は い/形容詞/い い/語尾/い 天気/名詞/てんき "
            "で/助動詞/で す/語尾/す 。/補助記号/。 1999/名詞/１９９９ "
        )

    def test_get_tags(self, mk):
        assert list_tags(mk.getTags(S)) == [
            ("今日", [[("名詞", float)], [("きょう", float)]]),
            ("は", [[("助詞", float)], [("は", float)]]),
            ("い", [[("形容詞", float)], [("い", float)]]),
            ("い", [[("語尾", float)], [("い", float)]]),
            ("天気", [[("名詞", float)], [("てんき", float)]]),
            ("で", [[("助動詞", float)], [("で", float)]]),
            ("す", [[("語尾", float)], [("す", float)]]),
            ("。", [[("補助記号", float)], [("。", float)]]),
            ("1999", [[("名詞", float)], [("１９９９", float)]]),
        ]

    def test_get_all_tags(self, mk):
        assert list_tags(mk.getAllTags(S)) == [
            ("今日", [[("名詞", float), ("ローマ字文", float), ("代名詞", float)],
                      [("きょう", float), ("こんにち", float)]]),
            ("は", [[("助詞", float), ("ローマ字文", float), ("言いよどみ", float)],
                    [("は", float)]]),
            ("い", [[("形容詞", float), ("動詞", float), ("ローマ字文", float)],
                    [("い", float)]]),
            ("い", [[("語尾", float), ("ローマ字文", float), ("接頭辞", float)],
                    [("い", float)]]),
            ("天気", [[("名詞", float), ("ローマ字文", float), ("代名詞", float)],
                      [("てんき", float)]]),
            ("で", [[("助動詞", float), ("ローマ字文", float), ("空白", float)],
                    [("で", float), ("らで", float)]]),
            ("す", [[("語尾", float), ("ローマ字文", float), ("助詞", float)],
                    [("す", float), ("やす", float)]]),
            ("。", [[("補助記号", float), ("ローマ字文", float), ("空白", float)],
                    [("。", float)]]),
            ("1999", [[("名詞", float), ("補助記号", float), ("URL", float)],
                      [("１９９９", float)]]),
        ]

    def test_empty_input(self, mk):
        assert list(mk.getWS("")) == []
        assert mk.getTagsToString("") == ""


class TestOptions:
    def test_kwargs_same_as_string(self, new, mk):
        mk_kwargs = new(deftag="UNKNOWN!!")
        assert list(mk_kwargs.getWS(S)) == list(mk.getWS(S))
        assert mk_kwargs.getTagsToString(S) == mk.getTagsToString(S)

    def test_list_option(self, new, mk):
        mk_list = new(["-deftag", "UNKNOWN!!"])
        assert mk_list.getTagsToString(S) == mk.getTagsToString(S)

    def test_unknown_keyword(self, Mykytea):
        with pytest.raises(TypeError, match="no_such_option"):
            Mykytea.Mykytea(no_such_option=True)

    def test_missing_model(self, Mykytea, tmp_path):
        with pytest.raises(RuntimeError):
            Mykytea.Mykytea(model=tmp_path / "no such model.bin")


class TestTagOptions:
    """-notags and -notag are honored, as by the kytea command."""

    def test_notags(self, new, mk):
        mk_ws = new(notags=True)
        assert list(mk_ws.getWS(S)) == list(mk.getWS(S))
        assert [list(w.tag) for w in mk_ws.getTags(S)] == [[] for _ in mk.getWS(S)]
        assert [list(w.tag) for w in mk_ws.getAllTags(S)] == [[] for _ in mk.getWS(S)]
        assert mk_ws.getTagsToString(S) == " ".join(mk.getWS(S)) + " "

    def test_notag_first(self, new):
        mk_pron = new(notag=1)
        assert mk_pron.getTagsToString("今日は") == "今日/きょう は/は "
        for word in mk_pron.getAllTags("今日は"):
            assert len(word.tag[0]) == 0
            assert len(word.tag[1]) > 0

    def test_notag_second(self, new):
        mk_pos = new(notag=2)
        assert mk_pos.getTagsToString("今日は") == "今日/名詞 は/助詞 "
        assert list_tags(mk_pos.getTags("今日は")) == [
            ("今日", [[("名詞", float)], []]),
            ("は", [[("助詞", float)], []]),
        ]

    def test_notag_all(self, new, mk):
        mk_none = new(notag=[1, 2])
        assert mk_none.getTagsToString(S) == " ".join(mk.getWS(S)) + " "


class TestNoWordSegmentation:
    """With -nows the input is already segmented, as with kytea -nows -in tok."""

    def test_getWS_splits_on_spaces(self, new):
        mk_tok = new(nows=True)
        assert list(mk_tok.getWS("今日 は  天気")) == ["今日", "は", "天気"]
        assert list(mk_tok.getWS(" 今日 ")) == ["今日"]
        assert list(mk_tok.getWS("")) == []

    def test_keeps_given_words(self, new):
        # Without -nows KyTea would segment いい into い/い (see TestAnalysis).
        mk_tok = new(nows=True)
        assert list(mk_tok.getWS("今日 は いい 天気")) == ["今日", "は", "いい", "天気"]

    def test_tags_given_words(self, new, mk):
        mk_tok = new(nows=True)
        segmented = " ".join(mk.getWS(S))
        assert mk_tok.getTagsToString(segmented) == mk.getTagsToString(S)
        assert [w.surface for w in mk_tok.getTags(segmented)] == list(mk.getWS(S))

    def test_custom_word_boundary(self, new):
        mk_tok = new("-nows -wordbound |")
        assert list(mk_tok.getWS("今日|は|天気")) == ["今日", "は", "天気"]


class TestBuildArgs:
    """Conversion of Mykytea() arguments to a KyTea argv."""

    @pytest.fixture
    def build(self, Mykytea):
        return lambda opt="", **options: Mykytea._build_args(opt, options)

    def test_empty(self, build):
        assert build() == []

    def test_string(self, build):
        assert build("-deftag UNK  -nounk") == ["-deftag", "UNK", "-nounk"]

    def test_list_keeps_spaces(self, build):
        assert build(["-model", "a b.bin"]) == ["-model", "a b.bin"]

    def test_flags(self, build):
        assert build(nows=True, notags=False, nounk=True) == ["-nows", "-nounk"]

    def test_values(self, build):
        assert build(deftag="UNK", unkbeam=0, debug=None) == ["-deftag", "UNK", "-unkbeam", "0"]

    def test_model_pathlike(self, build, tmp_path):
        path = tmp_path / "dir with space" / "model.bin"
        assert build(model=path) == ["-model", str(path)]

    def test_notag(self, build):
        assert build(notag=2) == ["-notag", "2"]
        assert build(notag=[1, 2]) == ["-notag", "1", "-notag", "2"]

    def test_kwargs_after_string(self, build):
        assert build("-deftag A", deftag="B") == ["-deftag", "A", "-deftag", "B"]
