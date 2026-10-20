"""Build the Latin reference text for test 3 from the fetched Project Gutenberg files.

Keeps the text between the Gutenberg start and end markers, joins the nine books in a fixed
order, cuts it into blocks of 4,000 characters and holds out every tenth block.
usage: python code/build_corpus.py SOURCE_DIR WORK_DIR
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

IDS = [218, 226, 7402, 21827, 227, 23294, 33849, 14945, 8400]


def body(text: str) -> str:
    m = re.search(r"\*\*\* ?START OF.*?\*\*\*", text)
    e = re.search(r"\*\*\* ?END OF", text)
    return text[m.end() if m else 0:e.start() if e else len(text)]


def main(src: str, work: str) -> None:
    out = Path(work)
    out.mkdir(parents=True, exist_ok=True)
    text = "\n".join(body((Path(src) / "gutenberg" / f"pg{i}.txt").read_text(encoding="utf-8",
                                                                             errors="ignore"))
                     for i in IDS)
    blocks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    (out / "train.txt").write_text("".join(b for k, b in enumerate(blocks) if k % 10 != 9))
    (out / "heldout.txt").write_text("".join(b for k, b in enumerate(blocks) if k % 10 == 9))
    print(len(blocks), "blocks")


if __name__ == "__main__":
    main(*sys.argv[1:3])
