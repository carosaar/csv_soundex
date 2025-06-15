# Soundex für die deutsche Begriffe in Tabellen im CSV-Format

**Version:** 1.0.0  
**Datum:** 15.06.2025
**Autor:** Dieter Eckstein

## Aufgabe

Dieses Python-Projekt erweitert eine CSV-Datei um Soundex-Spalten für deutsche Namen.  
Der Soundex-Algorithmus wird dabei durch eine phonetische Vorverarbeitung an die Besonderheiten der deutschen Sprache angepasst.  
Das Ziel ist es, phonetisch ähnliche Namen (wie „Colling“ und „Kolling“) mit demselben Code zu erfassen und so die Dublettenprüfung oder Namenssuche zu erleichtern.

## Lösung

- Das Script liest eine CSV-Datei ein und berechnet für eine oder mehrere angegebene Spalten einen deutschen Soundex-Code.
- Die phonetische Vorverarbeitung berücksichtigt deutsche Aussprachebesonderheiten, z.B. Umlaute, „ch“, „sch“, „c“/„k“, Diphthonge, „sp“/„st“ am Wortanfang, u.v.m.
- Für numerische Werte oder reine Sonderzeichen wird der Originalwert übernommen.
- Die neuen Soundex-Spalten werden als `_soundex` an die CSV-Datei angehängt.

## Voraussetzungen

- Python 3.7 oder neuer
- Keine externen Bibliotheken notwendig (nur Standardbibliothek)

## Installation

Kein Installationsschritt notwendig.  
Speichere das Script z.B. als `soundex_csv.py`.

## Nutzung

```bash
python soundex_csv.py  
```

**Beispiel:**
```bash
python soundex_csv.py kunden.csv Nachname,Vorname
```
Das Ergebnis wird als `kunden_soundex.csv` gespeichert.

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
