"""Write results/run_records.json: SHA-256 of every input and code file, seeds and the Python
version, so a rerun can be compared with the published one. No times are recorded, so the file
is the same on every rerun of the same inputs.
usage: python code/run_records.py SOURCE_DIR WORK_DIR
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(src: str, work: str) -> None:
    rec = {
        "python": platform.python_version(),
        "seeds": [20261020, 20261025],
        "code": {p.name: sha(p) for p in sorted((HERE / "code").glob("*.py"))},
        "data": {str(p.relative_to(HERE)): sha(p) for p in sorted((HERE / "data").glob("*.json"))},
        "sources": {str(p.relative_to(src)): sha(p)
                    for p in sorted((Path(src) / "gutenberg").glob("*.txt"))},
        "work": {p.name: sha(p) for p in sorted(Path(work).glob("*.txt"))},
        "results": {p.name: sha(p) for p in sorted((HERE / "results").glob("*.json"))
                    if p.name != "run_records.json"},
    }
    (HERE / "results/run_records.json").write_text(json.dumps(rec, indent=1) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])
