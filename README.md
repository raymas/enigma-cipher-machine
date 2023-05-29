# Enigma

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Enigma-logo.jpg" alt="Engima logo" />
</p>

The enigma machine in python.

## The Machine

Built by the German Scherbius & Ritter company in the early 20th century, the enigma machine is a cipher machine. The machine performs substitution : it encodes a letter from the alphabet to another one.

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/Enigma_%28crittografia%29_-_Museo_scienza_e_tecnologia_Milano.jpg" alt="Engima machine" height="400"/>
</p>

The machine is composed of the following elements:

- a keyboard for user input
- multiple rotors which are rotating parts that perform the cipher operation using a scrambled electrical wiring
- a front panel plugboard to allow additionnal substitution making the deciphering operation insanely more difficult (over 150,738,274,937,250 additionnal substitutions using 10 pairs)
- a light panel with 26 lamps labeled from A to Z.

The cipher process can be described as follow :

Keyboard -> Plugboard -> Entry Wheel -> Rotors (from 1 to x) -> Reflector -> Rotors (from x to 1) -> Entry Wheel -> Plugboard -> Light Panel

The user press a letter on the keyboard making the first rotor to rotate. The keyboard press close an electrical circuit, allowing the current to enter the plugboard, the entry wheel, each rotor and the reflector (a non rotating wheel). From there the electrical current makes it way back to the light panel, lighting up the alphabet letter corresponding to the cipher letter.

### Rotors

Rotors are the rotating part of the enigma machine. Most machines contains three of them but an additionnal one can be found (e.g. M4 variant for the Kriegsmarine with the _greek_ wheel).

Rotors' positions are numbered from A to Z and possess turnovers positions. When a rotor reach a turnover position, it rotates its closest neighbour.

Rotors' internal wiring can be shifted prior any operation by rotating a ring to a certain position. This setting is often called the _Ringstellung_.

The wiring pattern is usely represented with an alphabeter string. Each alphabet chacracter is replaced by the corresponding letter in the string. For instance the string: **EKMFLGDQVZNTOWYHXUSPAIBRCJ** means that a **A** substitute to an **E**, a **B** to an **K** and so on. The same logic applies for the remaining character as shown below.

```
ABCDEFGHIJKLMNOPQRSTUVWXYZ      keyboard    reflector  
||||||||||||||||||||||||||         ↓            ↑
EKMFLGDQVZNTOWYHXUSPAIBRCJ      reflector   keyboard
```

On each rotor increment, we rotate the alphabet by one (please pay attention to the position of the letter A):

```
BCDEFGHIJKLMNOPQRSTUVWXYZA
||||||||||||||||||||||||||
EKMFLGDQVZNTOWYHXUSPAIBRCJ
```

Moving the ring to a B position is equivalent to the inverse of a rotation.

```
ZABCDEFGHIJKLMNOPQRSTUVWXY
||||||||||||||||||||||||||
EKMFLGDQVZNTOWYHXUSPAIBRCJ
```

We can represent the shift with the following equations:

