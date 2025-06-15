# Soundex für die deutsche Begriffe in Tabellen im CSV-Format

**Version:** 1.0.1  
**Datum:** 15.06.2025

## Beschreibung

Dieses Python-Programm bietet eine grafische Oberfläche (GUI) und einen Konsolenmodus, um CSV-Dateien um Soundex-Spalten für deutsche Namen zu erweitern.  
Der Soundex-Algorithmus wurde speziell an die phonetischen Besonderheiten der deutschen Sprache angepasst.  
Das Ziel ist es, phonetisch ähnliche Namen (wie „Müller“ und „Mueller“) mit demselben Code zu erfassen und so die Dublettenprüfung oder Namenssuche zu erleichtern.

---

## Features

- **GUI-Modus:**  
  - Auswahl einer CSV-Datei per Dialog
  - Anzeige des Dateipfads mit intelligentem Zeilenumbruch
  - Übersichtliche Mehrfachauswahl der Spalten (Checkboxen), gruppiert in Spalten zu je 10 Zeilen
  - Start der Verarbeitung per Button
  - INFO-Button mit Programmbeschreibung
  - Bearbeiten-Button (startet die Verarbeitung)
  - Beenden-Button
  - Anzeige des Ausgabepfads nach erfolgreicher Verarbeitung
  - Fenstergröße 600x400, horizontal veränderbar

- **Konsolenmodus:**  
  - Aufruf mit Parametern möglich
  - Ausgabe des Ausgabepfads nach erfolgreicher Verarbeitung

---

## Voraussetzungen

- Python 3.7 oder neuer
- Keine externen Bibliotheken notwendig (nur Standardbibliothek)
- Die Datei `csv_soundex.py` muss sich im gleichen Verzeichnis befinden und die Funktion `csv_soundex(input_csv, columns)` bereitstellen

---

## Installation

Kein Installationsschritt notwendig.  
Speichere das Script z.B. als `csv_soundex_gui.py` und stelle sicher, dass `csv_soundex.py` im gleichen Verzeichnis liegt.

**Optional: Kompilieren zu einer ausführbaren Datei (EXE)**
Falls das Programm ohne Python-Installation auf anderen Rechnern genutzt werden soll, kannst es mit Tools wie PyInstaller oder cx_Freeze in eine ausführbare Datei (z.B. .exe für Windows) umwandeln:

Beispiel mit PyInstaller
PyInstaller installieren (falls noch nicht vorhanden):

```bash
pip install pyinstaller
```
EXE erstellen:
```bash
pyinstaller --onefile csv_soundex_gui.py
```
Die ausführbare Datei findet sich dann im Ordner dist/.

---

## Nutzung

### GUI-Modus (Standard)

```bash
python csv_soundex_gui.py
```

- Wähle eine CSV-Datei aus.
- Wähle eine oder mehrere Spalten für die Soundex-Verarbeitung.
- Starte die Verarbeitung mit dem 🛠️ Bearbeiten-Button.
- Die neue Datei wird im gleichen Verzeichnis gespeichert und der Pfad angezeigt.

---

### Konsolenmodus

```bash
python csv_soundex_gui.py --konsole  
```

**Beispiel:**
```bash
python csv_soundex_gui.py --konsole beispiel.csv Name,Ort
```
- Die neuen Soundex-Spalten werden wie gewohnt erzeugt.
- Nach Abschluss wird der Pfad der Ausgabedatei auf der Konsole ausgegeben.

---

## Beispiel-CSV

```csv
ID,Vorname,Name,Ort
1,Andreas,Schäfer,Berlin
2,Petra,Schäffer,Hamburg
3,Johann,Mueller,München
4,Julia,Müller,Frankfurt
...
```
Eine vollständige Testdatei mit vielen phonetischen Varianten ist im github-Verzeichnis hinterlegt.

---

## Hinweise zu den phonetischen Besonderheiten

Das Programm berücksichtigt u.a.:
- Umlaute und deren Umschreibungen: ä/ae, ö/oe, ü/ue, ß/ss
- Diphthonge und Varianten: Meier/Mayer, Seitz/Seiz
- ph/f/v/w, ck/k/ch, th/t, qu/kw, c/k/z, sch/sh, Doppelkonsonanten
- Namensendungen und -varianten

---

## Lizenz

Dieses Projekt ist frei nutzbar für private und wissenschaftliche Zwecke.

---

**Viel Erfolg beim Einsatz!**  
Für Fragen, Verbesserungen oder Anpassungen gerne melden.

---

## Beschreibung der Behandlung der deutschen Aussprache
Im Script werden folgende Besonderheiten der deutschen Aussprache behandelt und in der Vorverarbeitung umgesetzt:

