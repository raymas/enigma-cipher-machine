import string
from .plugboard import Plugboard
from .rotor import Rotors
from .utils import Letter


class Machine:
    def __init__(
        self, name: str, rotors: list, plugboard: Plugboard, double_stepping=True
    ) -> None:
        self.name = name
        self.rotors = rotors
        self.plugboard = plugboard
        self.double_stepping = double_stepping

    def encode(self, sequence: str, split=5, debug=False) -> str:
        ret = ""
        for x in sequence:
            if x.lower() in string.ascii_lowercase:
                letter = Letter(x)
                j = [letter]

                # plugboard
                letter = self.plugboard.encode(letter)
                j.append(letter)

                self.rotate()

                # one way
                for rotor in self.rotors:
                    letter = rotor.encode(letter)
                    j.append(letter)

                # other way
                for rotor in reversed(self.rotors):
                    if not rotor.reflector:
                        letter = rotor.decode(letter)
                        j.append(letter)

                letter = self.plugboard.encode(letter)
                j.append(letter)

                ret += letter.letter

                # print(self)
                if debug:
                    print('->'.join(str(l) for l in j))

        if split > 0:
            ret = " ".join(ret[i : i + split] for i in range(0, len(ret), split))
        return ret

    def rotate(self):
        if self.double_stepping:
            self.rotate_double_stepping()
        else:
            self.rotate_normal()

    def rotate_double_stepping(self):
        rotors = list(filter(lambda r: r.can_rotate, self.rotors))
        assert len(rotors) == 3

        if self.rotors[2].position in self.rotors[2].turnovers:
            self.rotors[1].rotate()
            self.rotors[2].rotate()
            self.rotors[3].rotate()
        elif self.rotors[1].position in self.rotors[1].turnovers:
            self.rotors[1].rotate()
            self.rotors[2].rotate()
        else:
            self.rotors[1].rotate()

    def rotate_normal(self):
        for r, rotor in enumerate(self.rotors):
            if r == 0:
                rotor.rotate()

    def reset(self):
        for rotor in self.rotors:
            rotor.position = Letter("A")

    def set_position(self, position: list):
        position = list(reversed(position))
        assert len(position) == len(self.rotors)
        for rotor, p in zip(self.rotors, position):
            rotor.position = Letter(p)
    
    def get_position(self) -> list:
        positions = list(reversed(list(map(lambda r: r.position, filter(lambda r: r.can_rotate, self.rotors)))))
        return positions

    def set_ringstellung(self, ringstellung: list):
        ringstellung = list(reversed(ringstellung))
        assert len(ringstellung) == len(self.rotors)
        for rotor, p in zip(self.rotors, ringstellung):
            rotor.ringstellung = Letter(p)

    def get_ringstellung(self) -> list:
        return list(reversed(map(lambda r: r.ringstellung, self.rotors)))

    def set_rotor_position(self, name: str, position: str):
        for rotor in self.rotors:
            if rotor.name == name:
                rotor.position = Letter(position)

    def set_rotor_ringstellung(self, name: str, ringstellung: str):
        for rotor in self.rotors:
            if rotor.name == name:
                rotor.ringstellung = Letter(ringstellung)

    def __str__(self) -> str:
        rrotor = list(reversed(self.rotors))
        return (f"Enigma {self.name}\n"
                f"Rotors: {'-'.join([r.name for r in rrotor])}\n"
                f"Ringstellung: {'-'.join(str(r.ringstellung) for r in rrotor)}\n"
                f"Positions: {'-'.join(str(r.position) for r in rrotor)}\n"
                f"Plugboard: {str(self.plugboard)}")