From the keyboard to the reflector (alphabet to rotor's wiring)
```
wiring_letter = letter + position - ringstellung
cipher_letter = wire.at(wiring_letter) - position + ringstellung
```

From the reflector to the light panel (rotor's wiring to alphabet)
```
wiring_letter = letter + position - rinsgtellung
cipher_letter = wire.index(wiring_letter) - position + ringstellung
```

The reflector is considered as a one-way (keyboard to reflector), non rotating "rotor".

Enigma machines that use a lever suffers an abnormal rotation when the center rotor reaches its turnover position, all the rotors are increment one step further.
Let's illustrate this anomaly.

- Rotor I turnover position is Q : if reached Rotor II increment,
- Rotor II turnover position  is E : if reached Rotor III increment.

We setup the machine to the A-D-Q position and we increment the Rotor I.

Expected rotation:

| III | II  |  I  |
|-----|-----|-----|
|  A  |  D  |  Q  |
|  A  |  E  |  R  |
|  A  |  E  |  S  |

Double stepping rotation:

| III | II  |  I  |
|-----|-----|-----|
|  A  |  D  |  Q  |
|  A  |  E  |  R  |
|  B  |  F  |  S  |

Rotor III, II and I increment. This software enables double stepping rotation by default as it was present on the M3 and M4 machine. You can desactivate this behaviour by setting `double_stepping=False` in the [Machine constructor](enigma/machine.py).

### Plugboard

The plugboard is a front panel with 26 electrical sockets. A male-male cable is used to connect letters between them. 10 connections (20 pairs) is a common setup.

An AB pair will substitute every A to B and every B to an A.

We use this notation : `AE BF CM DQ HU JN LX PR SZ VW`. Every pairs are space separated.

### Example

We use the M3 machine and the following setup:

| Object        | Value                             |
|---------------|-----------------------------------|
| Reflector     | C                                 |
| Rotors        | III-II-I                          |
| Positions     | A-B-C                             |
| Ringstellung  | D-E-F                             |
| Plugboard     | qd fe rw jn il ps cm ax kg yu     |
| Text          | Hello world                       |

The enigma produces: ```fsqsj fusta```


## Getting started

Get the library: 

```python
pip install enigma-machine
```

We use pure python, no dependency required and tested on python 3.10.6.

To run tests please install **pytest**.

## Usage

We want to decode the following message: `xgytk npnkq ssnxw kyf` with the settings extracted from the above example.

Start by initialise a plugboard, A plugboard object contains from 0 to 10 pairs of letters. A letter can only appears one time in the plugboard.

```python
from enigma.plugboard import Plugboard

plugboard = Plugboard("qd fe rw jn il ps cm ax kg yu")
```

Then make the machine using the predefined rotors (see below if you want to create yours).

```python
from enigma.rotor import Rotors
from enigma.machine import Machine

M3 = Machine(
    "M3",
    [
        Rotors.M3.ETW,
        Rotors.M3.I,
        Rotors.M3.II,
        Rotors.M3.III,
        Rotors.M3.UKWC
    ],
    plugboard
)

```

Now set the positions and the ringstellung:

```python
M3.set_rotor_position("I", "A")
M3.set_rotor_position("II", "B")
M3.set_rotor_position("III", "C")

M3.set_rotor_ringstellung("I", "D")
M3.set_rotor_ringstellung("II", "E")
M3.set_rotor_ringstellung("III", "F")
```

And then provide the input text (split is optionnal it adds an additionnal space every n character):

```python
plaintext = M3.encode("xgytk npnkq ssnxw kyf", split=0)
print(plaintext)
>> alanmathisonturing
```


Here is a full example using a M4 enigma machine with double stepping. We are decoding a real world message sent by GrossAdmiral Donitz on the 1st May 1945.

```python
from enigma.machine import Machine
from enigma.plugboard import Plugboard
from enigma.rotor import Rotors

plugboard = Plugboard("AE BF CM DQ HU JN LX PR SZ VW")

M4 = Machine(
    "M4",
    [
        Rotors.M4.ETW,
        Rotors.M4.VIII,
        Rotors.M4.VI,
        Rotors.M4.V,
        Rotors.M4.Beta,
        Rotors.M4.UKWC
    ],
    plugboard
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

print(plaintext)
```

The machine returns :
```
krkrallexxfolgendesistsofortbekanntzugebenxxichhabefolgelnbebefehlerhaltenxxjansterledesbisherigxnreichsmarschallsjgoeringjsetztderfuehrersieyhvrrgrzssadmiralyalsseinennachfolgereinxschriftlschevollmachtunterwegsxabsofortsollensiesaemtlichemassnahmenverfuegenydiesichausdergegenwaertigenlageergebenxgezxreichsleiteikktulpekkjbormannjxxobxdxmmmdurnhfkstxkomxadmxuuubooiexkp
```

After formating
```
krkr alle xx 
folgendes ist sofort bekanntzugeben xx 
ich habe folgelnbe befehl erhalten xx 
j ansterle des bisherigxn reichsmarschalls j goering j setzt der fuehrer sie y hvrr grzssadmiral y als seinen nachfolger ein x schriftlsche vollmacht unterwegs x absofort sollen sie saemtliche massnahmen verfuegen y die sich aus der gegenwaertigen lage ergeben x gez x reichsleitei kk tulpe kk j bormann j xx
ob x d x mmm durnh fkst x kom x adm x uuu booie x kp
```

Please see [cryptomuseum.com](https://www.cryptomuseum.com/crypto/enigma/msg/p1030681.htm) for more.

## Going further

You can create additionnal rotors by using the `Rotor` class from the `enigma.rotor` package.

A plugboard object contains from 0 to 10 pairs of letters. A letter can only appears one time in the plugboard.

```python
from enigma.plugboard import Plugboard

plugboard = Plugboard("AE BF CM DQ HU JN LX PR SZ VW")
```

You can also randomise the plugboard:

```python
plugboard.randomise()
```


A Rotor object requires an unique name, the wiring sequence containing every letter of the alphabet (len(wiring) == 26) and the turnover positions. See [rotor.py](enigma/rotor.py) for the full api description.

```python
from enigma.rotor import Rotor

# Commercial Enigma A27 wiring
KI = Rotor(
    "KI",                           #name
    "LPGSZMHAEOQKVXRFYBUTNICJDW",   # wiring
    "Y"                             # turnover
)

KII = Rotor(
    "KII",
    "SLVGBTFXJQOHEWIRZYAMKPCNDU",
    "E"
)

KIII = Rotor(
    "KII",
    "CJGDPSHKTURAWZXFMYNQOBVLIE",
    "N"
)

ETWK = Rotor(
    "ETWK",
    "QWERTZUIOASDFGHJKPYXCVBNML",
    "",
    rotate=False                    # no rotation for an entry wheel
)

UKWK = Rotor(
    "UKWK",
    "IMETCGFRAYSQBZXWLHKDVUPOJN",
    "",
    reflector=True                  # this rotor is a reflector
)
```

A machine object requires a name, a list of rotors (starting from the entry wheel to the reflector) and a plugboard.

```python
from enigma.machine import Machine

EK = Machine(
    "K-A27",
    [
        ETWK,
        KI,
        KII,
        KIII,
        UKWK
    ],
    plugboard
)
```

## TODO

- [ ] set_rotor_position and set_rotor_ringstellung even if the rotor shares the same name

## Licence 

MIT of course.
