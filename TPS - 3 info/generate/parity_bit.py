# Aggiunta dinamica degli scripts
import sys
from pathlib import Path
BATE_DIR = Path(__file__).resolve().parents[2]
TCRIPT_DIR = BATE_DIR / "scripts"
sys.path.insert(0, str(TCRIPT_DIR))

# Gestione del parametro --soluzioni
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--soluzioni", action="store_true")
args = parser.parse_args()

parity = [
    # Difficoltà 1 (parola corta 4-8 bit, parità pari)
    [1, "1011 pari"],
    [1, "1100 pari"],
    [1, "0011 pari"],
    [1, "1111 pari"],
    [1, "1000 pari"],
    [1, "1110 pari"],
    [1, "0110 pari"],
    [1, "1001 pari"],
    [1, "1101 pari"],
    [1, "10111 pari"],

    # Difficoltà 2 (parola media 8-12 bit, parità pari o dispari)
    [2, "1011001 pari"],
    [2, "11001100 pari"],
    [2, "10101010 dispari"],
    [2, "11110000 dispari"],
    [2, "10011001 pari"],
    [2, "11010010 pari"],
    [2, "00111001 dispari"],
    [2, "10100111 pari"],
    [2, "11101010 dispari"],
    [2, "01010101 pari"],
    [2, "10010011 dispari"],
    [2, "01100110 pari"],
    [2, "11001101 dispari"],
    [2, "10111000 pari"],
    [2, "00101101 dispari"],

    # Difficoltà 3 (parola lunga 12-16 bit, parità pari o dispari)
    [3, "11010011101100 dispari"],
    [3, "10101010101010 pari"],
    [3, "1111000011110000 dispari"],
    [3, "1001100110011001 pari"],
    [3, "11011011011011 dispari"],
    [3, "1010110100110101 pari"],
    [3, "1110001110001110 dispari"],
    [3, "1001001100110011 pari"],
    [3, "0101010101010101 dispari"],
    [3, "1100110011001100 pari"],
    [3, "1011011011011011 dispari"],
    [3, "0011001100110011 pari"],
    [3, "1111111100000000 dispari"],
    [3, "1010101001010101 pari"],
    [3, "1100110000111100 dispari"],
]

from ParityBit import generateLatex


if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for s in parity:
    print("""\\begin{esercizio}[""" + str(s[0]) + """]
    """ + s[1])
    if args.soluzioni:
        print("\\solution")
        print("")
        print(generateLatex(s[1]) + "\n")

    print("""\\end{esercizio}
""")

if not args.soluzioni:
    print("""\\end{multicols}
""")
