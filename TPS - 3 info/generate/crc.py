# Aggiunta dinamica degli scripts
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
SCRIPT_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# Gestione del parametro --soluzioni
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--soluzioni", action="store_true")
args = parser.parse_args()

crc = [
    # ========================================================================
    # Difficolta 1: messaggio corto (4-8 bit), generatore max 4 bit (inizia con 1)
    # ========================================================================
    [1, "1101:101"],
    [1, "1011:110"],
    [1, "1110:101"],
    [1, "1001:111"],
    [1, "1100:101"],
    [1, "1010:101"],
    [1, "1111:1101"],
    [1, "1000:1011"],
    [1, "0110:1001"],
    [1, "0101:1101"],
    [1, "10101:1011"],

    # ========================================================================
    # Difficolta 2: messaggio medio (8-12 bit), generatore max 5 bit (inizia con 1)
    # ========================================================================
    [2, "1101001:1011"],
    [2, "1010100:1101"],
    [2, "1100110:1001"],
    [2, "1010111:1101"],
    [2, "1100100:1001"],
    [2, "10110011:1101"],
    [2, "11100110:1111"],
    [2, "10010110:10111"],
    [2, "11011001:10011"],

    # ========================================================================
    # Difficolta 3: messaggio lungo (12-16 bit), generatore max 6 bit (inizia con 1)
    # ========================================================================
    [3, "1101001100:10111"],
    [3, "1010101010:11011"],
    [3, "11110010000:10111"],
    [3, "10011011001:11001"],
    [3, "11011011011:10101"],
    [3, "101010101010:11001"],
    [3, "111100010000:10101"],
    [3, "100110011001:101111"],
]

from CRC import generateLatex


if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for s in crc:
    p, g = s[1].split(":")

    print("""\\begin{esercizio}[""" + str(s[0]) + """]
Parola : """ + p + """

Generatore : """ + g + """
""")
    if args.soluzioni:
        print("\\solution")
        print("")
        print(generateLatex(s[1]) + "\n")

    print("""\\end{esercizio}
""")

if not args.soluzioni:
    print("""\\end{multicols}
""")
