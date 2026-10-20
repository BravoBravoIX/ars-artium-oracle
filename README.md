# The *Ars artium* oracle: does the machine compute its answers?

*Ars artium sive ars magna cabalistica* ("the art of arts, or the great cabalistic art") is a Latin treatise that teaches a question-answering machine. The work claims to be by the German poet Hartmann Schopper and dates itself 1564 and 1569. The surviving copies are 17th or 18th century, and the work was probably composed then. You write a question in Latin and turn each letter into a number. The numbers then pass through nine stages: difference lines, "pyramids" and "roots", two rhomboid grids, a ring-shaped "orbit", a "golden number", a number grid called the *cipher*, a home-made algebra, and finally tables of proportions. The last stage keeps a number's remainder after dividing by 23 as a letter, and the letters are meant to spell the answer.

The book gives worked example sheets. Two of them carry answers, and both answers are Latin verse. This study asks two questions:

1. Do the book's written rules, applied mechanically, reproduce its own worked numbers?
2. Are the answers computed by the procedure, or written first?

**What is new, in one sentence.** No study of how this machine works has been published. We rebuilt the first seven stages from the rule text, and they reproduce the book's own sheets almost cell for cell, down to a 108-cell grid. But the two printed answers are fluent Latin verse that names events the book's own date could not know, and the steps that would turn the arithmetic into those letters are left blank in both surviving Penn copies. So the evidence weighs strongly toward the arithmetic being real and the answers being written first.

This is a study of how a device works. Nothing here is a decipherment, and nothing here suggests that the device predicts anything.

October 2026. CPU only; Python standard library. The whole analysis reruns in under a minute.

**The paper:** [`paper/ars-artium-oracle.pdf`](paper/ars-artium-oracle.pdf) is a working paper, built from `paper/ars-artium-oracle.typ` by `paper/build.sh`. This README covers the same ground in more detail.

## In short

