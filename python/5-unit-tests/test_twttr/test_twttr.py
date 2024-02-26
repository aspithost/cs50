from twttr import shorten


def test_vowels():
    assert shorten("test") == "tst"
    assert shorten("testje") == "tstj"


def test_novowels():
    assert shorten("www") == "www"
    assert shorten("https") == "https"


def test_capitalized():
    assert shorten("AbCDEf") == "bCDf"
    assert shorten("IAMtESt") == "MtSt"


def test_numbers():
    assert shorten("test123") == "tst123"


def test_punctuation():
    assert shorten("test./?") == "tst./?"