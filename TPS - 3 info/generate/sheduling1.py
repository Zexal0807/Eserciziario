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

esercizi = [
    # =========================
    # Difficoltà 1
    # Pochi processi, qualche arrivo contemporaneo, differenze FCFS vs SJF/SRTF
    # =========================
    
    # 1. Arrivi contemporanei a t=0, burst diversi → SJF cambia ordine
    [1, """P1,0,6
P2,0,3
P3,0,2"""],
    
    # 2. Due arrivi a t=0, uno a t=1 → SJF migliore di FCFS
    [1, """P1,0,5
P2,0,2
P3,1,3"""],
    
    # 3. Arrivi scalari, ma un processo corto arriva dopo
    [1, """P1,0,6
P2,1,2
P3,2,3"""],
    
    # 4. Tutti arrivi a t=0, burst crescenti → FCFS pessimo, SJF ottimo
    [1, """P1,0,2
P2,0,4
P3,0,6"""],
    
    # 5. Due processi uguali a t=0, uno corto a t=1
    [1, """P1,0,4
P2,0,4
P3,1,2"""],
    
    # 6. Arrivi a 0 e 1, burst molto diversi → SRTF preemption chiara
    [1, """P1,0,6
P2,1,2
P3,2,3
P4,2,4"""],
    
    # 7. Tre processi, due con stesso arrivo, uno corto
    [1, """P1,0,5
P2,0,3
P3,1,2
P4,1,3"""],
    
    # 8. Arrivi a 0,1,2 con burst decrescente → SJF/SRTF vantaggiosi
    [1, """P1,0,6
P2,1,4
P3,2,2
P4,0,3"""],
    
    # 9. Due processi lunghi a t=0, uno corto a t=1
    [1, """P1,0,5
P2,0,6
P3,1,2
P4,1,3"""],
    
    # 10. Quattro processi, due a t=0, due dopo
    [1, """P1,0,4
P2,0,3
P3,1,2
P4,2,3"""],
    
    # =========================
    # Difficoltà 2
    # Più processi, più arrivi contemporanei, situazioni più “subdole”
    # =========================
    
    # 11. Tre processi a t=0, altri due dopo → SJF/SRTF molto diversi da FCFS
    [2, """P1,0,6
P2,0,3
P3,0,2
P4,1,4
P5,2,3"""],
    
    # 12. Due lunghi a t=0, corti in arrivo a 1 e 2 → SRTF preemption multipla
    [2, """P1,0,7
P2,0,6
P3,1,2
P4,2,3"""],
    
    # 13. Arrivi a 0,0,1,1,2 → FCFS vs SJF evidente
    [2, """P1,0,5
P2,0,4
P3,1,2
P4,1,3
P5,2,4"""],
    
    # 14. Processo lungo a t=0, molti corti dopo → SRTF molto efficiente
    [2, """P1,0,8
P2,1,2
P3,2,3
P4,3,2
P5,4,3
P6,1,2"""],
    
    # 15. Due “grandi” a t=0, tre medi a t=1,2,3
    [2, """P1,0,7
P2,0,6
P3,1,4
P4,2,3
P5,3,4
P6,3,1"""],
    
    # 16. Arrivi a 0,0,0,1,2 → SJF cambia molto l’ordine
    [2, """P1,0,5
P2,0,4
P3,0,3
P4,1,2
P5,2,4
P6,2,1"""],
    
    # 17. Processo lungo, poi due corti quasi simultanei
    [2, """P1,0,9
P2,1,2
P3,1,3
P4,3,4
P5,2,3"""],
    
    # 18. Quattro processi, due a t=0, due a t=2
    [2, """P1,0,6
P2,0,4
P3,2,2
P4,2,3
P5,3,5
P6,1,4"""],
    
    # 19. Tre a t=0, due a t=2, uno a t=4
    [2, """P1,0,5
P2,0,4
P3,0,3
P4,2,2
P5,2,4
P6,4,3"""],
    
    # 20. Lungo a t=0, corti ravvicinati tra 1 e 3
    [2, """P1,0,10
P2,1,2
P3,2,3
P4,3,2
P5,4,4
P6,1,1"""],
    
    # 21. Due lunghi a t=0, tre corti a t=1,2,3
    [2, """P1,0,8
P2,0,7
P3,1,2
P4,2,3
P5,3,2
P6,2,2
P7,1,3"""],
    
    # 22. Tre a t=0, tre a t=2, burst vari
    [2, """P1,0,6
P2,0,4
P3,0,5
P4,2,2
P5,2,3
P6,2,4
P7,3,1"""],
    
    # 23. Processo medio a t=0, molti piccoli dopo
    [2, """P1,0,7
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,3
P7,1,1
P8,2,1"""],
    
    # 24. Due a t=0, quattro a t=2,3,4
    [2, """P1,0,6
P2,0,5
P3,2,2
P4,3,3
P5,4,2
P6,4,4
P7,1,1
P8,2,1"""],
    
    # 25. Tre a t=0, tre a t=1,2,3 (burst decrescenti nei secondi)
    [2, """P1,0,6
P2,0,5
P3,0,4
P4,1,3
P5,2,2
P6,3,2
P7,4,1
P8,0,1"""],
    
    # =========================
    # Difficoltà 3
    # Molti processi, arrivi contemporanei multipli, situazioni “nastie”
    # =========================
    
    # 26. Tre lunghi a t=0, tre corti a t=1,2,3 → SRTF molto diverso
    [3, """P1,0,6
P2,0,5
P3,0,4
P4,1,2
P5,2,3
P6,3,2
P7,2,3
P8,1,3"""],
    
    # 27. Quattro a t=0, due a t=2, due a t=4
    [3, """P1,0,6
P2,0,5
P3,0,3
P4,0,2
P5,2,1
P6,2,2
P7,4,3
P8,4,1"""],
    
    # 28. Lungo a t=0, molti corti ravvicinati 1–5
    [3, """P1,0,8
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,3"""],
    
    # 29. Due lunghi a t=0, quattro corti a t=1,2,3,4
    [3, """P1,0,8
P2,0,6
P3,1,2
P4,2,3
P5,3,2
P6,4,2"""],
    
    # 30. Tre a t=0, tre a t=1, tre a t=3
    [3, """P1,0,6
P2,0,4
P3,0,3
P4,1,2
P5,1,1
P6,1,3"""],
    
    # 31. Quattro a t=0, quattro a t=2, burst molto vari
    [3, """P1,0,6
P2,0,5
P3,0,4
P4,0,3
P5,2,1
P6,2,2"""],
    
    # 32. Lungo a t=0, molti corti tra 1 e 6
    [3, """P1,0,6
P2,1,2
P3,2,3
P4,3,2
P5,4,2
P6,5,3
P7,6,2"""],
    
    # 33. Tre medi a t=0, cinque corti a t=1..5
    [3, """P1,0,6
P2,0,5
P3,0,4
P4,1,1
P5,3,3
P6,5,2
P7,4,2"""],
    
    # 34. Due lunghi a t=0, sei corti a t=1..6
    [3, """P1,0,5
P2,0,4
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2"""],
    
    # 35. Quattro a t=0, tre a t=2, tre a t=4
    [3, """P1,0,5
P2,0,4
P3,0,3
P4,0,3
P5,2,2
P6,2,3
P7,2,4
P8,4,2"""],
    
    # 36. Tre a t=0, quattro a t=1, tre a t=3
    [3, """P1,0,1
P2,0,3
P3,0,5
P4,1,2
P5,1,3
P6,1,2"""],
    
    # 37. Due lunghi a t=0, molti corti 1..7
    [3, """P1,0,6
P2,0,5
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2"""],
    
    # 38. Quattro a t=0, quattro a t=2, quattro a t=4
    [3, """P1,0,4
P2,0,3
P3,0,2
P4,0,3
P5,2,2
P6,2,3
P7,2,4"""],
    
    # 39. Tre a t=0, tre a t=1, tre a t=2, tre a t=4
    [3, """P1,0,3
P2,0,1
P3,0,5
P4,1,3
P5,1,2
P6,1,4
P7,2,2
P8,2,3"""],
    
    # 40. Lungo a t=0, molti corti 1..8
    [3, """P1,0,1
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,2
P7,6,3
P8,7,2"""],
    
    # 41. Due lunghi a t=0, otto corti 1..8
    [3, """P1,0,6
P2,0,4
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3"""],
]

from ProcessTable import generateLatex as generateTabella
from ProcessSchedule import generateLatex as generateScheduling

# Algoritmi di scheduling proposti dalla sezione
ALGORITMI = ["FCFS", "SJF", "SRTF"]

if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for es in esercizi:
    if args.soluzioni:
        print("""\\newpage""")
    print("""\\begin{esercizio}[""" + str(es[0]) + """]
    """)
    print(generateTabella(es[1]))
    if args.soluzioni:
        print("\\solution")
        print("")
        for alg in ALGORITMI:
            print(generateScheduling(alg + ";\n" + es[1]) + "\n")

    print("""\\end{esercizio}
""")

if not args.soluzioni:
    print("""\\end{multicols}
""")