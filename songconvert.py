import argparse
import os
import re
from typing import TypedDict


parser = argparse.ArgumentParser()


t_song = "Sang"
t_field = {"Titel": "title", "Melodi": "mel", "Forfatter": "author", "twocolumn": "twocolumn"}
t_verse = {"Vers": "vers", "Omkv": "omkvaed"}


class Verse(TypedDict):
    kind: str
    lines: list[str]


class Song(TypedDict):
    filename: str
    fields: dict[str, str]
    verses: list[Verse]


tex_escapes = [
    (r'\$[\x21-\x7f]+\$', ''),
    (r'\&', r'\&'),
    (r'’', "'"),
    (r'„', "''"),
    (r'“', "''"),
    (r'”', "''"),
    (r'\.\.\.', r"\ldots "),
    (r'\. \. \.', r"\ldots "),
    (r'–', "--"),
    (r'—', "---"),
]
tex_escape_pattern = re.compile("|".join(f"({k})" for k, v in tex_escapes))


def tex_escape(s: str) -> str:
    t = tex_escape_pattern.sub(lambda mo: tex_escapes[(mo.lastindex or 0//0) - 1][1] or mo.group(), s)
    unk = re.sub(r'[\x01-\x7fæøåÆØÅéüâ]', '', t)
    if unk:
        raise Exception("".join(sorted(set(unk))))
    return t


def main() -> None:
    parser.parse_args()
    filename = "songs.txt"
    with open(filename) as fp:
        contents = fp.read()

    current_song: Song | None = None
    songs: list[Song] = []
    for lineno, line in enumerate(contents.splitlines(), 1):
        line = line.strip()
        k, s, v = line.partition(":")
        v = v.strip()
        if s and k == t_song:
            current_song = {"filename": v, "fields": {}, "verses": []}
            songs.append(current_song)
        elif s and k in t_field:
            if current_song is None or current_song["verses"]:
                raise SystemExit(f"{filename}:{lineno}: Expected '{t_song}:' before headers")
            current_song["fields"][t_field[k]] = v
        elif s and k in t_verse:
            if current_song is None:
                raise SystemExit(f"{filename}:{lineno}: Expected '{t_song}:' before headers")
            current_song["verses"].append({"kind": t_verse[k], "lines": []})
        elif line:
            if current_song is None:
                raise SystemExit(f"{filename}:{lineno}: Expected '{t_song}:' before song line")
            if not current_song["verses"]:
                raise SystemExit(f"{filename}:{lineno}: Expected '{next(iter(t_verse))}:' before song line")
            current_song["verses"][-1]["lines"].append(line)
    for song in songs:
        with open(song["filename"] + "_", "w") as fp:
            title = tex_escape(song["fields"].get("title") or song["filename"])
            author = tex_escape(song["fields"].get("author", ""))
            print(r'\begin{sang}{%s}{%s}' % (title, author) + "%", file=fp)
            if song["fields"].get("twocolumn"):
                print(r'\begin{multicols}{2}\multicolinit', file=fp)
            for verse in song["verses"]:
                print(r'\begin{%s}' % (verse["kind"]), file=fp)
                print('\n\\verseend\n'.join(map(tex_escape, verse["lines"])), file=fp)
                print(r'\end{%s}' % (verse["kind"]), file=fp)
            if song["fields"].get("twocolumn"):
                print(r'\end{multicols}', file=fp)
            print(r'\end{sang}', file=fp)
        os.rename(song["filename"] + "_", song["filename"])


if __name__ == "__main__":
    main()
