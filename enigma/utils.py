import string
import random


class Letter:
    """Letter class : contains the string representation of a letter and its position in the alphabet"""
    def __init__(self, y) -> None:
        if isinstance(y, str):
            self.letter = y.lower()
            self.index = Letter.a2i(self.letter)
        elif isinstance(y, int):
            self.index = y
            self.letter = Letter.i2a(y)
        else:
            raise ValueError("Not Implemented")

    def __add__(self, y):
        q = self.get_type(y)
        x = (26 + self.index + q) % 26
        return Letter(string.ascii_lowercase[x])

    def __sub__(self, y):
        q = self.get_type(y)
        x = (26 + self.index - q) % 26
        return Letter(string.ascii_lowercase[x])

    def __eq__(self, y):
        return self.letter == y.letter

    def __str__(self):
        return self.letter

    def get_type(self, y):
        if isinstance(y, Letter):
            q = y.index
        else:
            q = y
        return q

    @staticmethod
    def random():
        return Letter(random.choice(string.ascii_lowercase))

    @staticmethod
    def a2i(a: str) -> int:
        return string.ascii_lowercase.find(a)

    @staticmethod
    def i2a(i: int) -> str:
        return string.ascii_lowercase[i]


class Pair:
    """A Plugboard pair"""
    def __init__(self, A: str, B: str) -> None:
        self.a = Letter(A)
        self.b = Letter(B)

    def get(self, x: Letter) -> Letter:
        if self.a == x:
            return self.b
        elif self.b == x:
            return self.a
        else:
            return None

    def __str__(self):
        return f"{self.a}{self.b}"
