"""Test 1: do the written rules of operations 1-2 reproduce the book's own worked numbers?

usage: python code/reproduce.py [--variant k=v ...]
Writes results/reproduction.json and prints a table.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import oracle as O  # noqa: E402

HERE = Path(__file__).resolve().parents[1]


def compare(ex: dict, five_digit: str = "pairs", no_line: str = "sum") -> list[dict]:
    rows = []
    op = O.operation1(ex["words"], five_digit)

    def add(stage, i, book, ours):
        rows.append({"example": ex["id"], "stage": stage, "i": i, "book": book, "ours": ours,
                     "match": book == ours})

    for i, s in enumerate(ex.get("sums", [])):
        add("sum", i, s, op.sums[i])
    for i, s in enumerate(ex.get("l1", [])):
        add("line1", i, s, "".join(map(str, op.l1[i])))
    for i, s in enumerate(ex.get("l2", [])):
        add("line2", i, s, op.l2[i])
    for i, s in enumerate(ex.get("l3", [])):
        add("line3", i, s, op.l3[i])
    for i, s in enumerate(ex.get("pairs", [])):
        a, b = op.pairs[i]
        add("pair", i, s, f"{a}{b}")
    for i, s in enumerate(ex.get("l4", [])):
        add("line4" if i < len(ex["words"]) - 1 else "line4_last", i, s, op.l4[i])
    for w, s in ex.get("pyramid_last", {}).items():
        lines = O.pyramid(w)
        add("pyramid", w, s, lines[-1] if len(lines) > 1 else "(none)")
    for w, (v, mark) in ex.get("roots", {}).items():
        i = ex["words"].index(w)
        r = O.root(w, op.sums[i], op.l1[i], op.l4[i], no_line)
        rows.append({"example": ex["id"], "stage": "root", "i": w, "book": [v, mark],
                     "ours": [r.value, r.reversed], "case": r.case,
                     "match": v == r.value, "mark_match": mark == r.reversed})
    return rows


def main() -> None:
    data = json.loads((HERE / "data/examples.json").read_text())
    rows = []
    for ex in data["examples"]:
        rows += compare(ex)
    out = {"rows": rows, "by_stage": {}}
    for r in rows:
        st = out["by_stage"].setdefault(r["stage"], {"n": 0, "match": 0})
        st["n"] += 1
        st["match"] += int(r["match"])
    (HERE / "results/reproduction.json").write_text(json.dumps(out, indent=1))
    for k, v in out["by_stage"].items():
        print(f"{k:12s} {v['match']}/{v['n']}")
    for r in rows:
        if not r["match"] or r.get("mark_match") is False:
            print("MISS", r)


if __name__ == "__main__":
    main()
