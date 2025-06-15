# csv_soundex.py
# Version 1.0.0 vom 15.06.2025
# Erstellt eine CSV mit Soundex-Spalten für deutsche Namen unter Berücksichtigung deutscher Phonetik.

import csv
import sys
import os
import re

def normalize_german_phonetics(word):
    """
    Vorverarbeitungsregeln für deutsche Namen zur phonetischen Angleichung:

    1. Umlaute und ß:
       - ä → ae, ö → oe, ü → ue, ß → ss

    2. Buchstabenkombinationen:
       - ph → f
       - th → t

    3. 'ch' und 'sch' am Wortanfang:
       - ch vor e, i, ä, ö, ü, y → sch
       - ch vor a, o, u, r, l → k

    4. 'sch' und 'ch' im Wort (Platzhalter, damit sie nicht verändert werden):
       - sch → $ (temporär)
       - ch → # (temporär)

    5. 'st', 'sp' am Wortanfang:
       - st → scht
       - sp → schp

    6. 'qu' zu 'kw' (optional, für phonetische Annäherung)

    7. 'c' am Wortanfang:
       - c vor a, o, u, l, r → k
       - c vor e, i, ä, ö, ü, y → z

    8. 'c' im Wortinneren (außer am Wortanfang, nicht nach 's'):
       - c vor a, o, u, l, r → k
       - c vor e, i, ä, ö, ü, y → z

    9. Konsonantenangleichungen:
       - v → f
       - w → v
       - z → ts
       - y → i
       - ck → k

    10. Endungen:
        - -ig am Wortende → ich

    11. 's' am Wortanfang vor Vokal zu 'z'

    12. Diphthonge:
        - ai, ey, ay → ei
        - eu, äu, euy, uy, ui → eu

    13. Rückumwandlung der Platzhalter:
        - $ → sch
        - # → ch
    """
    word = word.lower()
    # Umlaute und ß
    word = word.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    # ph, th
    word = word.replace("ph", "f").replace("th", "t")
    # ch am Wortanfang vor e, i, ä, ö, ü, y -> sch
    word = re.sub(r'^ch(?=[eiäöüyaeioyu])', 'sch', word)
    # ch am Wortanfang vor a, o, u, r, l -> k
    word = re.sub(r'^ch(?=[aoulr])', 'k', word)
    # sch schützen (Platzhalter)
    word = word.replace("sch", "$")
    # st, sp am Wortanfang
    word = re.sub(r'^st', 'scht', word)
    word = re.sub(r'^sp', 'schp', word)
    # ch schützen (Platzhalter)
    word = word.replace("ch", "#")
    # qu zu kw (optional)
    word = word.replace("qu", "kw")
    # c am Wortanfang vor a, o, u, l, r -> k
    word = re.sub(r'^c(?=[aoulr])', 'k', word)
    # c am Wortanfang vor e, i, ä, ö, ü, y -> z
    word = re.sub(r'^c(?=[eiäöüy])', 'z', word)

    # c im Wortinneren vor a, o, u, l, r -> k (nicht nach s)
    def replace_c_inner(match):
        prev = match.group(1)
        after = match.group(3)
        if prev != 's':
            return prev + 'k' + after
        else:
            return match.group(0)
    word = re.sub(r'(.)(c)([aoulr])', replace_c_inner, word)

    # c im Wortinneren vor e, i, ä, ö, ü, y -> z (nicht nach s)
    def replace_c_inner_z(match):
        prev = match.group(1)
        after = match.group(3)
        if prev != 's':
            return prev + 'z' + after
        else:
            return match.group(0)
    word = re.sub(r'(.)(c)([eiäöüy])', replace_c_inner_z, word)

    # v zu f, w zu v
    word = word.replace("v", "f").replace("w", "v")
    # z zu ts
    word = word.replace("z", "ts")
    # y zu i
    word = word.replace("y", "i")
    # ck -> k
    word = word.replace("ck", "k")
    # -ig am Wortende -> ich (optional)
    word = re.sub(r'ig$', 'ich', word)
    # s am Wortanfang vor Vokal zu z
    word = re.sub(r'^s(?=[aeiouy])', 'z', word)
    # Diphthonge
    word = re.sub(r'(ai|ey|ay)', 'ei', word)
    word = re.sub(r'(eu|äu|euy|uy|ui)', 'eu', word)
    # Platzhalter zurücksetzen
    word = word.replace("$", "sch").replace("#", "ch")
    return word

def german_soundex(word):
    """
    Deutsche Soundex-Variante, berücksichtigt Umlaute und phonetische Besonderheiten.
    """
    if not word:
        return ""
    # Vorverarbeitung
    word = normalize_german_phonetics(word)
    word = word.upper()
    # Nur Buchstaben zulassen
    word = re.sub(r'[^A-Z]', '', word)
    if not word:
        return ""
    # Soundex-Tabelle (deutsch angepasst)
    codes = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1', 'W': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    first_letter = word[0]
    result = first_letter
    prev_code = codes.get(first_letter, '')
    for char in word[1:]:
        code = codes.get(char, '')
        if code != prev_code:
            if code != '':
                result += code
            prev_code = code
    result = result.ljust(4, '0')[:4]
    return result

def is_numeric_or_special(val):
    """
    Prüft, ob val ausschließlich aus Ziffern oder Sonderzeichen besteht.
    """
    if not val or val.strip() == "":
        return False
    # Nur Ziffern oder nur Sonderzeichen (z.B. "_", "...", etc.)
    return all(not c.isalnum() for c in val) or val.isdigit()

def csv_soundex(input_csv, columns):
    """
    Liest eine CSV-Datei ein, berechnet für die angegebenen Spalten Soundex-Codes
    und schreibt eine neue Datei mit zusätzlichen Soundex-Spalten.
    """
    with open(input_csv, encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        missing = [col for col in columns if col not in fieldnames]
        if missing:
            print(f"Fehlende Spalten: {', '.join(missing)}")
            sys.exit(1)

        # Neue Feldnamen ergänzen
        new_fieldnames = list(fieldnames)
        for col in columns:
            new_fieldnames.append(f"{col}_soundex")

        # Ausgabedatei
        base, ext = os.path.splitext(input_csv)
        output_csv = f"{base}_soundex{ext}"

        with open(output_csv, "w", encoding="utf-8", newline='') as out_f:
            writer = csv.DictWriter(out_f, fieldnames=new_fieldnames)
            writer.writeheader()
            for row in reader:
                for col in columns:
                    val = row[col]
                    if val is None or val.strip() == "":
                        row[f"{col}_soundex"] = ""
                    elif is_numeric_or_special(val):
                        row[f"{col}_soundex"] = val
                    else:
                        row[f"{col}_soundex"] = german_soundex(val)
                writer.writerow(row)

    print(f"Fertig! Neue Datei: {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Aufruf: python soundex_csv.py <csv_datei> <spalten1,spalten2,...>")
        sys.exit(1)
    input_csv = sys.argv[1]
    columns = [col.strip() for col in sys.argv[2].split(",")]
    csv_soundex(input_csv, columns)
