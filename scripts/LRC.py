def parita_pari(bits):
    """
    Calcola il bit di parità pari per una stringa di bit.
    Restituisce '0' se il numero di 1 è già pari, '1' altrimenti.
    """
    n_uni = bits.count("1")
    return "0" if n_uni % 2 == 0 else "1"


def generateLatex(expr):
    """
    expr: elenco di numeri decimali separati da virgola, ad esempio "45,67,89"
    Ogni numero è una parola da 7 bit (0-127).
    Costruisce una matrice N x 7, aggiunge:
      - colonna 8: parity bit di riga (parità pari)
      - riga N+1: parity bit di colonna per le prime 7 colonne
      - cella (N+1,8): parity bit della colonna 8 (parità della riga dei parity di colonna)
    L'output LaTeX mostra:
      - elenco parole in decimali
      - conversione binaria di ogni parola
      - tabella (N+1) x 8 con parità di riga e colonna
    """
    # --- Parsing input ---
    items = [x.strip() for x in expr.split(",") if x.strip()]
    valori = []
    for it in items:
        try:
            v = int(it)
        except ValueError:
            return "{Errore: inserire numeri decimali separati da virgola.}"
        if v < 0 or v > 127:
            return "{Errore: ogni parola deve essere compresa tra 0 e 127 (7 bit).}"
        valori.append(v)

    n = len(valori)
    if n == 0:
        return "{Errore: almeno una parola richiesta.}"

    # --- Conversione in binario 7 bit ---
    binari = [bin(v)[2:].zfill(7) for v in valori]

    # --- Calcolo parity bit di riga ---
    row_parity = [parita_pari(b) for b in binari]

    # --- Calcolo parity bit di colonna (prime 7 colonne) ---
    col_parity = []
    for j in range(7):
        col_bits = [binari[i][j] for i in range(n)]
        col_parity.append(parita_pari("".join(col_bits)))

    # --- Cella angolo (riga N+1, colonna 8) ---
    # = parità della colonna 8 (dei row_parity bit)
    #   che equivale anche a parità della riga N+1 (dei col_parity bit)
    angolo = parita_pari("".join(row_parity))

    # --- Costruzione LaTeX ---
    res = []
    res.append("{")
    for v, b in zip(valori, binari):
        res.append("$"+ str(v) + " = " + str(b) + """_2$
""")
    res.append("")
    res.append("\\begin{tabular}{|" + "c" * 7 + "||c|}")
    res.append("\\hline")
    # Prime N righe: parola + parity di riga
    for b, rp in zip(binari, row_parity):
        celle = list(b) + [rp]
        res.append(" & ".join(celle) + " \\\\")
    res.append("\\hline")
    res.append("\\hline")
    # Riga N+1: parity di colonna + angolo
    celle_ultima = col_parity + [angolo]
    res.append(" & ".join(celle_ultima) + " \\\\")
    res.append("\\hline")
    res.append("\\end{tabular}")
    res.append("")
    res.append("}")

    return "\n".join(res)


def main(expr):
    print(generateLatex(expr))


import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
