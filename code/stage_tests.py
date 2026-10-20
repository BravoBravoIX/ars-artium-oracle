"""Pre-registered tests 6-11 (PREREG.md, second document). Seed 20261020.

usage: python code/stage_tests.py
Writes results/stage_tests.json.
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stages as S  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
SEED, N = 20261020, 10_000


def cells(rows):
    return [x for r in rows for x in r]


def score(a, b):
    fa, fb = cells(a), cells(b)
    return sum(x == y for x, y in zip(fa, fb, strict=True)), len(fa)


def build_cipher(sh, upper_side, left_cols):
    left, right = S.grid_from_rows(sh["left"]), S.grid_from_rows(sh["right"])
    orb = S.orbit(left, right, sh["branch_left"], sh["branch_right"], sh["canal"],
                  sh["crossed"], upper_side)
    return S.cipher(orb, left_cols)


def main() -> None:
    rng = random.Random(SEED)
    d = json.loads((HERE / "data/sheets.json").read_text())
    res: dict = {"seed": SEED, "N": N}

    # test 6: rhomboids
    t6 = {}
    for k in ("B", "D"):
        sh = d[k]
        lg = S.left_rhomboid(sh["l2"], sh["l3"])
        out = {"left": score(S.rows_from_grid(lg), sh["left"])}
        for dia in S.VARIANTS["diametral"]:
            rg = S.right_rhomboid(sh["l4"], S.grid_from_rows(sh["left"]), dia)
            out[f"right_{dia}"] = score(S.rows_from_grid(rg), sh["right"])
        t6[k] = out
    res["test6_rhomboids"] = t6

    # test 7: branches
    t7 = {}
    for k in ("B", "D"):
        sh = d[k]
        lg, rg = S.grid_from_rows(sh["left"]), S.grid_from_rows(sh["right"])
        r1, c1 = sh["canal"][0], sh["crossed"][0]
        bl, br = S.branch(lg, "left", r1, c1), S.branch(rg, "right", r1, c1)
        t7[k] = {"left": [bl, sh["branch_left"]], "right": [br, sh["branch_right"]],
                 "match": bl == sh["branch_left"] and br == sh["branch_right"]}
    res["test7_branches"] = t7

    # test 8: canal roots reduced by 23 or 24
    t8 = {}
    for k in ("B", "D"):
        sh = d[k]
        t8[k] = {str(a): sum(S.reduce_root(r, a) == c for r, c in zip(sh["roots"], sh["canal"],
                                                                     strict=True))
                 for a in S.VARIANTS["alpha"]}
        t8[k]["n"] = len(sh["roots"])
    res["test8_canal"] = t8

    # test 9: orbit -> cipher
    t9: dict = {}
    for k, other in (("B", "D"), ("D", "B")):
        sh = d[k]
        target = sh["cipher"]
        grid = {}
        for us in S.VARIANTS["upper_side"]:
            for lc in S.VARIANTS["left_cols"]:
                ours = build_cipher(sh, us, lc)
                m, n = score(ours, target)
                grid[f"{us}+{lc}"] = {"match": m, "n": n,
                                      "multiset_overlap": sum((Counter(cells(ours))
                                                               & Counter(cells(target))).values())}
        text_key = "interior+A_first"
        best_key = max(grid, key=lambda x: grid[x]["match"])
        out = {"variants": grid, "text_reading": text_key, "best": best_key}
        for label, key in (("text", text_key), ("best", best_key)):
            us, lc = key.split("+")
            ours = build_cipher(sh, us, lc)
            obs = grid[key]["match"]
            flat = cells(target)
            ge = 0
            for _ in range(N):
                rng.shuffle(flat)
                perm = [flat[i * 9:(i + 1) * 9] for i in range(12)]
                ge += score(ours, perm)[0] >= obs
            out[f"p_shuffle_{label}"] = (1 + ge) / (1 + N)
            wrong = build_cipher(d[other], us, lc)
            out[f"wrong_inputs_match_{label}"] = score(wrong, target)[0]
        rows = []
        us, lc = best_key.split("+")
        ours = build_cipher(sh, us, lc)
        for i in range(12):
            rows.append({"row": i + 1, "ours": ours[i], "sheet": target[i],
                         "match": sum(a == b for a, b in zip(ours[i], target[i], strict=True))})
        out["rows_best"] = rows
        t9[k] = out
    ps = sorted(((f"{k}_{lab}", t9[k][f"p_shuffle_{lab}"]) for k in t9
                 for lab in ("text", "best")), key=lambda x: x[1])
    holm, run = {}, 0.0
    for j, (name, p) in enumerate(ps):
        run = max(run, min(1.0, (len(ps) - j) * p))
        holm[name] = {"p": p, "p_holm": run}
    t9["holm"] = holm
    res["test9_cipher"] = t9

    # test 10: golden number
    t10 = {}
    for k in ("B", "D"):
        sh = d[k]
        t10[k] = {rule: S.golden(sh["canal"], sh["crossed"], rule)
                  for rule in S.VARIANTS["golden_cross"]}
        t10[k]["sheet"] = sh["golden"]
    for i, ex in enumerate(d["text_golden_examples"]):
        (r1, rl), (r2, rp) = ex["first"], ex["second"]
        (c1, cl), (c2, cp) = ex["crossed_first"], ex["crossed_second"]
        t10[f"text{i + 1}"] = {rule: S.golden4(r1, r2, rp, rl, c1, c2, cp, cl, rule)
                               for rule in S.VARIANTS["golden_cross"]}
        t10[f"text{i + 1}"]["book"] = ex["book"]
    res["test10_golden"] = t10

    # test 11: algebra arithmetic
    t11 = {}
    for k in ("B", "D"):
        sh = d[k]
        top, bottom = sh["subtraction"]["lines"]
        res_sub = sh["subtraction"]["result"]
        sub_ok = all(abs(t[i] - u[i]) == abs(r[i]) for t, u, r in zip(top, bottom, res_sub,
                                                                       strict=True)
                     for i in (0, 1))
        add = S.addition(sh["addition"]["roots"])
        mul = S.multiply([tuple(x) for x in res_sub], tuple(sh["addition"]["result"]))
        t11[k] = {"addition": [list(add), sh["addition"]["result"]],
                  "addition_ok": list(add) == sh["addition"]["result"],
                  "multiplication": [list(mul), sh["multiplication"]["result"]],
                  "multiplication_ok": list(mul) == sh["multiplication"]["result"],
                  "subtraction_magnitudes_ok": sub_ok}
    ta = d["text_addition_maximilian"]
    t11["text_maximilian_addition"] = {"ours": list(S.addition(ta["roots"])), "book": ta["book"]}
    res["test11_algebra"] = t11

    (HERE / "results/stage_tests.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "test9_cipher"}, indent=1))
    for k in ("B", "D"):
        t = t9[k]
        print(k, {v: t["variants"][v]["match"] for v in t["variants"]}, "best", t["best"],
              {x: t[x] for x in t if x.startswith(("p_", "wrong"))})
    print(t9["holm"])


if __name__ == "__main__":
    main()
