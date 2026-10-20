"""EXPLORATORY (after test 9 was scored): where sheet D's cipher departs from the rule.

Two systematic departures account for all but one of D's misses:
1. both lower semidiameters use root 1 (8) where the text says root 2 (11);
2. the right semicircle's rings 4-9 take the canal roots one place late (root 4 skipped, root 2
   repeated at the end): 8, 11, 3, 5, 10, 15+, 12, 4+, 11.
Writes results/explore_d.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stages as S  # noqa: E402
from oracle import diff  # noqa: E402

HERE = Path(__file__).resolve().parents[1]


def run(lower_root1: bool, skipped: bool) -> int:
    d = json.loads((HERE / "data/sheets.json").read_text())["D"]
    lg, rg = S.grid_from_rows(d["left"]), S.grid_from_rows(d["right"])
    orb = S.orbit(lg, rg, d["branch_left"], d["branch_right"], d["canal"], d["crossed"],
                  "exterior")
    rr = [8, 11, 3, 5, 10, 15, 12, 4, 11]
    rc = [False, False, False, False, False, True, False, True, False]
    for side, rh in (("right", rg), ("left", lg)):
        _, lo = S.semid_sequences(side, "exterior")
        for k in range(9):
            if lower_root1:
                orb[side][k][5] = diff(d["canal"][0], rh[lo[k]])
            if skipped and side == "right":
                b = d["branch_right"][::-1] if rc[k] else d["branch_right"]
                orb[side][k][1:5] = [diff(rr[k], x) for x in b]
    c = S.cipher(orb, "A_first")
    return sum(a == b for x, y in zip(c, d["cipher"], strict=True)
               for a, b in zip(x, y, strict=True))


def main() -> None:
    out = {f"lower_root1={a},skipped_root={b}": run(a, b) for a in (False, True)
           for b in (False, True)}
    out["n"] = 108
    (HERE / "results/explore_d.json").write_text(json.dumps(out, indent=1))
    print(out)


if __name__ == "__main__":
    main()
