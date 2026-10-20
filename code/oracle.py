"""The Ars artium machine, operations 1-2 and the answer-length / first-letter rules of
operation 8, implemented exactly as the rule text of Penn LJS 251 states them (part 1,
chapters II, III and IX; transcription in data/transcription, image numbers in data/*.json).

Every place where the text is silent or could be read two ways is a named variant
(VARIANTS); the default is the plainest reading. Nothing here is tuned to the worked examples.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Hebrew-Latin alphabet of chapter II (image 16): I and J share 9, U and V share 200.
ALPHA = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 9,
         "K": 10, "L": 20, "M": 30, "N": 40, "O": 50, "P": 60, "Q": 70, "R": 80, "S": 90,
         "T": 100, "U": 200, "V": 200, "X": 300, "Y": 400, "Z": 500}
# Answer alphabet of 23 letters (chapter IX: "Numerum Alphabeticum, 23"); order as in the
# book's Responsio lines (images 271, 279): G=7 ... V=20, X=21.
ANSWER = "ABCDEFGHIKLMNOPQRSTVXYZ"

VARIANTS = {
    # chapter II says nothing on five or more digits: pair them (1,2)(3,4)(5) or overlap
    "five_digit": ("pairs", "overlap"),
    # chapter III, 'if not even one line can be made ... the sum itself is left'
    "no_line": ("sum", "first_line"),
    # chapter III fourth note: divisor 0 or 1 -> divide the last line by the word sum
    "zero_divisor": ("as_written",),
}


def diff(a: int, b: int) -> int:
    """Chapter II: greater minus lesser as is; lesser compared with greater loses a unit."""
    return a - b if a >= b else b - a - 1


def word_sum(word: str) -> int:
    return sum(ALPHA[c] for c in word.upper() if c in ALPHA)


def letter_values(word: str) -> list[int]:
    return [ALPHA[c] for c in word.upper() if c in ALPHA]


def line1(s: int, five_digit: str = "pairs") -> list[int]:
    d = [int(c) for c in str(s)]
    if len(d) == 1:
        return [d[0]]
    if len(d) == 2:
        return [diff(d[0], d[1])]
    if len(d) == 3:
        return [diff(d[0], d[1]), diff(d[1], d[2])]
    if len(d) == 4 or five_digit == "pairs":
        out = [diff(d[i], d[i + 1]) for i in range(0, len(d) - 1, 2)]
        if len(d) % 2:
            out.append(d[-1])
        return out
    return [diff(d[i], d[i + 1]) for i in range(len(d) - 1)]


@dataclass
class Op1:
    sums: list[int]
    l1: list[list[int]]
    l2: list[int]
    l3: list[int]
    l4: list[int]          # one per word (last one from the odd/even rule)
    pairs: list[tuple[int, int]] = field(default_factory=list)


def operation1(words: list[str], five_digit: str = "pairs") -> Op1:
    sums = [word_sum(w) for w in words]
    l1 = [line1(s, five_digit) for s in sums]
    l2 = [sum(x) for x in l1]
    n = len(l2)
    l3 = [diff(l2[i], l2[i + 1]) for i in range(n - 1)]
    pairs = [(diff(l2[i], l3[i]), diff(l3[i], l2[i + 1])) for i in range(n - 1)]
    l4 = [diff(a, b) for a, b in pairs]
    if n >= 3:
        if n % 2:                       # odd number of words: two middle numbers of line 4
            m = len(l4) // 2
            last = diff(l4[m - 1], l4[m])
        else:                           # even: first~middle, middle~last, then compare
            m = len(l4) // 2
            last = diff(diff(l4[0], l4[m]), diff(l4[m], l4[-1]))
        l4 = l4 + [last]
    elif n == 2:
        l4 = l4 + [l4[0]]               # not covered by the text; declared, never used
    return Op1(sums, l1, l2, l3, l4, pairs)


def pyramid(word: str) -> list[str]:
    """Chapter III: the letter values of the word written flat as one digit string; each new
    line takes three units from every digit but the last (0 when the digit is under 3), set
    between it and the next; at most two new lines, and no line that would be all zeros."""
    top = "".join(str(v) for v in letter_values(word))
    lines = [top]
    for _ in range(2):
        prev = lines[-1]
        if len(prev) < 2:
            break
        new = "".join(str(int(c) - 3) if int(c) >= 3 else "0" for c in prev[:-1])
        if set(new) == {"0"}:
            break
        lines.append(new)
    return lines


@dataclass
class Root:
    value: int
    reversed: bool        # the book's cross mark
    case: str             # which rule of chapter III fired


def root(word: str, s: int, l1: list[int], m: int, no_line: str = "sum") -> Root:
    """Chapter III: (Q - S*m) mod D, with the nine exceptions as written."""
    lines = pyramid(word)
    if len(lines) == 1:
        q = s if no_line == "sum" else int(lines[0])
    else:
        q = int(lines[-1])
    mult = s * (m if m not in (0,) else 1)           # note 1: a zero multiplier leaves S
    dstr = "".join(str(x) for x in l1)
    lead_zero = dstr.startswith("0") and len(dstr) > 1
    d = int(dstr[::-1]) if lead_zero else int(dstr)  # note 3: '02' is taken as 20
    if d in (0, 1):                                  # note 4 (and 7/8 sub-cases)
        if q == mult:                                # note 7, first sub-case
            if m in (0, 1):
                return Root(0, False, "n7a_zero")
            r = q - s
            return Root(r, True, "n7a_sum")
        if mult > q:                                 # note 8
            r = mult - q
            if s > r:
                return Root(s, True, "n8_sum")
            return Root(r % s, True, "n8")
        return Root(q % s, True, "n4")
    if mult > q:                                     # note 6: reversed subtraction
        return Root(mult - q, True, "n6")
    rem = q - mult
    if rem == 0:                                     # note 7
        return Root(d, lead_zero, "n7")
    if d > rem:                                      # note 9
        return Root(d - rem, True, "n9")
    r = rem % d
    if r == 0:                                       # note 5: divides exactly
        return Root(d, lead_zero, "n5")
    return Root(r, lead_zero, "plain")


def letter(n: int) -> str:
    return ANSWER[(n - 1) % 23]
