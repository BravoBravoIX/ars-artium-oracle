# Pre-registrations

Three documents, reproduced word for word. Each was written and committed in the author's working repository before the tests it names were scored: the first on 20 October 2026 (tests 2–5), the second later the same day, after the first round (tests 6–11), and the third on 25 October 2026 for version 1.1 (tests 12–16). In the third, `preregistration.md` and `preregistration-stages.md` are the first two documents here, and `WORK_DIR/heldout.txt` is `work/heldout.txt`. Where the originals give paths to private working folders, this copy gives the public repository's equivalents: `work/train.txt` and `work/heldout.txt` for the Latin reference text. Where they say "read by eye", "I checked by hand" or "hand checks", it was Claude that read or checked against the page images.

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

---

# Pre-registration addendum: the machine chained end to end (v1.1, tests 12–16)

Written 25 October 2026, committed before `code/machine_tests.py` is run. Seed 20261025. This adds to `preregistration.md` (tests 2–5) and `preregistration-stages.md` (tests 6–11); nothing in them changes.

## 1. What v1.0 left uncoded or open

1. Stages 3–7 were tested **stage by stage only**: each stage was fed the sheet's own numbers. Nothing ran from the question through to the cipher and the algebra.
2. The **subtraction lines** of the algebra were taken from the sheets, not built from the roots by the rule (signs P/M, places, which pair goes on top).
3. The **multiplication's zero cases** (images 79–81) and the **division** (chapter VIII, second half) were not coded.
4. The **use of the quotients** (chapter IX: starting cell, first letter, number of letters) was coded only as hand arithmetic in test 2.
5. The **answer stage** (chapter X: reading the cipher, the proportion tables) was not coded.

## 2. What was found while reading, before this addendum (descriptive, not tests)

- **Two leaves of LJS 251 are missing.** The page numbers run 81, 82, 83, 84, 87 and 103, 104, 107. Page 84 ends with the catchword *per* in the middle of the division rule ("divide the second [quantity], of the cubes, by …"); page 87 begins with the worked division. Pages 105–106 held the first proportion table: the index on p. 118 lists "Tabula prima proportionalitatis multiplicis", and there is no such table in the book. The tables of compound proportions and of equality (images 104, 106, 108) are ruled and blank. **So the general division (golden number 2 or more) and the turning of numbers into letters cannot be coded from this copy.** Codex 1201 holds part 2 only.
- The rules that **are** complete: the division when the golden number is 0 or 1 (notes 5–7, images 85–87), the starting cell and first letter (images 88–89), the letter count when the golden number is 0 or 1 (image 90) and the read-out of the cipher (images 93–94).
- In reading the text's worked algebra I saw these numbers and checked a few by hand: the residue line of the pope multiplication (image 80) prints 640 and 14080, which are the products of the residue 8 and 176 (image 77) by 80; the golden-1 division example prints 7862 where its own line above has 7682, and its corrector 7863 follows from 7862; the first-letter example (image 89) divides 5840 by 23 and gets quotient 297 and remainder 9, which fit 6840; the general count example (image 90) splits the denominator of 2/13 into 106 and 107; the Maximilian count (image 90) takes 6290 less 1538 as 4553; the Maximilian dividends 56, 1538, 6290 are what a residue of P 1 R, P 5 Q times the addition 56, 1258 would give; both text additions (Maximilian, pope) leave out root 7 of the rule roots; one entry of the superparticular table (11:10, last column, 229) breaks the pattern of its neighbours. The Leedensi multiplication's second partial line (9861335100) was not checked before this addendum. These are listed here so that test 13 is not read as a blind discovery of them.
- Not yet run on any sheet: the chained machine, the subtraction built from roots, the controls.

## 3. The coded rules (`code/machine.py`)

Stages 1–2 are `oracle.py` and stages 3–6 are `stages.py`, both unchanged from v1.0. New:

| Step | Rule as coded | Source |
|---|---|---|
| Chain | question → sums, lines 1–4, roots (with crosses) → canal (roots reduced by the alphabetic number) → rhomboids → branches → orbit → cipher; golden number, subtraction and addition from the **unreduced** roots | ch. II–VII; image 78 ("integras … absque ulla diminutione") |
| Subtraction lines | first difference pair (last, first), first on the right; second pair (penultimate, second), second on the right; a single crossed root changes side; larger root P, smaller M, equal both P, zero P; each quantity as root and signed square; residue = upper minus lower, place by place, by algebra | images 65, 76–78 |
| Addition | all roots except the four of the subtraction, all P: sum of roots, sum of squares | image 78 |
| Multiplication | each residue quantity times each addition quantity, summed by species (Q, C, QQ); both residues zero: addition root × its square → (R, Q, C); addition zero: residue roots summed, squares summed, multiplied → (R, Q, C) | images 79–81 |
| Division, golden 0 | first dividend split by 3 and by 4; remainders added to it (Q corrector); thirds added to the second (C corrector), quarters to the third (QQ corrector); first quotient = second dividend, second quotient = third dividend; first dividend zero (note 6) or third zero (note 7) as written | images 85–87 |
| Division, golden 1 | as golden 0, a unit added to each corrector; quotients = second and third dividends with their parts | image 86 |
| Division, golden ≥ 2 | **not coded** (pages 85–86 missing); the run stops here and says so | — |
| Starting cell | first quotient's remainder on division by the number of cells (12 × words), +1 for P, −1 for M | image 88 |
| First letter | second quotient's remainder on division by 23, ±1 the same way | image 89 |
| Letter count (golden 0/1) | larger quotient less smaller; divide by the first dividend's third part, the quotient by its fourth part; subtract the remainders from the first dividend; +1 for P; this many letters after the first | image 90 |
| Read-out | from the starting cell along its row, then the next rows; row roots from the side columns (left: R1–R6 top down; right: R6, R7, R8, R9, R2, R1 top down); a crossed row root reverses the row | images 69, 93–94 |
| Letters from numbers | **not coded** (first table missing, three tables blank); each (number, row root) pair is given its proportion class instead | images 94–99 |