### 1. **Umlaute und ß**
- **ä, ö, ü** werden zu **ae, oe, ue** normalisiert, um unterschiedliche Schreibweisen gleichzubehandeln.
- **ß** wird zu **ss** gewandelt, da beide gleich ausgesprochen werden[3][5].

### 2. **Buchstabenkombinationen**
- **ph** wird zu **f** (wie in „Phonetik“ → „Fonetik“)[1].
- **th** wird zu **t** (wie in „Thema“ → „Tema“)[1].

### 3. **ch und sch am Wortanfang**
- **ch** vor **e, i, ä, ö, ü, y** am Wortanfang wird zu **sch** (wie in „Chemie“, „China“)[1].
- **ch** vor **a, o, u, r, l** am Wortanfang wird zu **k** (wie in „Chor“, „Chur“)[1].
- **sch** und **ch** werden im Wortinneren durch Platzhalter geschützt, damit sie nicht versehentlich verändert werden[1][3].

### 4. **sp und st am Wortanfang**
- **sp** und **st** am Wortanfang werden zu **schp** bzw. **scht** (wie in „Spiel“ [ʃpiːl], „Stein“ [ʃtaɪn])[1].

### 5. **qu**
- **qu** wird zu **kw** (wie in „Quelle“ → „Kwelle“), um die phonetische Annäherung zu verbessern[1].

### 6. **c am Wortanfang**
- **c** vor **a, o, u, l, r** am Wortanfang wird zu **k** (wie in „Cornelia“)[1].
- **c** vor **e, i, ä, ö, ü, y** am Wortanfang wird zu **z** (wie in „Cäsar“)[1].

### 7. **c im Wortinneren (nicht nach s)**
- **c** vor **a, o, u, l, r** wird zu **k** (z. B. „Bacardi“ → „Bakardi“).
- **c** vor **e, i, ä, ö, ü, y** wird zu **z** (z. B. „Cecilie“ → „Zezilie“).
- Nach „s“ bleibt „c“ unverändert, da „sc“ eine eigene Aussprache hat[1].

### 8. **Konsonantenangleichungen**
- **v** wird zu **f** (wie in „Vater“ → „Fater“)[3].
- **w** wird zu **v** (wie in „Wasser“ → „Vasser“)[2][3].
- **z** wird zu **ts** (wie in „Zimmer“ → „Tsimmer“)[3][5].
- **y** wird zu **i** (wie in „Mayer“ → „Maier“)[3].
- **ck** wird zu **k** (wie in „Beck“ → „Bek“)[1].

### 9. **Endungen**
- **-ig** am Wortende wird zu **ich** (umgangssprachliche Aussprache wie in „König“ → „Könich“)[1].

### 10. **s am Wortanfang vor Vokal**
- **s** am Wortanfang vor Vokal wird zu **z** (wie in „Sonne“ → „Zonne“)[3][5].

### 11. **Diphthonge**
- **ai, ey, ay** werden zu **ei** (wie in „Meyer“, „Mayr“, „Meier“)[5].
- **eu, äu, euy, uy, ui** werden zu **eu** (wie in „Eule“, „äußern“)[1].

### 12. **Platzhalter-Rückumwandlung**
- Temporäre Platzhalter für **sch** und **ch** werden am Ende zurück in die Originalbuchstabenkombinationen gewandelt.

---

**Fazit:**  
Das Script bildet viele zentrale Besonderheiten der deutschen Aussprache ab, insbesondere bei Konsonantenverbindungen, Umlaute, Diphthonge, und typischen phonetischen Schreibvarianten von Namen. Dadurch werden phonetisch ähnliche Namen im Deutschen besser zusammengeführt als mit dem klassischen, englisch geprägten Soundex[1][2][3][5].

[1] https://ifl.phil-fak.uni-koeln.de/sites/linguistik/Phonetik/import/Phonetik_Files/Allgemeine_Dateien/Martin_Wilz.pdf
[2] https://de.wikipedia.org/wiki/Soundex
[3] https://kryptografie.de/kryptografie/chiffre/soundex.htm
[4] https://de.wikipedia.org/wiki/K%C3%B6lner_Phonetik
[5] https://www.wittye.com/content/schule/info1617/09_Phonetische_Suche_Soundex.pdf
[6] https://www.c-plusplus.net/forum/topic/134350/soundex-algorithmus-f%C3%BCr-die-deutsche-sprache
[7] https://phpgangsta.de/meinten-sie-eingaben-verbessern-mit-levenshtein-und-soundex
[8] https://www.jd-engineering.de/german-soundex-koelner-phonetik-sql-implementation/
