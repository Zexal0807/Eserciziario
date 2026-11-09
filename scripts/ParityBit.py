def generateLatex(expr):
    """
    expr: "stringa_binaria tipo"  ad esempio "1011001 pari" oppure "1011001 dispari"
    Calcola il bit di parità e mostra la parola codificata, poi illustra il rilevamento
    di un errore di singolo bit (inversione di un bit) attraverso la parità.
    """
    parts = expr.split()
    data = parts[0].strip()
    tipo = parts[1].strip().lower() if len(parts) > 1 else "pari"

    # Verifica che data contenga solo 0 e 1
    if not all(c in "01" for c in data):
        return "{Errore: la stringa deve contenere solo bit 0 e 1.}"

    n_uni = data.count("1")
    if tipo == "pari":
        bit_parita = "0" if n_uni % 2 == 0 else "1"
    else:  # dispari
        bit_parita = "1" if n_uni % 2 == 0 else "0"

    parola_codificata = data + bit_parita

    res = []
    res.append("{")
    res.append(f"Parola dati: ${data}$")
    res.append("")
    res.append(f"Numero di bit a 1 nella parola dati: {n_uni}")
    res.append("")
    res.append(f"Tipo di parità richiesta: \\textbf{{{tipo}}}")
    res.append("")
    res.append(f"Il bit di parità è: ${bit_parita}$")
    res.append("")
    res.append(f"Parola codificata (dati + bit di parità): ${parola_codificata}$")
    res.append("")

    s = len(data) + 1
    
    res.append("\\begin{tabular}{" + " ".join(["c"] * s) + "}")
    res.append(" & ".join(list(data)) + " & \\\\")
    res.append("\\hline")
    res.append(" & ".join(list(parola_codificata[:-1])) + " & " + bit_parita + " \\\\")
    res.append("\\end{tabular}")
    res.append("")
    res.append("}")

    return "\n".join(res)

def main(expr):
    print(generateLatex(expr))

import sys
sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
