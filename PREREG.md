# Pre-registrations

Two documents, reproduced word for word. Each was written and committed in the author's working repository before the tests it names were scored: the first on 20 October 2026 (tests 2–5), the second later the same day, after the first round (tests 6–11). Where the originals give paths to private working folders, this copy gives the public repository's equivalents: `work/train.txt` and `work/heldout.txt` for the Latin reference text. Where they say "read by eye", "I checked by hand" or "hand checks", it was Claude that read or checked against the page images.

The second document reports one check that was wrong. It said that sheet D's golden number ignores the rule for crossed roots. That was a slip of arithmetic: 12 against 11 gives 1, not 0. The scored test 10 shows that the rule as written gives sheet D's golden number.

---

# Pre-registration: Ars artium oracle, tests 2–5

Written 20 October 2026, committed before tests 2–5 were scored. Seeds fixed below.

## What was already looked at (so not confirmatory)

- **Test 1 (reproduction of the worked numbers, operations 1–2)** was run once while the code was being written (`code/reproduce.py`, `results/reproduction.json`): sums 48/48, line 1 39/39, line 2 39/39, line 3 34/34, line 4 42/42, last number of line 4 5/6, roots 20/26. It is reported as descriptive. The six root misses were checked against single-zero copying slips (none explained). No variant will be added to make a miss fit; any later variant is labelled exploratory.
- The two printed answers (sheet B, image 271; sheet D, image 279) were read by eye: their numbers spell Latin through the 23-letter alphabet A=1 … X=21, Y=22, Z=23.
- The text's own worked letter count for the Maximilian query (image 90) was read by eye.

## Test 2: the stated letter-count rule against the printed answer (deterministic)

Chapter IX (images 89–90) gives a rule for the number of letters in the answer and works it for the Maximilian query: 41 letters "beyond the first", so 42. We compare with the length of the printed answer to that query (sheet D, image 279). We also re-do each arithmetic step the text states (subtraction, two divisions, final subtraction) and report which are correct. No statistics.

## Test 3: are the answers computed or composed? (Latin-likeness against controls)

The last step of the machine, as written, takes a number and keeps its residue mod 23 as a letter. Whatever the arithmetic before it, nothing in the rules makes the residues spell Latin.

- Statistic: mean log-probability per letter under a Latin character 5-gram model (add-0.5 smoothing; spaces removed), trained on `work/train.txt`, letters folded to the book's 23-letter answer alphabet (J→I, U→V, W→VV).
- Observed: the printed answers B (67 letters) and D (35 letters).
- Controls, each N = 10,000, seed 20261020:
  - C1 shuffle: the same letters in random order (keeps letter frequencies, destroys sequence).
  - C2 machine-like output: residues drawn uniformly from 1–23 (the stated last step), same length.
  - Positive control (not tested, reported): random windows of the same length from `work/heldout.txt`.
- p = (1 + number of controls scoring ≥ observed) / (1 + N), one-sided.
- Four p-values (B and D × C1, C2), Holm correction at α = 0.05.
- Reading: if the answers beat both controls, the printed answers are ordinary Latin, which the stated final step does not produce except by chance at about the C2 p-value; the evidence would weigh toward answers composed first and numbers fitted afterwards (or a rule not written in the book).

## Test 4: does the front of the machine depend on the question? (sensitivity)

For each of the four worked queries A–D: every single-letter substitution (each letter position × the 22 other letters of the 23-letter alphabet, using the chapter II values). Measure the share of substitutions that change (a) at least one number of line 4, (b) at least one root. Also 2,000 random questions of 6–9 words drawn from the word list of `work/heldout.txt` (seed 20261020): the number of distinct root vectors and the distribution of roots.

Prediction written now: if the machine computes, at least half of single-letter changes alter a root, and nearly all random questions give distinct root vectors. If the front end often gave the same roots whatever the question, an answer could be "planted" upstream; this test checks that.

## Test 5: dates (historical, no statistics)

Compare what each printed answer says with the dates the book claims (dedications dated 1564 and 1569) and with the events: Pius IV died 9 Dec 1565, Michele Ghislieri elected 7 Jan 1566 as Pius V; Maximilian II emperor from 25 Jul 1564, died 12 Oct 1576.

## Stop rule

One run of tests 2–5 as written. Operations 3–7 (rhomboids, orbit, golden number, cipher, algebra) are not implemented in this round; they are listed as the next step. No new variants after scoring except as labelled exploratory.

---

# Pre-registration: stages 3–7 against the example sheets (tests 6–11)

Written 20 October 2026 (second round), committed before tests 6–11 were scored. Seed 20261020.

## What was already seen (not confirmatory)

While reading chapters IV–VI I checked by hand, on sheets B and D: the left and right rhomboids (fill rules), the two branches, the first column of the upper semidiameter, and the golden numbers. The reading also showed three things the code now has as declared variants: the sheets reduce canal roots by 24 (the text's "alphabetic number" is 23 in chapter IX); the sheets' upper semidiameter runs down the branch side of each rhomboid, while the text and the figure on image 58 use the other side; and sheet D's golden number ignores the rule for crossed roots. These hand checks are reported as descriptive. Not yet seen: the cipher comparison (test 9), the algebra checks (test 11), and anything of sheet C.

## Design: stage-local tests

Each stage is fed **the sheet's own inputs** (the numbers the sheet shows for the stage before it), so a slip upstream does not count against later stages. The score is the share of the sheet's numbers that the rule reproduces, cell by cell.

| Test | Stage | Inputs (from the sheet) | Compared with | Sheets |
|---|---|---|---|---|
| 6 | 3: rhomboids | lines 2, 3, 4 | the 40 rhomboid cells | B, D |
| 7 | 4: branches | rhomboids, root 1 and its cross | the 8 branch numbers | B, D |
| 8 | 4: canal | the roots table | the 9 canal roots (alpha 23 and 24) | B, D |
| 9 | 4–6: orbit to cipher | rhomboids, branches, canal roots and crosses | the 108 cells of the cipher | B, D |
| 10 | 5: golden number | the four roots and their crosses | the golden number | B, D and the 4 worked examples in the text (images 66–67) |
| 11 | 7: algebra | the sheet's subtraction lines and addition roots | the sheet's sums, squares and products | B, D; text addition (image 78) |

**Variants for test 9.** These are run as a full grid and every cell is reported: `upper_side` (interior / exterior) × `left_cols` (A_first / D_first). The variant named as the text's reading is interior + A_first. The primary score is the text reading; the best variant is reported as exploratory.

**Controls for test 9.** (a) Shuffle: the rule's cipher compared with 10,000 random permutations of the sheet's 108 cells, so that values are kept and placement is destroyed. (b) Wrong inputs: the rule's cipher built from the other sheet's inputs (B inputs against D's cipher and the reverse). p = (1 + count ≥ observed) / (1 + N). Holm correction over the four p-values (B, D × text reading, best variant). Test 9 also reports the match of the multiset of values.

**Tests 6, 7, 8, 10 and 11** are exact checks with no p-values. The chance of an exact match by luck is small but not computed.

**Stop rule.** One run. The division (chapter VIII, second half) and the answer stage (chapters IX–X) are not coded in this round: the rule text's worked division (image 82) has unreadable cells, and the sheets leave the division lines blank. This is reported as the point where the mechanism can no longer be followed.
