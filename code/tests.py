"""Pre-registered tests 2-4 (PREREG.md, first document). Seed 20261020.

usage: WORK_DIR=work python code/tests.py   (WORK_DIR holds train.txt and heldout.txt from
       code/build_corpus.py)
Writes results/tests.json.
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import oracle as O  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
CORP = Path(os.environ.get("WORK_DIR", str(HERE / "work")))
SEED = 20261020
N = 10_000
K = 5


def fold(text: str) -> str:
    t = text.upper().replace("J", "I").replace("U", "V").replace("W", "VV")
    return "".join(c for c in t if c in O.ANSWER)


class CharLM:
    def __init__(self, text: str, k: int = K, alpha: float = 0.5):
        self.k, self.a = k, alpha
        self.ctx: Counter = Counter()
        self.full: Counter = Counter()
        for i in range(len(text) - k + 1):
            g = text[i:i + k]
            self.full[g] += 1
            self.ctx[g[:-1]] += 1
        self.V = len(O.ANSWER)

    def score(self, s: str) -> float:
        """Mean log-probability per letter (letters after the first k-1)."""
        tot, n = 0.0, 0
        pad = s
        for i in range(self.k - 1, len(pad)):
            g = pad[i - self.k + 1:i + 1]
            tot += math.log((self.full[g] + self.a) / (self.ctx[g[:-1]] + self.a * self.V))
            n += 1
        return tot / max(n, 1)


def test2() -> dict:
    """Chapter IX worked letter count for the Maximilian query (image 90), as written."""
    steps = [
        {"step": "6290 - 1536 (eye: 1536 or 1538)", "book": 4553,
         "correct": [6290 - 1536, 6290 - 1538]},
        {"step": "4553 / 16: quotient", "book": 252, "correct": 4553 // 16},
        {"step": "4553 / 16: remainder", "book": 16, "correct": 4553 % 16},
        {"step": "252 / 14: quotient", "book": 17, "correct": 252 // 14},
        {"step": "252 / 14: remainder", "book": 0, "correct": 252 % 14},
        {"step": "56 - 16", "book": 40, "correct": 40},
        {"step": "40 + 1 (P)", "book": 41, "correct": 41},
    ]
    for s in steps:
        c = s["correct"]
        s["ok"] = s["book"] in c if isinstance(c, list) else s["book"] == c
    d = json.loads((HERE / "data/examples.json").read_text())
    dresp = next(r for r in d["responses"] if r["id"] == "D")
    return {"steps": steps, "rule_letters_total": 42,
            "printed_answer_letters": len(dresp["numbers"]),
            "match": len(dresp["numbers"]) == 42,
            "golden_number_text": 0, "golden_number_sheet_D": 2}


def test3(rng: random.Random) -> dict:
    lm = CharLM(fold((CORP / "train.txt").read_text(errors="ignore")))
    held = fold((CORP / "heldout.txt").read_text(errors="ignore"))
    d = json.loads((HERE / "data/examples.json").read_text())
    out = {}
    ps = []
    for r in d["responses"]:
        if not r["numbers"]:
            continue
        s = "".join(O.letter(n) for n in r["numbers"])
        assert s == fold(r["text"]), (s, fold(r["text"]))
        obs = lm.score(s)
        sh, mc, pos = [], [], []
        letters = list(s)
        for _ in range(N):
            rng.shuffle(letters)
            sh.append(lm.score("".join(letters)))
            mc.append(lm.score("".join(rng.choice(O.ANSWER) for _ in s)))
            i = rng.randrange(len(held) - len(s))
            pos.append(lm.score(held[i:i + len(s)]))
        p1 = (1 + sum(x >= obs for x in sh)) / (1 + N)
        p2 = (1 + sum(x >= obs for x in mc)) / (1 + N)
        out[r["id"]] = {"letters": len(s), "observed": obs,
                        "shuffle_mean": sum(sh) / N, "shuffle_max": max(sh), "p_shuffle": p1,
                        "machine_mean": sum(mc) / N, "machine_max": max(mc), "p_machine": p2,
                        "latin_windows_mean": sum(pos) / N,
                        "latin_windows_share_below_observed": sum(x < obs for x in pos) / N}
        ps += [(f"{r['id']}_shuffle", p1), (f"{r['id']}_machine", p2)]
    ps.sort(key=lambda x: x[1])
    m = len(ps)
    holm, running = {}, 0.0
    for j, (name, p) in enumerate(ps):
        running = max(running, min(1.0, (m - j) * p))
        holm[name] = {"p": p, "p_holm": running, "reject_0.05": running < 0.05}
    out["holm"] = holm
    return out


def roots_of(words: list[str]) -> tuple[list[int], list[int]]:
    op = O.operation1(words)
    rs = [O.root(w, op.sums[i], op.l1[i], op.l4[i]).value for i, w in enumerate(words)]
    return op.l4, rs


def test4(rng: random.Random) -> dict:
    d = json.loads((HERE / "data/examples.json").read_text())
    out = {}
    for ex in d["examples"]:
        if not ex["id"].endswith("sheet"):
            continue
        words = ex["words"]
        l4, rs = roots_of(words)
        n = ch4 = chr_ = 0
        for wi, w in enumerate(words):
            for ci, c in enumerate(w):
                for a in O.ANSWER:
                    cu = c.upper()
                    if a == cu or (a, cu) in (("I", "J"), ("V", "U")):
                        continue
                    w2 = w[:ci] + a + w[ci + 1:]
                    ws = words[:wi] + [w2] + words[wi + 1:]
                    l4b, rsb = roots_of(ws)
                    n += 1
                    ch4 += l4b != l4
                    chr_ += rsb != rs
        out[ex["id"]] = {"substitutions": n, "share_line4_changed": ch4 / n,
                         "share_roots_changed": chr_ / n}
    held = (CORP / "heldout.txt").read_text(errors="ignore").lower()
    vocab = [w for w in re.findall(r"[a-z]+", held)
             if 2 <= len(w) <= 13]
    vecs, allroots = Counter(), Counter()
    for _ in range(2000):
        q = [rng.choice(vocab) for _ in range(rng.randint(6, 9))]
        _, rs = roots_of(q)
        vecs[tuple(rs)] += 1
        allroots.update(rs)
    out["random_questions"] = {"n": 2000, "distinct_root_vectors": len(vecs),
                               "most_common_root_values": allroots.most_common(10),
                               "distinct_root_values": len(allroots)}
    return out


def main() -> None:
    rng = random.Random(SEED)
    res = {"seed": SEED, "N": N, "test2": test2(), "test3": test3(rng), "test4": test4(rng)}
    (HERE / "results/tests.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1)[:6000])


if __name__ == "__main__":
    main()
