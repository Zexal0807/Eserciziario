def crc_mod2_division(dividendo, generatore):
    """
    Esegue la divisione modulo-2 (CRC) passo-passo.

    Restituisce:
      - dividendo: stringa binaria (messaggio + zeri di padding)
      - generatore: stringa binaria (polinomio generatore)
      - quoziente: stringa binaria (stessa lunghezza del dividendo)
      - resto: stringa binaria (resto finale / FCS parziale)
      - steps: lista di tuple (start, blocco, xor_result_o_none, xor_done)
    """
    lg = len(generatore)
    current = ""
    quoziente = ""
    steps = []

    for i, bit in enumerate(dividendo):
        current += bit

        if len(current) < lg:
            quoziente += "0"
            start = i - len(current) + 1
            steps.append((start, current, None, False))
            continue

        blocco = current[-lg:]
        start = i - lg + 1

        if blocco[0] == "0":
            quoziente += "0"
            steps.append((start, blocco, None, False))
        else:
            xor_val = int(blocco, 2) ^ int(generatore, 2)
            xor_bin = bin(xor_val)[2:].zfill(lg)
            quoziente += "1"
            steps.append((start, blocco, xor_bin, True))
            current = xor_bin

    if len(current) > lg:
        current = current[-lg:]
    resto = current

    return dividendo, generatore, quoziente, resto, steps


def generateLatex(expr):
    """
    expr: "messaggio:generatore" ad esempio "11010011101100:10111"
    Esegue la divisione modulo-2 (CRC), calcola il FCS (Frame Check Sequence),
    mostra il messaggio trasmesso e verifica che la divisione del trasmesso per
    il generatore dia resto 0.
    """
    parts = expr.split(":")
    message = parts[0].strip()
    generator = parts[1].strip()

    if not all(c in "01" for c in message) or not all(c in "01" for c in generator):
        return "{Errore: messaggio e generatore devono contenere solo bit 0 e 1.}"

    lg = len(generator)
    dividendo, _, quoziente, resto, steps = crc_mod2_division(message + "0" * (lg - 1), generator)

    # FCS: ultimi lg-1 bit del resto
    if lg > 1:
        fcs = (resto.zfill(lg - 1))[-(lg - 1):]
    else:
        fcs = "0"
    trasmesso = message + fcs

    # Verifica: dividiamo il messaggio trasmesso per il generatore
    _, _, _, resto_verifica, _ = crc_mod2_division(trasmesso, generator)
    if lg > 1:
        resto_verifica = (resto_verifica.zfill(lg - 1))[-(lg - 1):]
    else:
        resto_verifica = "0"

    la = len(dividendo)
    lb = lg
    left_cols = la
    right_cols = lb

    res = []
    res.append("{")
    
    res.append(f"Lunghezza generatore ${lg}$ bit")
    res.append("")
    res.append(f"Si aggiungono ${lg-1}$ zeri in coda al messaggio prima di procedere con il calcolo")

    res.append("")
    res.append("\\begin{tabular}{" + "c" * left_cols + "|" + "c" * right_cols + "}")
    # --- PRIMA RIGA: dividendo aumentato | generatore (right-justified) ---
    left_row = list(dividendo)
    right_row = [""] * (right_cols - lb) + list(generator)
    res.append(" & ".join(left_row) + " & " + " & ".join(right_row) + " \\\\")
    res.append("\\hline")
    res.append("\\hline")

    # --- PASSI: per ogni step mostro il blocco corrente e, se XOR, il generatore allineato ---
    for start, blocco, xor_result, xor_done in steps:
        row = [""] * left_cols
        for j, ch in enumerate(blocco):
            pos = start + j
            if 0 <= pos < left_cols:
                row[pos] = ch
        right_empty = [""] * right_cols
        res.append(" & ".join(row) + " & " + " & ".join(right_empty) + " \\\\")

        if xor_done:
            row_b = [""] * left_cols
            for j, ch in enumerate(generator):
                pos = start + j
                if 0 <= pos < left_cols:
                    row_b[pos] = ch
            res.append(" & ".join(row_b) + " & " + " & ".join(right_empty) + " \\\\")
            res.append("\\hline")

    rest_row = [""] * (left_cols - len(resto)) + list(resto)
    right_row = [""] * len(generator)
    res.append("\\hline")
    res.append("\\hline")
    res.append(" & ".join(rest_row) + " & " + " & ".join(right_row) + " \\\\")
    res.append("\\end{tabular}")
    res.append("")
    res.append("Messaggio trasmesso (dati + FCS): " + message + " \\textbf{" + fcs + "}")
    res.append("")
    res.append("}")

    return "\n".join(res)


def main(expr):
    print(generateLatex(expr))


import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])
