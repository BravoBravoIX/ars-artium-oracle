"""Pre-registered tests 12-16 of v1.1 (the third pre-registration in PREREG.md) and the exploratory
checks E1-E2. Seed 20261025.

usage: WORK_DIR=work python code/machine_tests.py   (WORK_DIR holds heldout.txt from
       code/build_corpus.py)
Writes results/machine_tests.json.
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
from collections import Counter
from math import comb, gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import machine as M  # noqa: E402
import oracle as O  # noqa: E402
import stages as S  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WORK = Path(os.environ.get("WORK_DIR", str(HERE / "work")))
SEED, N = 20261025, 10_000
READINGS = {"sheets": M.PRIMARY_SHEETS, "text": M.PRIMARY_TEXT}
ANSWER_PATH = ("roots", "golden", "sub_top", "sub_bottom", "sub_result", "addition", "product")


def load():
    sh = json.loads((HERE / "data/sheets.json").read_text())
    ex = {e["id"]: e for e in json.loads((HERE / "data/examples.json").read_text())["examples"]}
    ta = json.loads((HERE / "data/text_algebra.json").read_text())
    tb = json.loads((HERE / "data/tables.json").read_text())
    return sh, ex, ta, tb


def flat(x):
    if isinstance(x, (list, tuple)):
        return [y for z in x for y in flat(z)]
    return [x]


# ------------------------------------------------------------------ printed values
def printed(sh, ex, k):
    """label -> list of printed numbers for stage 2-7 values of sheet k."""
    s = sh[k]
    if k == "C":
        roots = [v for v, _ in ex["C_sheet"]["roots"].values()]
        side = [None] * 12
        for i, v in enumerate(s["canal_side_columns"]["left_top_down"]):
            side[2 * i] = v
        for i, v in enumerate(s["canal_side_columns"]["right_top_down"]):
            side[2 * i + 1] = v
        return {"roots": roots, "side_roots": side, "cipher": flat(s["cipher"])}
    top, bot = s["subtraction"]["lines"]
    return {
        "roots": s["roots"],
        "canal": s["canal"],
        "left": flat(s["left"]),
        "right": flat(s["right"]),
        "branch_left": s["branch_left"],
        "branch_right": s["branch_right"],
        "cipher": flat(s["cipher"]),
        "golden": [s["golden"]],
        "sub_top": flat(top),
        "sub_bottom": flat(bot),
        "sub_result": flat(s["subtraction"]["result"]),
        "addition": s["addition"]["result"],
        "product": s["multiplication"]["result"],
    }


def machine_values(R: M.Run, labels) -> dict:
    out = {
        "roots": R.roots,
        "canal": R.canal,
        "left": flat(S.rows_from_grid(R.left)),
        "right": flat(S.rows_from_grid(R.right)),
        "branch_left": R.branch_left,
        "branch_right": R.branch_right,
        "cipher": flat(R.cipher),
        "golden": [R.golden],
        "sub_top": flat(R.sub["top"]),
        "sub_bottom": flat(R.sub["bottom"]),
        "sub_result": flat(R.sub["result"]),
        "addition": list(R.add),
        "product": list(R.mult["q"]) if R.mult["q"] else [None] * 3,
        "side_roots": [r for r, _ in M.side_roots(R.canal, R.crossed)],
    }
    return {k: out[k] for k in labels}


def compare(pr: dict, mv: dict) -> dict:
    res = {}
    for k, vals in pr.items():
        got = mv[k][: len(vals)]
        pairs = [(a, b) for a, b in zip(vals, got, strict=True) if a is not None]
        res[k] = {"match": sum(a == b for a, b in pairs), "n": len(pairs)}
    return res


def total(c: dict) -> tuple[int, int]:
    return sum(v["match"] for v in c.values()), sum(v["n"] for v in c.values())


def holm(ps: dict) -> dict:
    items = sorted(ps.items(), key=lambda x: x[1])
    out, run = {}, 0.0
    for j, (name, p) in enumerate(items):
        run = max(run, min(1.0, (len(items) - j) * p))
        out[name] = {"p": p, "p_holm": run, "below_0.05": run < 0.05}
    return out


# ------------------------------------------------------------------ test 12
def random_questions(rng, n):
    held = (WORK / "heldout.txt").read_text(errors="ignore").lower()
    vocab = [w for w in re.findall(r"[a-z]+", held) if 2 <= len(w) <= 13]
    return [[rng.choice(vocab) for _ in range(9)] for _ in range(n)]


def test12(sh, ex, qs):
    out = {}
    for rname, v in READINGS.items():
        rr = {}
        for k in ("B", "C", "D"):
            pr = printed(sh, ex, k)
            R = M.run(ex[f"{k}_sheet"]["words"], v)
            c = compare(pr, machine_values(R, pr))
            m, n = total(c)
            rr[k] = {"by_stage": c, "match": m, "n": n, "share": m / n}
        out[rname] = rr
    # control: the same machine (sheets' reading) on random 9-word questions
    v = READINGS["sheets"]
    prs = {k: printed(sh, ex, k) for k in ("B", "C", "D")}
    obs = {k: out["sheets"][k]["match"] for k in prs}
    ge, fails, dist = Counter(), 0, {k: [] for k in prs}
    runs = []
    for q in qs:
        try:
            R = M.run(q, v)
        except Exception:  # pre-registered: a failure scores 0
            fails += 1
            runs.append(None)
            for k in prs:
                dist[k].append(0)
            continue
        runs.append(R)
        for k, pr in prs.items():
            m, _ = total(compare(pr, machine_values(R, pr)))
            dist[k].append(m)
            ge[k] += m >= obs[k]
    ps = {k: (1 + ge[k]) / (1 + len(qs)) for k in prs}
    out["control"] = {
        "N": len(qs),
        "failures": fails,
        "random_mean": {k: sum(d) / len(d) for k, d in dist.items()},
        "random_max": {k: max(d) for k, d in dist.items()},
        "observed": obs,
        "holm": holm(ps),
        "min_p": 1 / (1 + len(qs)),
    }
    return out, runs


# ------------------------------------------------------------------ test 13: departures
def stage_local(sh, ex, k, v):
    """Each stage fed the sheet's own inputs; returns (label, index, printed, rule) misses and
    the per-label counts."""
    s = sh[k]
    pr = printed(sh, ex, k)
    words = ex[f"{k}_sheet"]["words"]
    op = O.operation1(words)
    rule_roots = [O.root(w, op.sums[i], op.l1[i], op.l4[i]).value for i, w in enumerate(words)]
    rule = {"roots": rule_roots[: len(pr["roots"])]}
    if k == "C":
        rs = pr["roots"]
        side = [None] * 12
        red = [S.reduce_root(x, v["alpha"]) for x in rs]
        for i in range(6):
            side[2 * i] = red[i]
        side[1], side[9], side[11] = red[5], red[1], red[0]  # R6, R2, R1 on the right
        rule["side_roots"] = side
        pr = {"roots": pr["roots"], "side_roots": pr["side_roots"]}
    else:
        roots, crossed = s["roots"], s["crossed"]
        lg, rg = S.grid_from_rows(s["left"]), S.grid_from_rows(s["right"])
        rule["canal"] = [S.reduce_root(x, v["alpha"]) for x in roots]
        rule["left"] = flat(S.rows_from_grid(S.left_rhomboid(s["l2"], s["l3"])))
        rule["right"] = flat(S.rows_from_grid(S.right_rhomboid(s["l4"], lg, v["diametral"])))
        rule["branch_left"] = S.branch(lg, "left", s["canal"][0], crossed[0])
        rule["branch_right"] = S.branch(rg, "right", s["canal"][0], crossed[0])
        orb = S.orbit(
            lg, rg, s["branch_left"], s["branch_right"], s["canal"], crossed, v["upper_side"]
        )
        rule["cipher"] = flat(S.cipher(orb, v["left_cols"]))
        rule["golden"] = [S.golden(roots, crossed, v["golden_cross"])]
        sub = M.subtraction(roots, crossed, v["sub_top"], v["zero_top"])
        rule["sub_top"], rule["sub_bottom"] = flat(sub["top"]), flat(sub["bottom"])
        top, bot = s["subtraction"]["lines"]
        rule["sub_result"] = [a - b for a, b in zip(flat(top), flat(bot), strict=True)]
        rule["addition"] = list(M.addition(roots, v["addition_set"]))
        res = [tuple(x) for x in s["subtraction"]["result"]]
        rule["product"] = list(M.multiplication(res, tuple(s["addition"]["result"]))["q"])
    misses, counts = [], {}
    for lab, vals in pr.items():
        n = m = 0
        for i, (a, b) in enumerate(zip(vals, rule[lab], strict=True)):
            if a is None or b is None:
                continue
            n += 1
            if a == b:
                m += 1
            else:
                misses.append({"sheet": k, "stage": lab, "i": i, "printed": a, "rule": b})
        counts[lab] = {"match": m, "n": n}
    return misses, counts


def text_checks(ta):
    """Rule applied to each text example's own printed inputs; every mismatch listed."""
    out = []

    def chk(where, item, printed_v, rule_v):
        out.append(
            {
                "where": where,
                "item": item,
                "printed": printed_v,
                "rule": rule_v,
                "match": printed_v == rule_v,
            }
        )

    for e in ta["subtraction"]:
        if "roots" in e:
            r, c = e["roots"], e["crossed"]
            roots = [r["first"], r["second"], r["penultimate"], r["last"]]
            cr = [c["first"], c["second"], c["penultimate"], c["last"]]
            sub = M.subtraction(roots, cr, "first_diff")
            chk(
                e["where"],
                f"{e['id']}: upper line from roots",
                e["top"],
                [list(x) for x in sub["top"]],
            )
            chk(
                e["where"],
                f"{e['id']}: lower line from roots",
                e["bottom"],
                [list(x) for x in sub["bottom"]],
            )
        for zt in ("algebraic", "abs_P"):
            res = []
            for (tr, tq), (br, bq) in zip(e["top"], e["bottom"], strict=True):
                res.append([abs(br), abs(bq)] if zt == "abs_P" and tr == 0 else [tr - br, tq - bq])
            chk(e["where"], f"{e['id']}: residue ({zt})", e["result"], res)
    for e in ta["addition"]:
        if "roots" in e:
            chk(
                e["where"],
                f"{e['id']}: sum of the roots it lists",
                e["result"],
                list(M.addition([0, 0] + e["roots"] + [0, 0])),
            )
        key = [x for x in e if x.startswith("rule_roots")][0]
        chk(
            e["where"],
            f"{e['id']}: rule roots of the sheet question, all middle",
            e["result"],
            list(M.addition([0, 0] + e[key] + [0, 0])),
        )
        chk(
            e["where"],
            f"{e['id']}: rule roots, last middle root left out",
            e["result"],
            list(M.addition([0, 0] + e[key] + [0, 0], "drop_last_middle")),
        )
    for e in ta["multiplication"]:
        res = e.get("residue") or e["residue_from_subtraction"]
        if "residue_printed" in e:
            chk(
                e["where"],
                f"{e['id']}: residue line as printed vs the subtraction (image 77)",
                e["residue_printed"],
                e["residue_from_subtraction"],
            )
        mres = M.multiplication([tuple(x) for x in res], tuple(e["addition"]))
        chk(e["where"], f"{e['id']}: product", e["product"], list(mres["q"]))
        if "partials" in e:
            (a1, a2), (b1, b2) = res
            x, y = e["addition"]
            part = [a1 * x, a2 * x, b1 * x, b2 * x, a1 * y, a2 * y, b1 * y, b2 * y]
            # printed order: aR*x, aQ*x, bR*x, bQ*x / aR*y, aQ*y, bR*y, bQ*y
            for i, (p, q) in enumerate(zip(e["partials"], part, strict=True)):
                chk(e["where"], f"{e['id']}: partial product {i + 1}", p, q)
    for e in ta["division"]:
        if e["golden"] not in (0, 1):
            chk(
                e["where"],
                f"{e['id']}: general division",
                "printed",
                "not coded (pages 85-86 missing)",
            )
            continue
        d = M.division(tuple(e["dividend"]), e["golden"])
        if "parts" in e:
            chk(
                e["where"],
                f"{e['id']}: thirds and quarters of the first dividend",
                e["parts"],
                [
                    [abs(d.parts[0]), abs(e["dividend"][0]) % 3],
                    [abs(d.parts[1]), abs(e["dividend"][0]) % 4],
                ],
            )
        line = [
            e["dividend"][0] + sum(abs(e["dividend"][0]) % n for n in (3, 4)),
            e["dividend"][1] + d.parts[0],
            e["dividend"][2] + d.parts[1],
        ]
        chk(e["where"], f"{e['id']}: line after adding the parts", e["first_line"], line)
        if "correctors" in e:
            chk(e["where"], f"{e['id']}: correctors", e["correctors"], list(d.correctors))
            chk(
                e["where"],
                f"{e['id']}: correctors from the printed line + 1",
                e["correctors"],
                [x + 1 for x in e["first_line"]],
            )
        if "q1" in e:
            chk(e["where"], f"{e['id']}: quotients", [e["q1"], e["q2"]], [d.q1, d.q2])
    for e in ta["quotient_use"]:
        if e["id"] == "start_cell":
            m = abs(e["q1"])
            chk(
                e["where"],
                "start cell: quotient and remainder",
                [e["quotient"], e["remainder"]],
                [m // e["cells"], m % e["cells"]],
            )
            chk(e["where"], "start cell", e["start"], M.count_off(e["q1"], e["cells"]))
        elif e["id"] == "first_letter":
            chk(
                e["where"],
                "first letter: quotient and remainder",
                [e["quotient"], e["remainder"]],
                [e["q2"] // 23, e["q2"] % 23],
            )
            chk(
                e["where"],
                "first letter (rule, from the printed quotient)",
                e["first_letter"],
                M.count_off(e["q2"], 23),
            )
            chk(
                e["where"],
                "first letter (from the printed remainder + 1)",
                e["first_letter"],
                e["remainder"] + 1,
            )
        elif e["id"] == "count_general":
            chk(e["where"], "q1 less golden", e["q1_less_golden"], e["q1"] - e["golden"])
            den = int(e["fraction"].split("/")[1])
            chk(
                e["where"],
                "denominator split in two (from the printed fraction)",
                e["parts"],
                [den // 2, den - den // 2],
            )
            chk(
                e["where"],
                "left after subtracting the printed parts",
                e["left"],
                e["q1_less_golden"] - sum(e["parts"]),
            )
        elif e["id"] == "count_maximilian":
            d1 = e["first_dividend"]
            chk(
                e["where"],
                "difference of the quotients",
                e["difference"],
                e["q_larger"] - e["q_smaller"],
            )
            chk(
                e["where"],
                "first divisor = third part of the first dividend",
                e["div1"]["by"],
                d1 // 3,
            )
            chk(
                e["where"],
                "second divisor = fourth part of the first dividend",
                e["div2"]["by"],
                d1 // 4,
            )
            q, r = divmod(e["difference"], e["div1"]["by"])
            chk(
                e["where"],
                "first division (printed numbers)",
                [e["div1"]["quotient"], e["div1"]["remainder"]],
                [q, r],
            )
            q2, r2 = divmod(e["div1"]["quotient"], e["div2"]["by"])
            chk(
                e["where"],
                "second division (printed numbers)",
                [e["div2"]["quotient"], e["div2"]["remainder"]],
                [q2, r2],
            )
            chk(
                e["where"],
                "first dividend less remainder (printed)",
                e["after_subtraction"],
                d1 - e["div1"]["remainder"] - e["div2"]["remainder"],
            )
            chk(e["where"], "plus 1 for P", e["letters_after_first"], e["after_subtraction"] + 1)
    return out


def maximilian_chain(ta):
    """The text's Maximilian count run by the rule from its own first inputs (q 6290, 1538,
    first dividend 56), every variant."""
    e = next(x for x in ta["quotient_use"] if x["id"] == "count_maximilian")
    d1 = e["first_dividend"]
    div = M.Division(True, "note5_zero", e["q_smaller"], e["q_larger"], None, (d1 // 3, d1 // 4))
    out = {}
    for cr in M.VARIANTS["count_remainders"]:
        n = M.letter_count(div, d1, cr)
        out[cr] = {"letters_after_first": n, "letters_total": n + 1}
    out["book"] = {
        "letters_after_first": e["letters_after_first"],
        "letters_total": e["letters_after_first"] + 1,
    }
    out["printed_answer_letters"] = 35
    return out


# ------------------------------------------------------------------ test 14: clustering
def test14(misses_bd, counts_bd):
    n_a = sum(c[lab]["n"] for c in counts_bd for lab in c if lab in ANSWER_PATH)
    n_all = sum(c[lab]["n"] for c in counts_bd for lab in c)
    k = len(misses_bd)
    j = sum(m["stage"] in ANSWER_PATH for m in misses_bd)

    def hyper_ge(j, k):
        return sum(
            comb(n_a, x) * comb(n_all - n_a, k - x) for x in range(j, min(k, n_a) + 1)
        ) / comb(n_all, k)

    p_min = hyper_ge(min(k, n_a), k) if k else 1.0
    by_stage = Counter(m["stage"] for m in misses_bd)
    return {
        "N_values": n_all,
        "answer_path_values": n_a,
        "departures": k,
        "departures_in_answer_path": j,
        "expected_in_answer_path": k * n_a / n_all,
        "p_cluster": hyper_ge(j, k) if k else 1.0,
        "min_achievable_p": p_min,
        "informative": p_min < 0.05,
        "by_stage": dict(by_stage),
    }


# ------------------------------------------------------------------ test 15: answers
PRINTED_ANSWER = {"B": {"letters": 67, "first": 7}, "D": {"letters": 35, "first": 4}}


def summary(R: M.Run) -> dict:
    return {
        "golden": R.golden,
        "roots": R.roots,
        "crossed": R.crossed,
        "multiplication": R.mult,
        "division_coded": bool(R.div and R.div.coded),
        "stop": R.stop,
        "start_cell": R.start_cell,
        "first_letter": R.first_letter,
        "letters_total": None if R.letters_after_first is None else R.letters_after_first + 1,
    }


def test15(sh, ex, runs):
    out = {}
    for k in ("B", "D"):
        o = {}
        for rname, v in READINGS.items():
            o[f"rule_{rname}"] = summary(M.run(ex[f"{k}_sheet"]["words"], v))
            # the sheet's own roots, rest by rule
            R = M.Run(ex[f"{k}_sheet"]["words"], dict(M.PRIMARY_TEXT, **v))
            R.op1 = O.operation1(R.words)
            R.roots, R.crossed = list(sh[k]["roots"]), list(sh[k]["crossed"])
            R.canal = [S.reduce_root(x, R.v["alpha"]) for x in R.roots]
            o[f"sheet_roots_{rname}"] = summary(M.finish(R))
        o["printed_answer"] = PRINTED_ANSWER[k]
        out[k] = o
    ok = [R for R in runs if R is not None]
    reach = [R for R in ok if R.letters_after_first is not None]
    tot = Counter(R.letters_after_first + 1 for R in reach)
    out["control"] = {
        "N_run": len(ok),
        "golden_distribution": dict(sorted(Counter(R.golden for R in ok).items())[:12]),
        "share_golden_0_or_1": sum(R.golden in (0, 1) for R in ok) / len(ok),
        "reached_letter_count": len(reach),
        "letters_total_quantiles": quantiles(sorted(tot.elements())),
        "share_total_35": tot[35] / max(len(reach), 1),
        "share_total_67": tot[67] / max(len(reach), 1),
        "share_total_nonpositive": sum(v for t, v in tot.items() if t <= 1) / max(len(reach), 1),
        "first_letter_distribution": dict(sorted(Counter(R.first_letter for R in reach).items())),
    }
    return out


def quantiles(xs):
    if not xs:
        return None
    return {
        q: xs[min(len(xs) - 1, int(q * len(xs)))] for q in (0.0, 0.05, 0.25, 0.5, 0.75, 0.95)
    } | {"max": xs[-1]}


# ------------------------------------------------------------------ test 16: tables needed
CLASSES = (
    "multiple",
    "superparticular",
    "superpartient",
    "multiple_superparticular",
    "multiple_superpartient",
    "equality",
    "zero",
)
STATUS = {
    "multiple": "table missing (pp. 105-106)",
    "superparticular": "table present",
    "superpartient": "table present",
    "multiple_superparticular": "table blank; built from the missing multiple table",
    "multiple_superpartient": "table blank; built from the missing multiple table",
    "equality": "table blank; rule given (double less one)",
    "zero": "rule given (read as 1)",
}


def classes_of(cipher, canal, crossed):
    roots = M.side_roots(canal, crossed)
    return Counter(M.proportion_class(a, roots[i][0]) for i, row in enumerate(cipher) for a in row)


def test16(sh, ex, runs, tb):
    listed = {r[0] for t in tb.values() if isinstance(t, dict) for r in t["rows"]}
    out = {}
    for k in ("B", "D"):
        s = sh[k]
        c_sheet = classes_of(s["cipher"], s["canal"], s["crossed"])
        R = M.run(ex[f"{k}_sheet"]["words"], M.PRIMARY_SHEETS)
        c_rule = classes_of(R.cipher, R.canal, R.crossed)
        out[k] = {"sheet_cipher": dict(c_sheet), "rule_cipher": dict(c_rule)}
    agg = Counter()
    beyond = Counter()
    for R in runs:
        if R is None:
            continue
        roots = M.side_roots(R.canal, R.crossed)
        for i, row in enumerate(R.cipher):
            for a in row:
                c = M.proportion_class(a, roots[i][0])
                agg[c] += 1
                if c in ("superparticular", "superpartient"):
                    r = roots[i][0]
                    p, q = max(a, r), min(a, r)
                    g = gcd(p, q)
                    beyond[f"{p // g}:{q // g}" in listed] += 1
    n = sum(agg.values())
    out["control_all_cells"] = {
        "cells": n,
        "share": {c: agg[c] / n for c in CLASSES},
        "status": STATUS,
        "share_needing_missing_multiple_table": sum(
            agg[c] for c in ("multiple", "multiple_superparticular", "multiple_superpartient")
        )
        / n,
        "particular_ratios_in_listed_rows": beyond[True],
        "particular_ratios_not_in_listed_rows": beyond[False],
    }
    return out


# ------------------------------------------------------------------ exploratory
def e1_tables(tb):
    """EXPLORATORY: internal arithmetic pattern of each table, read off its first rows."""
    out = {}
    pats = {
        "superparticular": lambda r: [
            2 * r[0] + 1,
            r[0] + r[1],
            2 * (r[0] + r[1]) + 3,
            (r[0] + r[1]) + r[3],
            2 * r[4] + 9,
        ],
        "superpartient": lambda r: [None, r[0] + r[1], r[2] + r[0], r[2] + r[3], r[4] + r[2]],
    }
    for name, f in pats.items():
        bad = []
        for row in tb[name]["rows"]:
            vals = row[1:]
            exp = f(vals)
            for i, e in enumerate(exp):
                if e is not None and vals[i + 1] != e:
                    bad.append(
                        {"row": row[0], "column": i + 2, "printed": vals[i + 1], "pattern": e}
                    )
        out[name] = {"rows": len(tb[name]["rows"]), "breaks": bad}
    return out


def e2_general_division(ta):
    """EXPLORATORY: internal arithmetic of the one general division example (image 82)."""
    e = next(x for x in ta["division"] if x["id"] == "general_golden_7")
    d, L = e["dividend"], e["lines"]
    return {
        "Q_less_under": [d[0] - L["under"][0], L["remainder"][0]],
        "C_less_under": [d[1] - L["under"][1], L["remainder"][1]],
        "box_C": [L["box"][1][0] + L["box"][0][0], L["remainder"][1]],
        "box_QQ": [L["box"][1][1] + L["box"][0][1], d[2]],
        "C_over_golden_squared": [d[1] // 49, d[1] % 49],
        "q1_printed": e["q1"],
    }


def main() -> None:
    sh, ex, ta, tb = load()
    rng = random.Random(SEED)
    qs = random_questions(rng, N)
    res: dict = {"seed": SEED, "N": N}
    res["test12_chained"], runs = test12(sh, ex, qs)
    misses, counts = [], []
    conv = {}
    for k in ("B", "D", "C"):
        m, c = stage_local(sh, ex, k, READINGS["sheets"])
        misses += m
        if k != "C":
            counts.append(c)
        mt, _ = stage_local(sh, ex, k, READINGS["text"])
        conv[k] = {"misses_sheets_reading": len(m), "misses_text_reading": len(mt)}
    tc = text_checks(ta)
    res["test13_departures"] = {
        "sheets": misses,
        "sheets_text_vs_sheets_reading": conv,
        "text_examples": tc,
        "text_examples_mismatches": [x for x in tc if not x["match"]],
        "maximilian_chain": maximilian_chain(ta),
    }
    res["test14_clustering"] = test14([m for m in misses if m["sheet"] in ("B", "D")], counts)
    res["test15_answers"] = test15(sh, ex, runs)
    res["test16_tables"] = test16(sh, ex, runs, tb)
    res["exploratory"] = {
        "E1_tables": e1_tables(tb),
        "E2_general_division": e2_general_division(ta),
    }
    (HERE / "results/machine_tests.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    t12 = res["test12_chained"]
    for r in READINGS:
        print(r, {k: (t12[r][k]["match"], t12[r][k]["n"]) for k in ("B", "C", "D")})
    print(
        "control",
        t12["control"]["random_mean"],
        t12["control"]["random_max"],
        t12["control"]["holm"],
    )
    print(
        "departures",
        len(misses),
        "text mismatches",
        len(res["test13_departures"]["text_examples_mismatches"]),
    )
    print("t14", res["test14_clustering"])
    print(
        "t15",
        json.dumps(
            {
                k: {
                    x: (y["golden"], y["stop"], y["letters_total"])
                    for x, y in v.items()
                    if isinstance(y, dict) and "golden" in y
                }
                for k, v in res["test15_answers"].items()
                if k in ("B", "D")
            }
        ),
    )


if __name__ == "__main__":
    main()
