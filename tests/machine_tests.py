from enigma.machine import Machine
from enigma.plugboard import Plugboard
from enigma.rotor import Rotors, Rotor
import string


def test_hello_world():
    tests = [
        {"entry": "hello world", "result": "fsqsj fusta"},
        {"entry": "xgytk npnkq ssnxw kyf", "result": "alanm athis ontur ing"},
    ]

    for test in tests:
        p = Plugboard("qd fe rw jn il ps cm ax kg yu")

        M3 = Machine(
            "M3",
            [Rotors.M3.ETW, Rotors.M3.I, Rotors.M3.II, Rotors.M3.III, Rotors.M3.UKWC],
            p,
        )

        M3.set_rotor_position("I", "A")
        M3.set_rotor_position("II", "B")
        M3.set_rotor_position("III", "C")

        M3.set_rotor_ringstellung("I", "D")
        M3.set_rotor_ringstellung("II", "E")
        M3.set_rotor_ringstellung("III", "F")

        ciphertext = M3.encode(test["entry"])

        assert ciphertext == test["result"]

        M3.reset()

        M3.set_rotor_position("I", "A")
        M3.set_rotor_position("II", "B")
        M3.set_rotor_position("III", "C")

        M3.set_rotor_ringstellung("I", "D")
        M3.set_rotor_ringstellung("II", "E")
        M3.set_rotor_ringstellung("III", "F")

        plaintext = M3.encode(test["result"])

        assert plaintext == test["entry"]


def test_decode_M4_U534():
    # decode this : https://www.cryptomuseum.com/crypto/enigma/msg/p1030681.htm

    plugboard = Plugboard("AE BF CM DQ HU JN LX PR SZ VW")

    M4 = Machine(
        "M4",
        [
            Rotors.M4.ETW,
            Rotors.M4.VIII,
            Rotors.M4.VI,
            Rotors.M4.V,
            Rotors.M4.Beta,
            Rotors.M4.UKWC,
        ],
        plugboard,
    )

    M4.set_rotor_position("Beta", "C")
    M4.set_rotor_position("V", "D")
    M4.set_rotor_position("VI", "S")
    M4.set_rotor_position("VIII", "Z")

    M4.set_rotor_ringstellung("Beta", "E")
    M4.set_rotor_ringstellung("V", "P")
    M4.set_rotor_ringstellung("VI", "E")
    M4.set_rotor_ringstellung("VIII", "L")

    print(M4)

    ciphertext = """LANO TCTO UARB BFPM HPHG CZXT DYGA HGUF XGEW KBLK GJWL QXXT
   GPJJ AVTO CKZF SLPP QIHZ FXOE BWII EKFZ LCLO AQJU LJOY HSSM BBGW HZAN
   VOII PYRB RTDJ QDJJ OQKC XWDN BBTY VXLY TAPG VEAT XSON PNYN QFUD BBHH
   VWEP YEYD OHNL XKZD NWRH DUWU JUMW WVII WZXI VIUQ DRHY MNCY EFUA PNHO
   TKHK GDNP SAKN UAGH JZSM JBMH VTRE QEDG XHLZ WIFU SKDQ VELN MIMI THBH
   DBWV HDFY HJOQ IHOR TDJD BWXE MEAY XGYQ XOHF DMYU XXNO JAZR SGHP LWML
   RECW WUTL RTTV LBHY OORG LGOW UXNX HMHY FAAC QEKT HSJW"""

    plaintext = M4.encode(ciphertext, split=0, debug=False)

    assert (
        plaintext
        == """krkrallexxfolgendesistsofortbekanntzugebenxxichhabefolgelnbebefehlerhaltenxxjansterledesbisherigxnreichsmarschallsjgoeringjsetztderfuehrersieyhvrrgrzssadmiralyalsseinennachfolgereinxschriftlschevollmachtunterwegsxabsofortsollensiesaemtlichemassnahmenverfuegenydiesichausdergegenwaertigenlageergebenxgezxreichsleiteikktulpekkjbormannjxxobxdxmmmdurnhfkstxkomxadmxuuubooiexkp"""
    )


def test_double_stepping():
    plugboard = Plugboard("")

    M3 = Machine(
        "M3",
        [Rotors.M3.ETW, Rotors.M3.I, Rotors.M3.II, Rotors.M3.III, Rotors.M3.UKWC],
        plugboard,
    )

    M3.set_rotor_position("I", "Q")
    M3.set_rotor_position("II", "D")
    M3.set_rotor_position("III", "A")

    M3.encode("aaa")  # three rotation

    rotors = M3.get_position()

    assert (
        rotors[0].letter == "b" and rotors[1].letter == "f" and rotors[2].letter == "t"
    )


# http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
def test_decode_M3_manual():
    M3 = Machine(
        "M3",
        [
            Rotors.M3.ETW,
            Rotors.M3.III,
            Rotors.M3.I,
            Rotors.M3.II,
            Rotor("UKWA", "EJMZALYXVBWFCRQUONTSPIKHGD", "", reflector=True),
        ],
        Plugboard("AM FI NV PS TU WZ"),
    )

    M3.set_rotor_position("II", "A")
    M3.set_rotor_position("I", "B")
    M3.set_rotor_position("III", "L")

    M3.set_rotor_ringstellung("II", string.ascii_lowercase[24 - 1])
    M3.set_rotor_ringstellung("I", string.ascii_lowercase[13 - 1])
    M3.set_rotor_ringstellung("III", string.ascii_lowercase[22 - 1])

    plaintext = M3.encode(
        "GCDSE AHUGW TQGRK VLFGX UCALX VYMIG MMNMF DXTGN VHVRM MEVOU YFZSL RHDRR XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ",
        split=0,
    )

    assert (
        plaintext
        == "feindliqeinfanteriekolonnebeobaqtetxanfangsuedausgangbaerwaldexendedreikmostwaertsneustadt"
    )


def test_decode_enigma_K():
    K = Machine(
        "K",
        [
            Rotor("ETWK", "QWERTZUIOASDFGHJKPYXCVBNML", "", rotate=False),
            Rotor("KII", "CJGDPSHKTURAWZXFMYNQOBVLIE", "N"),
            Rotor("KI", "LPGSZMHAEOQKVXRFYBUTNICJDW", "Y"),
            Rotor("KII", "CJGDPSHKTURAWZXFMYNQOBVLIE", "N"),
            Rotor("UKWK", "IMETCGFRAYSQBZXWLHKDVUPOJN", "", reflector=True),
        ],
        Plugboard(""),
    )

    # 26 17 16 13
    K.set_rotor_ringstellung("KII", string.ascii_lowercase[13 - 1])
    K.set_rotor_ringstellung("KI", string.ascii_lowercase[16 - 1])
    K.set_rotor_ringstellung("KIII", string.ascii_lowercase[17 - 1])
    K.set_rotor_ringstellung("UKWK", string.ascii_lowercase[26 - 1])

    plaintext = K.encode("QSZVI DVMPN EXACM RWWXU IYOTY NGVVX DZ---", split=0)

    assert(
        plaintext == ""
    )
