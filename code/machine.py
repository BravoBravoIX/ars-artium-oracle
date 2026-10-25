"""The Ars artium machine chained end to end (v1.1): question -> answer inputs, as LJS 251 writes
the rules (part 1, chapters II-X). Stages 1-2 come from oracle.py and stages 3-6 from stages.py
unchanged; this file adds the chaining, the algebra (chapter VIII: subtraction lines built from
the roots, addition, multiplication with its zero cases), the division where the text gives it
in full (golden number 0 or 1, chapter VIII notes 5-7), the use of the quotients (chapter IX:
starting cell, first letter, number of letters) and the read-out of the cipher (chapter X).

What is NOT coded, and why (third pre-registration in PREREG.md):
- the division for a golden number of 2 or more: its rule ran onto pages 85-86 of LJS 251,
  which are missing (the page numbers jump from 84 to 87, and the catchword 'per' on p. 84 does
  not join the top of p. 87);
- the turning of cipher numbers into letters (chapter X, tables): the first table
  ('Tabula prima proportionalitatis multiplicis', listed in the index on p. 118) was on pages
  105-106, also missing; the tables of compound proportions and of equality are ruled but
  blank. read_out() stops at the numbers and their proportion classes.

Every place where the text is silent or reads two ways is a named variant (VARIANTS); the
first value is the reading of the rule text. Only 9-word questions are run (the right
rhomboid's later fills, needed for other lengths, are not coded; all three sheets have 9).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import gcd

import oracle as O
import stages as S

VARIANTS = {
    # chapter V: roots in the canal and the cipher's side columns 'reject the alphabetic
    # number': 23 (chapter IX) or 24 (what the sheets do)
    "alpha": (23, 24),
    # chapter V / image 58 vs the sheets
    "upper_side": ("interior", "exterior"),
    "left_cols": ("A_first", "D_first"),
    "diametral": ("mirror", "point"),
    "golden_cross": ("apply", "ignore"),
    # chapter VIII (image 76): the quantities forming the FIRST difference of the golden
    # number (last and first roots) make the upper subtraction line; the sheets put the
    # second-difference pair (penultimate and second roots) on top
    "sub_top": ("first_diff", "second_diff"),
    # image 77, third example: a zero quantity in the upper line; algebraic subtraction, or
    # the book's result (bottom quantity's magnitude written with P)
    "zero_top": ("algebraic", "abs_P"),
    # chapter VIII (image 78): addition takes all roots except the four of the subtraction;
    # both worked text examples leave out root n-2 as well
    "addition_set": ("all_middle", "drop_last_middle"),
    # chapter VIII note 5 (golden 1, image 86): first and second quotients with the part
    # added only, or with the unit as well
    "g1_quotient": ("part_only", "part_and_unit"),
    # chapter IX (image 90): remainders subtracted from the first dividend: both divisions'
    # remainders, or the first only ('subduco solum 16')
    "count_remainders": ("both", "first_only"),
}

PRIMARY_TEXT = {k: v[0] for k, v in VARIANTS.items()}
# the reading that fits the sheets (v1.0 tests 6-10; sub_top from the sheets' layout)
PRIMARY_SHEETS = dict(PRIMARY_TEXT, alpha=24, upper_side="exterior", sub_top="second_diff")


def sgn(x: int) -> int:
    return -1 if x < 0 else 1


# ---------------------------------------------------------------- stage 7: algebra
def golden_pairs(roots: list[int], crossed: list[bool]) -> dict:
    """Chapter VI: first difference from (last, first), the first on the right; second from
    (penultimate, second), the second on the right; a single crossed root changes side.
    Returns each pair as (left, right) and whether it was swapped."""

    def pair(a, ca, b, cb):
        return ((b, a), True) if ca != cb else ((a, b), False)

    first, s1 = pair(roots[-1], crossed[-1], roots[0], crossed[0])
    second, s2 = pair(roots[-2], crossed[-2], roots[1], crossed[1])
    return {"first": first, "second": second, "swapped": (s1, s2)}


def signed_line(pair: tuple[int, int]) -> list[tuple[int, int]]:
    """Image 76-78: the larger root P, the smaller M; equal roots both P; a zero root P.
    Each quantity as (R, Q) with the sign carried: (s*r, s*r*r)."""
    a, b = pair
    if a == b:
        sa = sb = 1
    else:
        sa, sb = (1, -1) if a > b else (-1, 1)
    return [(sa * a, sa * a * a), (sb * b, sb * b * b)]


def subtraction(roots, crossed, sub_top="first_diff", zero_top="algebraic") -> dict:
    gp = golden_pairs(roots, crossed)
    top_pair, bot_pair = (
        (gp["first"], gp["second"]) if sub_top == "first_diff" else (gp["second"], gp["first"])
    )
    top, bot = signed_line(top_pair), signed_line(bot_pair)
    res = []
    for (tr, tq), (br, bq) in zip(top, bot, strict=True):
        if zero_top == "abs_P" and tr == 0:
            res.append((abs(br), abs(bq)))
        else:
            res.append((tr - br, tq - bq))
    return {"top": top, "bottom": bot, "result": res}


def addition(roots, addition_set="all_middle") -> tuple[int, int]:
    mid = roots[2:-2]
    if addition_set == "drop_last_middle":
        mid = mid[:-1]
    return sum(mid), sum(r * r for r in mid)


def multiplication(res: list[tuple[int, int]], add: tuple[int, int]) -> dict:
    """Images 79-81. General: each residue quantity times each addition quantity, summed by
    species (Q, C, QQ). Both residues zero: addition root times its square -> (R, Q, C).
    Addition zero: residue roots summed, squares summed, then multiplied -> (R, Q, C)."""
    zero_res = all(r == 0 and q == 0 for r, q in res)
    if zero_res and add == (0, 0):
        return {"case": "undefined", "q": None}
    if zero_res:
        a, b = add
        return {"case": "residues_zero", "species": ("R", "Q", "C"), "q": (a, b, a * b)}
    if add == (0, 0):
        sr, sq = sum(r for r, _ in res), sum(q for _, q in res)
        return {"case": "addition_zero", "species": ("R", "Q", "C"), "q": (sr, sq, sr * sq)}
    q, c, qq = S.multiply(res, add)
    return {"case": "general", "species": ("Q", "C", "QQ"), "q": (q, c, qq)}


def _part(x: int, n: int) -> tuple[int, int]:
    """Signed integer part and remainder of x / n (the sign of x carried, as P/M)."""
    return sgn(x) * (abs(x) // n), sgn(x) * (abs(x) % n)


@dataclass
class Division:
    coded: bool
    why: str = ""
    q1: int | None = None
    q2: int | None = None
    correctors: tuple | None = None
    parts: tuple | None = None  # (t3, t4): integer parts of the first dividend


def division(dividend: tuple[int, int, int], g: int, g1_quotient: str = "part_only") -> Division:
    """Chapter VIII notes 5-7 (images 85-87): golden number 0 or 1 only."""
    if g not in (0, 1):
        return Division(False, "golden number >= 2: rule on the missing pages 85-86")
    d1, d2, d3 = dividend
    unit = 1 if g == 1 else 0
    if d1 == 0:  # note 6
        return Division(True, "note6", d2, d3, (1, d2 + unit, d3 + unit), (0, 0))
    if d3 == 0:  # note 7 ('in 6 primum, deinde in 4')
        t6, _ = _part(d1, 6)
        t4, _ = _part(d1, 4)
        return Division(
            True, "note7", d2, t4 + unit, (d1 + unit, d2 + t6 + unit, t4 + unit), (t6, t4)
        )
    t3, r3 = _part(d1, 3)
    t4, r4 = _part(d1, 4)
    corr = (d1 + r3 + r4 + unit, d2 + t3 + unit, d3 + t4 + unit)
    if g == 0:
        return Division(True, "note5_zero", d2, d3, corr, (t3, t4))
    extra = 1 if g1_quotient == "part_and_unit" else 0
    return Division(True, "note5_one", d2 + t3 + extra, d3 + t4 + extra, corr, (t3, t4))


# ---------------------------------------------------------------- chapter IX
def count_off(q: int, n: int) -> int:
    """Image 88-89: remainder of q / n (or q itself when smaller), plus 1 for P, minus 1 for M;
    0 is read as n and n + 1 as 1 (not stated)."""
    m = abs(q)
    r = m % n if m >= n else m
    r += 1 if q >= 0 else -1
    return (r - 1) % n + 1


def letter_count(div: Division, d1: int, count_remainders: str = "both") -> int | None:
    """Image 89-90, case of golden 0 or 1: larger minus smaller quotient; divide by the
    first dividend's third part, the quotient by its fourth part; subtract what is left from
    the first dividend; add 1 for P (subtract for M). Returns letters after the first one."""
    delta = abs(div.q2 - div.q1)
    rems = []
    x = delta
    for t in div.parts:
        if t == 0:
            continue
        x, r = divmod(x, abs(t))
        rems.append(r)
    if not rems:
        sub = delta
    else:
        sub = rems[0] if count_remainders == "first_only" else sum(rems)
    n = abs(d1) - sub
    n += 1 if d1 >= 0 else -1
    return n


# ---------------------------------------------------------------- chapter X: read-out
def side_roots(canal: list[int], crossed: list[bool]) -> list[tuple[int, bool]]:
    """Chapter VII (image 69): left column (odd rows) R1..R6 top down; right column (even
    rows) from the bottom up: R1 (repeated), R2 (repeated), R9, R8, R7, R6. Row k root."""
    n = len(canal)
    left = [(canal[i], crossed[i]) for i in range(6)]
    right_bottom_up = [(canal[0], crossed[0]), (canal[1], crossed[1])] + [
        (canal[i], crossed[i]) for i in range(n - 1, 4, -1)
    ]
    right = right_bottom_up[::-1]
    rows = []
    for k in range(12):
        rows.append(left[k // 2] if k % 2 == 0 else right[k // 2])
    return rows


def proportion_class(a: int, r: int) -> str:
    """Kind of ratio between a cipher number and its row root (chapter X)."""
    if a == 0 or r == 0:
        return "zero"
    p, q = max(a, r), min(a, r)
    g = gcd(p, q)
    p, q = p // g, q // g
    if p == q:
        return "equality"
    if q == 1:
        return "multiple"
    if p < 2 * q:
        return "superparticular" if p - q == 1 else "superpartient"
    return "multiple_superparticular" if p % q == 1 else "multiple_superpartient"


def read_out(cipher: list[list[int]], roots: list[tuple[int, bool]], start: int, n: int):
    """Chapter X (images 93-94): from the starting cell, the rest of its row, then the next
    rows; a crossed row root reverses the row; after the last row back to the first (not
    stated). Returns n (number, root) pairs."""
    width = len(cipher[0])
    order = []
    for k in range(len(cipher)):
        cells = list(range(width))
        if roots[k][1]:
            cells = cells[::-1]
        order += [(k, c) for c in cells]
    flat_index = {(k, c): k * width + c for k in range(len(cipher)) for c in range(width)}
    start_pos = next(i for i, kc in enumerate(order) if flat_index[kc] == start - 1)
    out = []
    i = start_pos
    while len(out) < n:
        k, c = order[i % len(order)]
        out.append((cipher[k][c], roots[k][0]))
        i += 1
    return out


# ---------------------------------------------------------------- the chain
@dataclass
class Run:
    words: list[str]
    v: dict
    op1: O.Op1 = None
    roots: list[int] = field(default_factory=list)
    crossed: list[bool] = field(default_factory=list)
    canal: list[int] = field(default_factory=list)
    left: dict = None
    right: dict = None
    branch_left: list[int] = None
    branch_right: list[int] = None
    cipher: list[list[int]] = None
    golden: int = None
    sub: dict = None
    add: tuple = None
    mult: dict = None
    div: Division = None
    start_cell: int | None = None
    first_letter: int | None = None
    letters_after_first: int | None = None
    readout: list | None = None
    stop: str = ""


def run(words: list[str], v: dict | None = None) -> Run:
    v = dict(PRIMARY_TEXT, **(v or {}))
    if len(words) != 9:
        raise ValueError("only 9-word questions are coded")
    R = Run(words, v)
    op = O.operation1(words)
    R.op1 = op
    rs = [O.root(w, op.sums[i], op.l1[i], op.l4[i]) for i, w in enumerate(words)]
    R.roots, R.crossed = [r.value for r in rs], [r.reversed for r in rs]
    R.canal = [S.reduce_root(x, v["alpha"]) for x in R.roots]
    return finish(R)


def finish(R: Run) -> Run:
    """Stages 3-9 from R.op1 (lines 2-4), R.roots, R.crossed, R.canal."""
    v, op = R.v, R.op1
    R.left = S.left_rhomboid(op.l2, op.l3)
    R.right = S.right_rhomboid(op.l4, R.left, v["diametral"])
    R.branch_left = S.branch(R.left, "left", R.canal[0], R.crossed[0])
    R.branch_right = S.branch(R.right, "right", R.canal[0], R.crossed[0])
    orb = S.orbit(
        R.left, R.right, R.branch_left, R.branch_right, R.canal, R.crossed, v["upper_side"]
    )
    R.cipher = S.cipher(orb, v["left_cols"])
    R.golden = S.golden(R.roots, R.crossed, v["golden_cross"])
    R.sub = subtraction(R.roots, R.crossed, v["sub_top"], v["zero_top"])
    R.add = addition(R.roots, v["addition_set"])
    R.mult = multiplication(R.sub["result"], R.add)
    if R.mult["q"] is None:
        R.stop = "multiplication undefined"
        return R
    R.div = division(R.mult["q"], R.golden, v["g1_quotient"])
    if not R.div.coded:
        R.stop = R.div.why
        return R
    cells = 12 * len(R.words)
    R.start_cell = count_off(R.div.q1, cells)
    R.first_letter = count_off(R.div.q2, 23)
    R.letters_after_first = letter_count(R.div, R.mult["q"][0], v["count_remainders"])
    if R.letters_after_first is not None and R.letters_after_first > 0:
        R.readout = read_out(
            R.cipher, side_roots(R.canal, R.crossed), R.start_cell, R.letters_after_first
        )
    R.stop = "read-out (tables missing or blank)"
    return R
