from enigma.plugboard import Plugboard

def test_plugboard_init():
    tests = [
        {
            "sequence": "AB CD EF",
            "len": 3
        }
    ]

    for test in tests:
        p = Plugboard(test["sequence"])

        assert(p.active_len() == test["len"])

def test_plugboard_init_random():
    p = Plugboard("")
    p.randomize()

    assert(p.active_len() == 10)