**Ambiguities, each chosen in advance or enumerated** (`VARIANTS` in `machine.py`; the first value is the text's reading):

| Variant | Readings | Used |
|---|---|---|
| alpha (canal reduction) | 23 / 24 | both readings run |
| upper_side, left_cols, diametral, golden_cross | as in v1.0 | both readings run |
| sub_top: which pair is the upper subtraction line | first-difference pair (text, image 76) / second-difference pair (what sheets B and D show) | both |
| zero_top: zero quantity in the upper line | algebraic / bottom magnitude with P (image 77 third example) | text checks report both |
| addition_set | all middle roots (text) / last middle root left out (both text examples) | text checks report both |
| g1_quotient | part only / part and unit | text reading only (no sheet has golden 1) |
| count_remainders | both remainders / first only | Maximilian chain reports both |
| Not stated, fixed here | a remainder of 0 counts as the last cell (or 23rd letter); the read-out wraps from the last row to the first; correctors are not used (they act only through the missing tables) | — |

Two named readings: **sheets** (alpha 24, upper side exterior, A first, mirror, cross rule applied, second-difference pair on top: the conventions the sheets follow, from v1.0 tests 6–10 and the sheets' layout) and **text** (every first value). The sheets' reading is primary for tests 12–14; the text reading is reported beside it. Only 9-word questions are run (all three sheets have 9 words; later fills of the right rhomboid are not coded).

## 4. Tests

**Test 12. Chained reproduction.** Run the machine from each sheet's printed question (B, C, D) and compare, cell by cell, with every printed stage 2–7 value: B and D, 192 each (roots 9, canal 9, rhomboids 40, branches 8, cipher 108, golden number 1, subtraction 12, addition 2, product 3); C, 126 (roots 6, side-column roots 12, cipher 108). Score = values reproduced. Report per stage and both readings.
*Control:* the same machine (sheets' reading) on 10,000 random 9-word questions (words drawn uniformly from the Gutenberg Latin held-out text, `WORK_DIR/heldout.txt`, words of 2–13 letters; seed 20261025), each scored against each sheet's printed values. A run that fails scores 0. p = (1 + count ≥ observed) / (1 + N), Holm over B, C, D. Threshold 0.05 after Holm. **Minimum achievable p** = 1/10,001 ≈ 1.0 × 10⁻⁴; after Holm over three, ≤ 3.0 × 10⁻⁴, below 0.05.

**Test 13. Departures.** Every stage fed the sheet's own inputs (stage-local, sheets' reading); every printed value that differs from the rule is listed with the rule value as its correction. The same for the text's worked algebra (`data/text_algebra.json`: four subtractions, two additions, four multiplications, two divisions, four uses of quotients), each step fed the book's own preceding numbers. The text's Maximilian count is also run by the rule from its own first numbers (6290, 1538, 56), for both `count_remainders` readings. The count of departures under the text reading is reported, to show which differences are conventions rather than slips.

**Test 14. Do the departures cluster where the answer is decided?** On sheets B and D, the printed stage 2–7 values (384) are split into the *answer path* (the values that feed the division and the letter count directly: roots, golden number, subtraction, addition, product; 54) and the *cipher path* (canal, rhomboids, branches, cipher; 330). If the author had changed numbers to steer the result, departures should fall in the answer path more often than its share. Statistic: the number of test-13 sheet departures in the answer path; p = hypergeometric P(X ≥ observed). Threshold 0.05 (one test). **Minimum achievable p** = C(54, k) / C(384, k) for k departures: 0.0195 at k = 2 and smaller for larger k, so the test can reach 0.05 when there are 2 or more departures; with 0 or 1 it is reported as uninformative. The script records the minimum for the observed k. Systematic conventions (canal by 24, upper side, pair on top) are not counted, since the sheets' reading absorbs them.

**Test 15. Do the printed answers follow from their questions by the book's rules?** Run the chain for questions B and D (both readings), and again with the sheet's own printed roots. Record the golden number, whether the division can be done by the written rules, and when it can, the starting cell, the first letter and the number of letters, against the printed answers (B: 67 letters, first letter G = 7; D: 35 letters, first letter D = 4). *Control (descriptive):* over the 10,000 random questions, the share with golden number 0 or 1 (the only ones the written rules carry to a letter count), and the distribution of the letter count and first letter among them.

**Test 16. What the answer stage would need (descriptive).** For each of the 108 cells of the cipher (sheets B and D, as printed and as the machine builds them, and over all random questions), the proportion class of the cell's number to its row root: multiple, superparticular, superpartient, multiple superparticular, multiple superpartient, equality, zero. Report the share that needs the missing multiple table (multiple and the two compound classes, since the text builds compounds from the multiple table).

**Exploratory (labelled as such):** E1, internal pattern of the two surviving tables (pattern read off their first rows: superparticular second = 2 × first + 1, third = first + second, fourth = 2 × third + 3, fifth = third + fourth, sixth = 2 × fifth + 9; superpartient third = first + second, fourth = third + first, fifth = third + fourth, sixth = fifth + third). E2, the internal arithmetic of the one worked general division (image 82).

**Stop rule.** One run. Departures are listed and corrected; nothing is retuned after the run. If a result depends on a reading not listed here, it is reported as exploratory.
