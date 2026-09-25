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

# Ogni esercizio e' una lista di tre elementi:
#   [difficolta, "ALGORITMO,NUMERO_FRAME", "RIF1,RIF2,...,RIFn"]
esercizi = [
    # =========================
    # Difficolta 1
    # Pochi riferimenti e pochi frame
    # =========================

    [1, "FIFO,3", "1,2,3,4,1,2,5,1,2"],
    [1, "LRU,3", "1,2,1,3,1,4,1,5,1"],
    [1, "OPT,3", "7,0,1,2,0,3,0,4,2"],
    [1, "FIFO,4", "1,2,3,1,4,5,2,1"],
    [1, "LRU,4", "2,3,2,1,5,2,4,5"],

    # =========================
    # Difficolta 2
    # Sequenze piu' lunghe e algoritmi diversi
    # =========================

    [2, "LRU,3", "1,2,3,4,1,2,5,1,2,3,4,5"],
    [2, "FIFO,3", "7,0,1,2,0,3,0,4,2,3,0,3"],
    [2, "OPT,4", "1,2,3,4,1,2,5,1,2,3,4,5"],
    [2, "LFU,3", "1,2,3,4,1,2,5,1,2,3,4,5"],
    [2, "MFU,3", "1,2,3,4,1,2,5,1,2,3,4,5"],

    # =========================
    # Difficolta 3
    # Sequenze lunghe con molti fault
    # =========================

    [3, "FIFO,4", "1,2,3,4,5,1,2,3,4,5,1,2,3,4,5"],
    [3, "LRU,4", "2,3,2,1,5,2,4,5,3,2,5,2"],
    [3, "OPT,3", "2,3,2,1,5,2,4,5,3,2,5,2"],
    [3, "LFU,4", "1,2,3,4,1,2,5,1,2,3,4,5"],
    [3, "MFU,4", "1,2,3,4,1,2,5,1,2,3,4,5"]
]

from AllocPagine import generateLatex

ALGORITMI = ["FIFO", "LRU", "OPT"]


for es in esercizi:
    algoritmo, frame = es[1].split(",")

    if args.soluzioni:
        print("""\\newpage""")
    print("""\\begin{esercizio}[""" + str(es[0]) + """]
    Avendo a disposizione """ + frame + """ frame
    """)
    print(generateLatex(es[1] + ",T;" + es[2]))
    if args.soluzioni:
        print("\\solution")
        print("")
        for alg in ALGORITMI:
            # TODO: Implement algs
            print(generateLatex(es[1] + ",S;" + es[2]) + "\n")

    print("""\\end{esercizio}
""")
