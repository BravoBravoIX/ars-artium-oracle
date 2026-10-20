"""Stages 3-7 of the Ars artium machine (chapters IV-VIII of LJS 251), as written, for queries
of 7-10 words (the 32-cell rhomboid; all three surviving example sheets have 9 words).

Each function takes the book's own values for its inputs, so every stage can be tested on its
own ("stage-local"). Where the text and the book's figures can be read two ways, the choice is
a named variant (VARIANTS); the first value listed is the reading of the rule text.
"""

from __future__ import annotations

from oracle import diff

# numbered positions of the 32-cell rhomboid: row -> lattice columns (1..7)
COLS = [[4], [3, 5], [2, 4, 6], [1, 3, 5, 7], [1, 3, 5, 7], [2, 4, 6], [3, 5], [4]]
POS = [(r, c) for r, cs in enumerate(COLS) for c in cs]          # 20 positions, reading order

VARIANTS = {
    # chapter V (image 54) and the demonstration figure (image 58): the upper semidiameter
    # runs down the side away from the branch; the example sheets run down the branch side.
    "upper_side": ("interior", "exterior"),
    # chapter IV (image 44) 'diametraliter': mirror across the middle, or through the centre
    "diametral": ("mirror", "point"),
    # chapter V (image 48) roots in the canal 'reject the alphabetic number': 23 (chapter IX)
    # or 24 (what the sheets do)
    "alpha": (23, 24),
    # chapter VII: order of the left semicircle's columns going round from the bottom
    "left_cols": ("A_first", "D_first"),
    # chapter VI (image 66): the cross rule for the golden number applied, or not
    "golden_cross": ("apply", "ignore"),
}


def grid_from_rows(rows: list[list[int]]) -> dict:
    return {(r, c): rows[r][i] for r, cs in enumerate(COLS) for i, c in enumerate(cs)}


def rows_from_grid(g: dict) -> list[list[int | None]]:
    return [[g.get((r, c)) for c in cs] for r, cs in enumerate(COLS)]


# ---------------------------------------------------------------- stage 3: rhomboids
def left_rhomboid(l2: list[int], l3: list[int]) -> dict:
    """Image 39-40: line 2 then line 3 into the numbered cells in reading order; an empty cell
    takes the difference of its two nearest upper neighbours (left, right); a lower-half cell
    with one upper neighbour compares cell A with it."""
    vals = list(l2) + list(l3)
    g: dict = {}
    for k, p in enumerate(POS):
        if k < len(vals):
            g[p] = vals[k]
            continue
        r, c = p
        left, right = g.get((r - 1, c - 1)), g.get((r - 1, c + 1))
        if left is not None and right is not None:
            g[p] = diff(left, right)
        else:
            g[p] = diff(g[(0, 4)], g.get((r - 1, c)))
    return g


def right_rhomboid(l4: list[int], left: dict, diametral: str = "mirror") -> dict:
    """Images 40-44: line 4 into the upper half; the first empty upper cell compares the right
    rhomboid's cell A with the left's cell A (right A named first: diff(rA, x)); lower half:
    rA compared with the diametrically opposite cell; the bottom cell from the two above it.
    Only the first upper fill is coded (the 9-word sheets need no more)."""
    g: dict = {}
    upper = [p for p in POS if p[0] <= 3]
    for k, p in enumerate(upper):
        if k < len(l4):
            g[p] = l4[k]
        elif k == len(l4):
            g[p] = diff(g[(0, 4)], left[(0, 4)])
        else:
            raise NotImplementedError("second and later upper fills (angles) not coded")
    ra = g[(0, 4)]
    for p in POS:
        r, c = p
        if r <= 3 or p == (7, 4):
            continue
        opp = (7 - r, c) if diametral == "mirror" else (7 - r, 8 - c)
        g[p] = diff(ra, g[opp])
    g[(7, 4)] = diff(g[(6, 3)], g[(6, 5)])
    return g


# ---------------------------------------------------------------- stage 4: branches and orbit
SIDE = {"left": [(1, 3), (2, 2), (6, 3), (5, 2)], "right": [(1, 5), (2, 6), (6, 5), (5, 6)]}


def branch(rh: dict, side: str, r1: int, crossed: bool) -> list[int]:
    """Images 49-52: R1 compared with the outer-side cells (not the angles): from the top
    downwards, then from the bottom upwards; a crossed root starts from the bottom.
    Written from the canal outwards (A, B, C, D)."""
    cells = SIDE[side]
    order = cells[2:] + cells[:2] if crossed else cells
    return [diff(r1, rh[p]) for p in order]


