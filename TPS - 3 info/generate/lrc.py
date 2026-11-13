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

lrc = [
    # ========================================================================
    # Difficolta 1: 3-4 parole, valori decimali piccoli (0-127)
    # ========================================================================
    [1, "45,67,89"],
    [1, "12,34,56"],
    [1, "100,20,50"],
    [1, "10,20,30"],
    [1, "120,100,50"],
    [1, "5,15,25,35"],
    [1, "60,70,80"],
    [1, "1,2,3,4,5"],
    [1, "127,0,64"],
    [1, "33,66,99"],

    # ========================================================================
    # Difficolta 2: 5-6 parole, valori decimali medi (0-127)
    # ========================================================================
    [2, "45,67,89,12,34"],
    [2, "100,50,25,75,125"],
    [2, "10,20,30,40,50,60"],
    [2, "20,150,100,50,25"],
    [2, "7,14,21,28,35,42"],
    [2, "64,32,16,8,4,2"],
    [2, "127,64,32,16,8"],
    [2, "11,22,33,44,55,66"],
    [2, "90,80,70,60,50"],
    [2, "1,3,5,7,9,11"],

    # ========================================================================
    # Difficolta 3: 7-8 parole, valori decimali vari (0-127)
    # ========================================================================
    [3, "45,67,89,12,34,56,78"],
    [3, "100,50,25,75,125,10,20"],
    [3, "7,14,21,28,35,42,49,56"],
    [3, "64,32,16,8,4,2,1"],
    [3, "127,64,32,16,8,4,2,1"],
    [3, "11,22,33,44,55,66,77"],
    [3, "90,80,70,60,50,40,30"],
    [3, "1,3,5,7,9,11,13,15"],
]

from LRC import generateLatex


if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for s in lrc:
    expr = s[1]
    print("""\\begin{esercizio}[""" + str(s[0]) + """]
""" + expr.replace(",", ", ") + """
""")
    if args.soluzioni:
        print("\\solution")
        print("")
        print(generateLatex(expr) + "\n")

    print("""\\end{esercizio}
""")

if not args.soluzioni:
    print("""\\end{multicols}
""")