| Question | Answer | How firm |
|---|---|---|
| Do the rules reproduce the worked numbers of stages 1–2? | Yes, almost all | Word sums 48/48, difference lines 154/154, last number of line 4 5/6, roots 20/26 (four example queries, text and sheets) |
| …of stages 3–5? | Yes | Rhomboids 80/80 cells, branches 16/16, golden number 6/6 (two sheets and four worked examples in the text), canal roots 18/18 when reduced by 24 (14/18 by the text's 23) |
| …of the 108-cell cipher grid? | Mostly, once one ambiguity is read the way the sheets read it | Sheet B: 83/108 cells by the text's reading, 103/108 by the sheets' reading. Sheet D: 60 and 70/108; two systematic slips on sheet D (exploratory) bring it to 107/108. Against shuffled sheets, p = 0.0001 each (Holm 0.0004). The wrong sheet's inputs match only 6–8 cells |
| …of the algebra? | Yes | Subtraction, addition and multiplication on both sheets are exact; the text's Maximilian addition also |
| Does the machine depend on the question? | Strongly | One changed letter alters a root in 98–99 % of cases; 2,000 random questions give 2,000 different sets of roots |
| Are the printed answers ordinary Latin? | Yes | Both beat every one of 10,000 shuffles of their own letters and 10,000 random strings of the kind the last stage produces (p = 0.0001 each, Holm 0.0004) |
| Do the answers follow from the arithmetic? | Not that we can see | The final division, which fixes the start cell, first letter and length of the answer, is blank on both answer sheets in both copies. The one worked letter count in the text (Maximilian) has three wrong sums in seven steps and gives 42 letters; the printed answer has 35 |
| What do the answers say? | Things known only after the book's own date | Pius IV's successor: *Ghislerium cernes…*, naming Michele Ghislieri (Pius V, elected January 1566). Maximilian II: *Dena trino…*, "ten and three"; he died in the 13th year of his reign (1576) |

## 1. The book and the machine

The work survives in six known manuscripts and was never printed, although its title pages imitate a print ("Francofurti apud Moenum MDLXIV" and "MDLXIX"). Its two dedications cannot be right as dated: one to Moritz of Hessen-Kassel, who became Landgrave in 1592, and one from Johann Theodor de Bry, who was eight years old in 1569 (Les Enluminures, TM 623).

**Part 1** (in LJS 251, images 2–112) gives the practical rules in ten chapters, each with worked examples:

1. the question;
2. letter values and four "difference lines";
3. "pyramids" and "roots";
4. the two rhomboids;
5. the branches and the orbit;
6. the golden number;
7. the cipher;
8. the algebra;
9. the two quotients and the letter count;
10. the answer.

**Part 2** gives the "reasons" and ends with example sheets, labelled A to D, that work four questions through the stages:

- **A:** "Will Antonius Pacutus the Venetian trade?"
- **B:** "Tell the surname of the pope to be elected after the death of Pius IV of Florence."
- **C:** "Will crops abound at *Leedensi* in 1540?"
- **D:** "In which year of his reign will Emperor Maximilian II die?"

Sheets B and D end with an answer, given as a string of numbers and its reading:

- **B:** 7.8.9.18.11.5.17.9.20.12 … = *Ghislerium cernes Petri gratissima proles / Ex Alexandrinis currere nemoribus*.
- **D:** 4.5.13.1.19 … = *Dena trino pollens mortem concedet heroi*.

The numbers map onto the letters through the 23-letter alphabet A = 1 … X = 21, Y = 22, Z = 23. Sheet C has no answer in either copy; sheet A has none in LJS 251.

The core operation throughout is the book's "difference" of two numbers *a* and *b*: *a − b* when *a ≥ b*, but *b − a − 1* when the lesser comes first. The code implements it as `diff` in `code/oracle.py`.

## 2. Sources

- **Penn, Kislak Center, LJS 251** (Germany, 1655–1699, 139 ff.): the main witness, both parts. Images from the Internet Archive item `ljs251`, uploaded by Penn Libraries under the Public Domain Mark; Penn's own rights statement is No Copyright – United States.
- **Penn, Ms. Codex 1201** (part 2 only, 50 ff.): a second witness for the example sheets, fetched through Penn's Colenda IIIF service. Its sheets carry the same two answers, the same blank division lines, and no answer on sheet C.
- **Penn, Ms. Codex 1636** (ex Les Enluminures TM 623): could not be obtained for this study, so it is not used.
- **Amsterdam, Embassy of the Free Mind, BPH PH337**: Source Library (sourcelibrary.org) has an AI transcription and English translation of it, licensed CC BY-SA 4.0 and marked as not reviewed by a scholar. It was used **only as a finding aid** to locate chapters. Nothing from it is in this repository.
- **Leipzig, UB, Cod. mag. 28**, *Kabala mosaica* (Public Domain Mark): a related number "cabala" looked at briefly. Its operations (*chorda*, *detractio*, *numeri restricti*) are different, and it is left for another study.
- **Not online:** Wellcome Library MS.4464 (a mid-18th-century transcript of 139 ff.; the catalogue calls it "a copy of an extremely rare printed book on fortune-telling by letters and numbers") and Florence, BNCF II.III.323.

**Transcription.** Claude (Anthropic's API) read 113 pages of LJS 251 (pass A, Claude Opus 5.5) and 33 rule and example pages a second time (pass B, Claude Sonnet 5.5), at a cost of 7.82 US dollars. Every number used in a test was checked by eye against the page image, and the model declined seven diagram pages, which were read by eye where needed. Details and prompts are in `data/transcription/README.md`. The worked numbers used in the tests are in `data/examples.json` (stages 1–2 and the answers) and `data/sheets.json` (stages 3–7), with image numbers.

## 3. Method

The rules are coded as written (`code/oracle.py` for stages 1–2 and the answer alphabet, `code/stages.py` for stages 3–7). Where the text can be read two ways, the choice is a named variant, and both readings are run. Each later stage is tested **stage-locally**: it is fed the numbers the sheet itself shows for the stage before. A slip early on a sheet therefore does not count against every later stage.

All tests were written down and committed before they were scored (`PREREG.md`), with seed 20261020, Holm's correction and one run each. Test 1 (stages 1–2) was run while the code was written, so it is reported as descriptive.

| Test | What | Controls |
|---|---|---|
| 1 | Stages 1–2 against every worked number of four queries | none (exact) |
| 2 | Text's worked letter count against the printed answer | none (exact) |
| 3 | Latin-likeness of the answers: mean log-probability per letter under a Latin 5-gram letter model (nine classical and humanist texts from Project Gutenberg) | 10,000 shuffles; 10,000 uniform residue strings; Latin windows as a positive reference |
| 4 | Sensitivity: every single-letter change of the four questions; 2,000 random Latin questions | — |
| 5 | Dates of the events the answers name | — |
| 6–8, 10, 11 | Rhomboids, branches, canal roots, golden number, algebra against sheets B and D (and the text's worked examples) | none (exact) |
| 9 | The 108-cell cipher grid rebuilt from the sheet's rhomboids, branches and roots | 10,000 permutations of the sheet's cells; the other sheet's inputs |

## 4. Results

**Stages 1–2** (`results/reproduction.json`). Every word sum (48/48) and every number of the four difference lines (154/154) agrees. Five of six "last numbers" agree: for Antonius, the rule chapter gives 0 and sheet A gives 2. Twenty of 26 roots agree. None of the six misses is a single zero dropped or added in a pyramid line. In one of them (Pij), the rule chapter works the very same case and gets 6, while sheet B has 68. For query D, the text's own later worked steps (the addition on image 78) use the roots the rules give (16 and 31), but sheet D shows 3 and 10. The book carries two different computations of the same question.

**Stages 3–5** (`results/stage_tests.json`). Both rhomboids of both sheets agree cell for cell (80/80), with "diametrically opposite" read as a mirror across the middle; read as through the centre, only 13–14 of 20 agree. Both branches agree (16/16). The golden number agrees in all six cases (two sheets, four text examples) with the rule for crossed roots applied; without it, in 1 of 6. The roots written in the canal are reduced by 24 on both sheets (18/18), not by the 23 the text calls the "alphabetic number" (14/18).

**Stage 6: the cipher.**
- **The 108 cells.** Rebuilt from the sheet's own inputs, sheet B's cipher agrees in 83 of 108 cells under the text's reading and in 103 under the reading the sheets use. In the text's reading, the "upper semidiameter" runs down the inner side of each rhomboid, avoiding the cells already used for the branches; the sheets run it down the branch side. Sheet D agrees in 60 and 70 cells.
- **Two systematic slips on sheet D.** These were found after scoring, so they are exploratory (`results/explore_d.json`). Sheet D's lower semidiameters use root 1 where the text says root 2, and its right half takes the roots one place late from ring 4 onwards, as if root 4 had been skipped. With both slips, sheet D agrees in 107 of 108 cells.
- **Controls.** Against 10,000 random rearrangements of the sheet's own cells, no rearrangement matched as well (p = 0.0001 for each sheet and reading, Holm 0.0004). The other sheet's inputs match only 6–8 cells.

**Stage 7: the algebra.** Subtraction, addition and multiplication are exact on both sheets, and the text's worked Maximilian addition (16 + 4 + 5 + 31 = 56; squares 1,258) is exact too.

**Where the mechanism breaks.**
- **The division is not worked.** Next comes the division by the golden number and its square (chapter VIII), which yields the two quotients that fix the start cell, the first letter and the length of the answer (chapter IX). Both answer sheets, in both copies, rule the lines for this division and leave them empty. The rule text's own worked division (image 82) cannot be followed from what is written, so we could not code it.
- **The letter count does not fit the answer.** The one place where the text works the letter count for a printed answer is Maximilian (image 90). It uses a golden number of 0 where sheet D has 2. Its quantities (6290, 56) are not sheet D's (183, 6538, 41775). Three of its seven sums are wrong (6290 − 1536 [or 1538] = 4553; 4553 ÷ 16 = 252 remainder 16; 252 ÷ 14 = 17). It ends at 42 letters; the printed answer has 35.

**Are the answers computed?** (`results/tests.json`)
- **Language.** The answer letters score −2.06 (B, 67 letters) and −2.29 (D, 35 letters) per letter under the Latin model. Shuffles of the same letters average −3.35 (best −2.94 and −2.80). Strings of the kind the last stage produces average −3.24 (best −3.00 and −2.95). Real Latin windows of the same length average −1.92. Both answers are Latin, beyond every control.
- **Sensitivity.** One changed letter in a question alters a root in 97.8–99.0 % of cases. 2,000 random questions give 2,000 different root sets.
- **Hindsight.** Answer B names Ghislieri, born near Alessandria, who was elected on 7 January 1566. Answer D gives "ten and three" for Maximilian II, emperor from July 1564, who died on 12 October 1576 in the 13th year of his reign. The work dates itself 1564/1569.

## 5. Verdict

The procedure is real, and the copyists followed it with care for seven stages, down to a 108-cell grid that the rules rebuild almost exactly. Nothing in that arithmetic fixes the answer in advance: the numbers change with every letter of the question. But the printed answers are Latin verse naming events after the book's own date. They cannot be expected from a last stage that turns remainders into letters. The division that would have to produce them is left blank in both copies, and the one worked letter count disagrees with its answer.

The evidence weighs strongly toward answers that were written first, with the calculation carried out as far as it could be shown. It would take an unwritten rule, or a great deal of freedom in the unwritten steps, to make the numbers spell the verses.

## 6. Earlier work, and what is new

- **Les Enluminures**, description of TM 623 (now Penn Ms. Codex 1636): content, the six copies and the dating problems; no mechanism. Its argument that the work is 17th-century and probably Italian is followed here.
- **Penn Libraries**: catalogue records for LJS 251 and Codex 1201. The LJS 251 record says the mathematical notation "suggests that the text was copied and updated between 1655 and 1699". There is also a video orientation.
- **Wellcome Collection**: catalogue record of MS.4464 (mid-18th-century transcript; treats the work as a copy of a printed book). The manuscript itself was not seen.
- **Richard Hoche, "Schopper, Hartmann"**, *Allgemeine Deutsche Biographie* 32 (1891), 372–373: a poet and translator (Latin *Reineke Fuchs*, *Panoplia*), born about 1542 at Neumarkt in der Oberpfalz, last attested 1595. It mentions no cabalistic or divinatory work.
- **Source Library** (sourcelibrary.org): AI transcription and translation of BPH PH337 (CC BY-SA 4.0), unreviewed. It is a translation, not an analysis.
- **GitHub and Zenodo**: searched 20 October 2026 for seven phrases ("ars artium cabalistica", "ars magna cabalistica", "Schopper cabala", "kabala mosaica", "cabalistic oracle", "cabala oracle", "cabala numerica"). No results.
- **Not read** (no lawful copy reachable):
  - Christine Mundhenk, "Schopper, Hartmann", *Killy Literaturlexikon* 10 (2011), 565–566.
  - Moorat's catalogue entry for Wellcome MS.4464.
  - The Florence catalogue entry for BNCF II.III.323.
  - The literature on numerical "cabala" and lottery oracles: Stephen M. Stigler, *Casanova's Lottery* (2003); Paolo Macry, *Giocare la vita. Storia del lotto a Napoli tra Sette e Ottocento* (1997); the tradition of Rutilio Benincasa's *Almanacco perpetuo*.

  The study places *Ars artium* in that genre only loosely. Someone who knows it may find that the mechanism, or the practice of composing answers first, is already described for related books.

## 7. Caveats

- **Three of six copies.** Only two Penn copies were read; the third Penn copy, the Wellcome and Florence copies and the 2011 sale copy were not.
- **Machine transcription.** The transcription is by a language model. The numbers used in tests were checked by eye, but by the AI coding assistant, not by a palaeographer.
- **Partial coverage.** Stages 3–7 are coded for 7–10-word questions only (all three surviving sheets have 9 words). Some fill rules for larger rhomboids and for the angles are not coded.
- **Exploratory findings.** The sheet-D slips (lower semidiameters, skipped root) are exploratory and were found after scoring.
- **The cipher variant.** The "sheets' reading" of the upper semidiameter was seen on the sheets before test 9 was scored; the pre-registration says so, and the text's reading is the primary score.
- **What the answer test does not show.** The Latin-likeness test shows that the answers are Latin. It cannot show who wrote them or when. The hindsight argument rests on dates.
- **The division.** The division and the answer stage (chapters VIII–X) are not implemented, so "where it breaks" means where the book stops showing its work, not a proof that no rule could exist.

## 8. How to reproduce

```
scripts/fetch_sources.sh SOURCE_DIR          # nine Latin texts from Project Gutenberg (and, with
                                             # WITH_IMAGES=1, the LJS 251 page images, 508 MB)
code/run_all.sh SOURCE_DIR                   # under a minute; writes results/*.json
```

The code uses the Python standard library only; `run_all.sh` asks `uv` for Python 3.13. A clean rerun from the fetched sources reproduces every file in `results/` byte for byte (checked 20 October 2026). `results/run_records.json` lists the SHA-256 of every input, code file and result.

## Licensing

- **Code** (`code/`, `scripts/`, `paper/build.sh`): MIT, see `LICENSE`.
- **Our data, results and paper** (`data/`, `results/`, `paper/`, `PREREG.md`, this README): CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). `data/transcription/` is our machine transcription of a public-domain manuscript; `data/examples.json` and `data/sheets.json` are our readings of it.
- **Manuscripts:** LJS 251 and Ms. Codex 1201 are in the public domain (Penn: No Copyright – United States; Internet Archive: Public Domain Mark). No page images are included; the LJS 251 images can be fetched (above).
- **Left out:**
  - Source Library's transcription and translation (CC BY-SA 4.0), which was used only to find chapters.
  - The Project Gutenberg texts, which are fetched and not redistributed.
  - The API reading script, which called the author's private client and is not needed to rerun the analysis. Its prompts are in `data/transcription/README.md`.

## References

- Philadelphia, University of Pennsylvania, Kislak Center, LJS 251, *Ars artium sive ars magna cabalistica*. Internet Archive https://archive.org/details/ljs251 ; Colenda https://colenda.library.upenn.edu/catalog/81431-p3dj58h43
- Philadelphia, University of Pennsylvania, Ms. Codex 1201. Colenda https://colenda.library.upenn.edu/catalog/81431-p36242
- Philadelphia, University of Pennsylvania, Ms. Codex 1636 (formerly Les Enluminures TM 623).
- London, Wellcome Collection, MS.4464, catalogue record https://wellcomecollection.org/works/gjew7h5p
- Les Enluminures, "Hartmann Schopper (?), Ars artium sive ars magna cabalistica", description TM 623, https://www.textmanuscripts.com/medieval/schopper-ars-artium-cabalistica-60878
- Richard Hoche, "Schopper, Hartmann", *Allgemeine Deutsche Biographie* 32 (1891), 372–373, https://www.deutsche-biographie.de/sfz79053.html
- Christine Mundhenk, "Schopper, Hartmann", in W. Kühlmann et al. (eds), *Killy Literaturlexikon* 10, Berlin and New York 2011, 565–566 (not read).
- Source Library, *Great Kabbalistic Art: Hartmann Schopper, 1564–1569* (BPH PH337), AI transcription and translation, CC BY-SA 4.0, https://sourcelibrary.org/book/great-kabbalistic-art-hartmann-schopper-1564-1569-schopper (finding aid only).
- Stephen M. Stigler, *Casanova's Lottery: The History of a Revolutionary Game of Chance*, Chicago 2003 (not read).
- Paolo Macry, *Giocare la vita. Storia del lotto a Napoli tra Sette e Ottocento*, Rome 1997 (not read).
- Sture Holm, "A simple sequentially rejective multiple test procedure", *Scandinavian Journal of Statistics* 6 (1979), 65–70.

## Versions

- **1.0** (20 October 2026): stages 1–7 coded and tested against the example sheets; the answer tests; the transcription; the paper.

## How to cite

Burford, B. (2026). The *Ars artium* oracle: does the machine compute its answers? (version 1.0). Source: https://github.com/BravoBravoIX/ars-artium-oracle