def semid_sequences(side: str, upper_side: str) -> tuple[list, list]:
    """Upper semidiameter: top cell, three cells down one side, the angle pair, three cells
    up... as in the demonstration figure (image 58) or its mirror (the sheets).
    Lower semidiameter: the six inner cells round the centre, the remaining angle cell, then
    the first two again (letters a-i, 'h' on 'a', 'i' on 'b')."""
    # figure (rule) orientation for the LEFT rhomboid runs down its right side
    fig_upper = [(0, 4), (1, 5), (2, 6), (3, 7), (4, 7), (5, 6), (6, 5), (7, 4), (4, 1)]
    fig_lower = [(2, 4), (3, 3), (4, 3), (5, 4), (4, 5), (3, 5), (3, 1)]

    def mirror(seq):
        return [(r, 8 - c) for r, c in seq]

    # 'interior' = as in the figure: left rhomboid down its right side, right rhomboid mirrored
    up, lo = (fig_upper, fig_lower) if side == "left" else (mirror(fig_upper), mirror(fig_lower))
    if upper_side == "exterior":
        up, lo = mirror(up), mirror(lo)
    lo = lo + lo[:2]
    return up, lo


def reduce_root(v: int, alpha: int) -> int:
    return v % alpha if v > alpha else v


def orbit(left: dict, right: dict, br_l: list[int], br_r: list[int], roots: list[int],
          crossed: list[bool], upper_side: str = "interior") -> dict:
    """Images 54-61. Returns, per semicircle, a 9-ring list of 6 values:
    [upper semidiameter, column A, B, C, D, lower semidiameter]. Ring 1 is the outermost.
    `roots` are the canal values (already reduced); ring k of the right semicircle uses root k,
    of the left semicircle R1, R2, then the roots backwards from the last."""
    n = len(roots)
    out = {}
    for side, rh, br in (("right", right, br_r), ("left", left, br_l)):
        up_seq, lo_seq = semid_sequences(side, upper_side)
        up_cells = up_seq[::-1] if crossed[0] else up_seq
        lo_cells = lo_seq[::-1] if crossed[1] else lo_seq
        order = list(range(n)) if side == "right" else [0, 1] + list(range(n - 1, 1, -1))
        rings = []
        for k in range(n):
            ri = order[k]
            rv, rc = roots[ri], crossed[ri]
            b = br[::-1] if rc else br
            rings.append([diff(roots[0], rh[up_cells[k]])] + [diff(rv, x) for x in b]
                         + [diff(roots[1], rh[lo_cells[k]])])
        out[side] = rings
    return out


# ---------------------------------------------------------------- stage 5: golden number
def golden4(r1: int, r2: int, rpen: int, rlast: int, c1: bool, c2: bool, cpen: bool,
            clast: bool, rule: str = "apply") -> int:
    """Images 65-67: diff(last, first) with the first root on the right; diff(penultimate,
    second) with the second on the right; a crossed root changes side; the golden number is
    diff(second difference, first difference), commuted when both roots of a pair are crossed."""
    def pair(a, ca, b, cb):
        if rule == "apply" and ca != cb:
            return diff(b, a), False
        return diff(a, b), ca and cb
    d1, both1 = pair(rlast, clast, r1, c1)
    d2, both2 = pair(rpen, cpen, r2, c2)
    if rule == "apply" and (both1 or both2):
        return diff(d1, d2)
    return diff(d2, d1)


def golden(roots: list[int], crossed: list[bool], rule: str = "apply") -> int:
    return golden4(roots[0], roots[1], roots[-2], roots[-1], crossed[0], crossed[1],
                   crossed[-2], crossed[-1], rule)


# ---------------------------------------------------------------- stage 6: cipher
def cipher(orb: dict, left_cols: str = "A_first") -> list[list[int]]:
    """Images 69-71: twelve lines round the orbit, each read spirally inwards one ring per
    step, written as the twelve rows of the cipher (nine cells each). Positions clockwise from
    the top of the right semicircle: upper semid, A, B, C, D, lower semid, then the left
    semicircle from the bottom."""
    cols = [1, 2, 3, 4] if left_cols == "A_first" else [4, 3, 2, 1]
    pos = [("right", i) for i in range(6)] + [("left", 5)] + [("left", c) for c in cols]
    pos += [("left", 0)]
    n = len(orb["right"])
    return [[orb[pos[(i + j) % 12][0]][j][pos[(i + j) % 12][1]] for j in range(n)]
            for i in range(12)]


# ---------------------------------------------------------------- stage 7: algebra
def addition(roots: list[int]) -> tuple[int, int]:
    return sum(roots), sum(x * x for x in roots)


def multiply(sub: list[tuple[int, int]], add: tuple[int, int]) -> tuple[int, int, int]:
    """(a1 R + a2 Q) per (b1 R + b2 Q) summed by species, signed: Q, C, QQ."""
    q = c = qq = 0
    b1, b2 = add
    for a1, a2 in sub:
        q += a1 * b1
        c += a1 * b2 + a2 * b1
        qq += a2 * b2
    return q, c, qq
