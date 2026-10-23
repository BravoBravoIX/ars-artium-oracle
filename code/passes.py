"""Two-pass check: agreement of the numbers read by pass A (Opus) and pass B (Sonnet) on each
page both read, and whether each image-checked worked number (data/examples.json) is found in
each pass of its page. Writes results/passes.json.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
T = HERE / "data/transcription"
PAGES = {"A_text": 23, "A_sheet": 269, "B_text": 24, "B_sheet": 266, "C_sheet": 272, "D_sheet": 276}


def nums(p: Path) -> Counter:
    if not p.exists():
        return Counter()
    return Counter(re.findall(r"\d+", p.read_text()))


def main() -> None:
    out = {"pages": {}, "examples": {}}
    for f in sorted((T / "B").glob("*.txt")):
        a, b = nums(T / "A" / f.name), nums(f)
        if not a and not b:
            continue
        inter = sum((a & b).values())
        union = sum((a | b).values())
        out["pages"][f.stem] = {"numbers_A": sum(a.values()), "numbers_B": sum(b.values()),
                                "agreement": round(inter / union, 3) if union else None}
    ex = json.loads((HERE / "data/examples.json").read_text())["examples"]
    for e in ex:
        page = PAGES[e["id"]]
        a, b = nums(T / "A" / f"{page:04d}.txt"), nums(T / "B" / f"{page:04d}.txt")
        vals = [str(x) for x in e.get("sums", [])] + [str(x) for x in e.get("l2", [])]
        vals += [str(v[0]) for v in e.get("roots", {}).values()]
        out["examples"][e["id"]] = {
            "page": page, "checked": len(vals),
            "found_A": sum(v in a for v in vals) if a else None,
            "found_B": sum(v in b for v in vals) if b else None}
    ag = [v["agreement"] for v in out["pages"].values() if v["agreement"] is not None]
    out["median_agreement"] = sorted(ag)[len(ag) // 2] if ag else None
    (HERE / "results/passes.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out["examples"], indent=1), out["median_agreement"])


if __name__ == "__main__":
    main()
