# Data

Sheet music, MusicXML files, training data and models are **not** committed
(see `.gitignore`). Only this description and `corpus.csv` live here.

Intended structure (local):

```
data/
  raw/          # original PDFs and MusicXML of the test corpus
  reference/    # reference pitches per piece (generated from MusicXML)
  synthetic/    # synthetic training images + YOLO labels
  deepscores/   # DeepScores V2 (converted)
```

**Important:** pieces from the test corpus are never used for training,
otherwise the measurements are worthless.

`corpus.csv` lists the source and the verified license of each piece.
Use only public-domain or openly licensed scores for the public demo.
