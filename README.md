# Sangbog

Skriv flere sange ind i songs.txt.
Bemærk formatet i songs.txt:

* Hver sang starter med `Sang: FILNAVN.tex` - husk at tilføje `\input{FILNAVN.tex}` inde i sangbog.tex.
* Hver sang skal have `Titel: TITEL PÅ SANG` og `Forfatter: NAVN PÅ FORFATTER`.
* Vers starter med `Vers:` på en linje for sig og omkvæd med `Omkv:` på en linje for sig.
* For tospaltede sange, tilføj `twocolumn: true` på en linje for sig efter `Sang:`.

## Sådan gør du

Kør `python3 songconvert.py` for at generere tex-filer til alle sangene.

Kør `pdflatex sangbog ; makeindex songbookpreamble ; pdflatex sangbog` for at oversætte sangbogen til PDF.
