![CI](https://github.com/davmorai/Notenamer/actions/workflows/ci.yml/badge.svg)

# Daten

Notenblätter, MusicXML-Dateien, Trainingsdaten und Modelle werden **nicht** committet
(siehe `.gitignore`). Hier liegen nur diese Beschreibung und `corpus.csv`.

Vorgesehene Struktur (lokal):

```
data/
  raw/          # Original-PDFs und MusicXML des Testkorpus
  reference/    # Referenz-Notennamen pro Stück (aus MusicXML erzeugt)
  synthetic/    # Synthetische Trainingsbilder + YOLO-Labels
  deepscores/   # DeepScores V2 (konvertiert)
```

**Wichtig:** Stücke aus dem Testkorpus werden nie fürs Training verwendet,
sonst sind die Messwerte wertlos.

In `corpus.csv` steht pro Stück die Quelle und die geprüfte Lizenz.
Für die öffentliche Demo nur gemeinfreie Stücke verwenden.
