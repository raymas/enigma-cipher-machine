import random
import string
from .utils import Pair, Letter


class Plugboard:
    def __init__(self, pairs: str) -> None:
        pairs = pairs.split(" ")
        self.pairs = [Pair(*p) for p in pairs if p]

    def encode(self, x: Letter):
        for pair in self.pairs:
            ret = pair.get(x)
            if ret:
                return ret
        return x

    def active_len(self):
        return len(self.pairs)

    def randomize(self):
        alphabet = string.ascii_lowercase
        while self.active_len() < 10:
            a = random.choice(alphabet)
            alphabet = alphabet.replace(a, "")
            b = random.choice(alphabet)
            alphabet = alphabet.replace(b, "")
            self.pairs.append(Pair(a, b))

    def __str__(self):
        return " ".join(map(lambda p: str(p), self.pairs))
