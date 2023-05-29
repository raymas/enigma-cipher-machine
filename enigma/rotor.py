from .utils import Letter


class Rotor:
    """Enigma rotor class"""

    def __init__(
        self,
        name: str,
        wiring: str,
        turnovers: str,
        reflector=False,
        position="A",
        ringstellung="A",
        rotate=True,
    ) -> None:
        self.name = name
        self.wiring = [Letter(wire) for wire in wiring]
        self.turnovers = [Letter(turnover) for turnover in turnovers]
        self.position = Letter(position)
        self.ringstellung = Letter(ringstellung)
        self.reflector = reflector
        self.can_rotate = rotate and not reflector

    def randomize(self):
        """Randomize the machine position"""
        self.position = Letter.random()
        self.ringstellung = Letter.random()

    def encode(self, letter: Letter):
        """From the plugboard to the reflector"""
        wiring_letter = letter + self.position - self.ringstellung
        offset = self.wiring[wiring_letter.index] - self.position + self.ringstellung
        return offset

    def decode(self, letter: Letter):
        """From the reflector to the plugboard"""
        wiring_letter = letter + self.position - self.ringstellung
        offset = Letter(self.wiring.index(wiring_letter)) - self.position + self.ringstellung
        return offset

    def rotate(self):
        """Rotate one time this rotor"""
        if not self.reflector and self.can_rotate:
            self.position += 1

    def __str__(self):
        return (f"{self.name}\n"
            f"Turnover: {''.join([str(t) for t in self.turnovers])}\n"
            f"Wiring: {''.join([str(w) for w in self.wiring])}\n"
            f"Position: {self.position}\n")


class Rotors:
    # M3 
    class M3:
        ETW     = Rotor("ETW", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "", rotate=False)
        I       = Rotor("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
        II      = Rotor("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
        III     = Rotor("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
        IV      = Rotor("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
        V       = Rotor("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
        VI      = Rotor("VI", "JPGVOUMFYQBENHZRDKASXLICTW", "ZM")
        VII     = Rotor("VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM")
        VIII    = Rotor("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM")
        UKWB    = Rotor("UKWB", "YRUHQSLDPXNGOKMIEBFZCWVJAT", "", reflector=True)
        UKWC    = Rotor("UKWC", "FVPJIAOYEDRZXWGCTKUQSBNMHL", "", reflector=True)

    class M4(M3):
        Beta    = Rotor("Beta", "LEYJVCNIXWPBQMDRTAKZGFUHOS", "", rotate=False)
        Gamma   = Rotor("Gamma", "FSOKANUERHMBTIYCWLQPZXVGJD", "", rotate=False)
        UKWB    = Rotor("UKWB", "ENKQAUYWJICOPBLMDXZVFTHRGS", "", reflector=True)
        UKWC    = Rotor("UKWC", "RDOBJNTKVEHMLFCWZAXGYIPSUQ", "", reflector=True)

