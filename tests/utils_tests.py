import string
from enigma.utils import Letter, Pair


def test_letter_from_str():
    tests = []
    for i in range(26):
        character = string.ascii_lowercase[i]
        index = i
        tests.append({"letter": character, "index": index})

    for test in tests:
        letter = Letter(test["letter"])
        assert letter.letter == test["letter"] and letter.index == test["index"]


def test_letter_from_index():
    tests = []
    for i in range(26):
        character = string.ascii_lowercase[i]
        index = i
        tests.append({"letter": character, "index": index})

    for test in tests:
        letter = Letter(test["index"])
        assert letter.letter == test["letter"] and letter.index == test["index"]


def test_pairs():
    tests = [
        {"pair": {"A": "x", "B": "c"}, "off": "t"},
        {"pair": {"A": "r", "B": "t"}, "off": "g"},
        {"pair": {"A": "r", "B": "t"}, "off": "l"},
    ]

    for test in tests:
        p = test["pair"]
        pair = Pair(p["A"], p["B"])

        a = Letter(p["A"])
        b = Letter(p["B"])
        off = Letter(test["off"])

        assert(pair.get(a) == b and pair.get(b) == a and pair.get(off) == None)
