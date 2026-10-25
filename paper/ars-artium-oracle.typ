// Working paper for the ars-artium-oracle repository. Build: paper/build.sh
#set document(title: "The Ars artium oracle: does the machine compute its answers?", author: "Brett Burford")
#set page(paper: "a4", margin: (x: 2.3cm, y: 2.4cm), numbering: "1")
#set text(font: ("Libertinus Serif", "New Computer Modern"), size: 10.5pt, lang: "en", region: "au")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#1a4f8b"))
#set table(stroke: 0.4pt + luma(150), inset: 5pt)
#show table: set text(size: 9.2pt)
#show table: set par(justify: false)

#align(center)[
  #text(size: 16pt, weight: "bold")[The _Ars artium_ oracle: does the machine compute its answers?]
  #v(0.5em)
  #text(size: 11pt)[Brett Burford]
  #v(0.2em)
  #text(size: 9pt)[ORCID #link("https://orcid.org/0009-0003-6599-8297")[0009-0003-6599-8297] · Independent researcher, Australia]
  #v(0.2em)
  #text(size: 9pt)[Working paper, version 1.1, 25 October 2026 · not peer reviewed]
  #v(0.2em)
  #text(size: 9pt)[Code, data and results: #link("https://github.com/BravoBravoIX/ars-artium-oracle")[github.com/BravoBravoIX/ars-artium-oracle]]
]

#v(0.8em)
#block(inset: (x: 1.2cm))[
  #text(weight: "bold")[Abstract.] _Ars artium sive ars magna cabalistica_, ascribed to Hartmann Schopper and dated 1564/1569 but surviving in 17th- and 18th-century copies, teaches a Latin question-answering machine. A question's letters become numbers, the numbers pass through nine written stages, and remainders after division by 23 are read as the letters of the answer. We transcribed the rules and worked example sheets of Philadelphia, Penn LJS 251, compared the sheets with Penn Ms. Codex 1201, and coded the first seven stages exactly as written, with ambiguities as declared variants; tests and controls were committed before scoring. Fed the sheets' own inputs stage by stage, the rules reproduce the book's rhomboids (80/80 cells), branches (16/16), golden numbers (6/6) and algebra exactly, and its 108-cell cipher grids in 103/108 (sheet B) and 70/108 (sheet D) cells under the sheets' reading; two systematic slips on sheet D, found after scoring, account for all but one of its other misses, and shuffled controls never come close (_p_ = 0.0001). One changed letter of a question alters a root in 98–99 % of cases. Yet the two printed answers are Latin verse, ordinary Latin far beyond shuffled and machine-like controls (_p_ = 0.0001 each), naming events after the book's own date: Ghislieri's election as Pius V (1566) and Maximilian II's death in the 13th year of his reign (1576). The division that would produce the letters is ruled and left blank on both answer sheets in both copies, and the text's one worked letter count has three wrong sums and gives 42 letters for a 35-letter answer. Version 1.1 chains the stages so that the machine runs from the question alone. It reproduces about two thirds of every printed value on the three sheets (130/192, 83/126, 133/192; random questions 7–17, _p_ = 0.0001). It cannot reach the answers: both answered questions need the general division, whose rule, like the first proportion table, was on two leaves now missing (pp. 85–86 and 105–106). The book's 22 departures from its own rules are listed with corrections. They do not cluster where the answer is decided (7 of 50, against 7.0 by chance). The evidence weighs strongly toward a real, carefully followed procedure whose answers were written first.
]

= Introduction

_Ars artium sive ars magna cabalistica_ ("the art of arts, or the great cabalistic art") is a Latin treatise in two parts. Its title pages imitate a Frankfurt print of 1564 and 1569 and name Hartmann Schopper of Neumarkt, a poet and translator active in Frankfurt in the 1560s. Its dedications cannot be right as dated: one is to Moritz of Hessen-Kassel, Landgrave from 1592, and a preface by Johann Theodor de Bry, who was eight in 1569, calls the second part posthumous. Les Enluminures argue that the work is of the later seventeenth century and probably Italian; six manuscript copies are known and it was never printed.

The book teaches a machine. A question, written in Latin under strict rules of form, is turned letter by letter into numbers. The numbers pass through nine stages, and the end of the process yields letters that are meant to form the answer. Part 1 gives the rules with worked examples; part 2 gives the "reasons" and ends with four example sheets, labelled A to D, that carry questions through the stages. Two sheets end with an answer in Latin verse.

We ask two questions. Do the written rules, applied mechanically, reproduce the book's own worked numbers? And are the answers computed by the procedure, or written first? This is a study of how a device works, not a decipherment, and nothing here suggests that the device predicts anything.

= Earlier work

Les Enluminures' description of the copy now Penn Ms. Codex 1636 (TM 623) gives the content, the copies and the dating arguments. Penn's catalogue records of LJS 251 and Ms. Codex 1201 are descriptive; the LJS 251 record dates its mathematical notation to 1655–1699. The Wellcome catalogue describes MS.4464 (mid-18th century, 139 ff.) as a transcript of "an extremely rare printed book on fortune-telling by letters and numbers". Hoche's article on Schopper in the _Allgemeine Deutsche Biographie_ (1891) knows him as the author of a Latin _Reineke Fuchs_ and of the _Panoplia_ and mentions no cabalistic work. Source Library (sourcelibrary.org) offers an unreviewed AI transcription and English translation of the Amsterdam copy, BPH PH337 (CC BY-SA 4.0), which we used only to find chapters. We found no study of the machine's mechanism, no edition, and nothing on GitHub or Zenodo (searched 20 October 2026). We did not read Mundhenk's article in the _Killy Literaturlexikon_ (2011) or the literature on numerical "cabala" and lottery oracles (Stigler 2003; Macry 1997), and someone who knows that literature may find the practice described here already described for related books.

= Sources and transcription

The main witness is LJS 251 (Germany, 1655–1699; 139 ff.), from the Internet Archive images that Penn uploaded under the Public Domain Mark. Its example sheets were compared with those of Ms. Codex 1201 (part 2 only), read through Penn's IIIF service. Ms. Codex 1636 could not be obtained; the Wellcome and Florence copies are not online.

Claude (Anthropic's API) was given 113 page images of LJS 251 and returned text for 106: part 1 and the example sheets with Claude Opus 5.5, and 33 rule and example pages a second time with Claude Sonnet 5.5, at a cost of 7.82 US dollars. The model declined seven diagram pages. Claude read the declined pages that were needed from the images and checked every number used in a test against the page image; the median page-level agreement of the numbers read by the two passes is 0.93.

*How AI was used.* The pages of LJS 251 were read from the images by Claude (Anthropic, model Opus 5.5), with 33 rule and example pages read a second time by Claude (Anthropic, model Sonnet 5.5). The two passes agree on a median 0.93 of the numbers on each page, and all 71 worked numbers checked on pages both passes read were found by both. Claude also read the diagram pages the model declined and checked every number used in a test against the page image. An AI coding assistant (Claude Code) was used. The analysis reruns without any AI service; Claude's readings are stored as data.

= Method

The book's basic operation is a "difference": for numbers _a_ and _b_, _a_ − _b_ when _a_ ≥ _b_, but _b_ − _a_ − 1 when the lesser comes first. With it the stages are:

#table(
  columns: (auto, 1fr),
  [*Stage*], [*What the rules do (chapters of part 1)*],
  [1], [Sum the letter values of each word (A = 1 … I = 9, K = 10 … S = 90, T = 100 … Z = 500); four "lines" of differences between digits and between neighbouring words (ch. II)],
  [2], [For each word a digit "pyramid" (subtract three from every digit but the last) and a "root": (pyramid − sum × line-4 number) mod line-1 number, with nine exceptions; some roots are "crossed" (ch. III)],
  [3], [Two stepped rhomboids filled from lines 2–4, empty cells by differences of neighbours or of opposite cells (ch. IV)],
  [4], [Two "branches" (root 1 against the outer cells of each rhomboid) and an "orbit" of rings, one per word, each ring holding differences of a root with the branches and with rhomboid cells (ch. V)],
  [5], [A "golden number" from the first two and last two roots (ch. VI)],
  [6], [The "cipher": the orbit read spirally into a grid of twelve rows, with the roots down its sides (ch. VII)],
  [7], [Algebra on roots and their squares: subtraction, addition, multiplication; then division by the golden number (ch. VIII)],
  [8–9], [Two quotients give the start cell in the cipher, the first letter and the number of letters; proportion tables turn cipher numbers into letter numbers, kept mod 23 (ch. IX–X)],
)

We coded stages 1–7 as written; where the text can be read two ways, both readings are named variants. Each stage from 3 onward is tested _stage-locally_: it is fed the numbers the sheet itself shows for the stage before, so an early slip does not count against every later stage. All tests, controls, seeds (20261020) and the multiple-testing correction (Holm) were committed before scoring; the reproduction of stages 1–2 was run while the code was written and is reported as descriptive.

To ask whether the answers could come from the last stage, we scored each answer's letters with a Latin 5-gram letter model (nine classical and humanist texts from Project Gutenberg) against 10,000 shuffles of its own letters and 10,000 strings of uniform residues 1–23, the kind of output the stated last stage produces. To ask whether the machine depends on its question, we made every single-letter change to the four example questions and ran 2,000 random Latin questions.

= Results

#table(
  columns: (auto, 1fr, auto),
  [*Stage*], [*Compared with the book*], [*Agreement*],
  [1], [word sums; four difference lines; last number of line 4], [48/48; 154/154; 5/6],
  [2], [roots], [20/26],
  [3], [rhomboid cells, sheets B and D], [80/80],
  [4], [branches; canal roots reduced by 24 (by 23)], [16/16; 18/18 (14/18)],
  [5], [golden number, two sheets and four text examples], [6/6],
  [6], [cipher cells, sheet B: text's reading / sheets' reading], [83 / 103 of 108],
  [6], [cipher cells, sheet D: text's reading / sheets' reading / with two slips (exploratory)], [60 / 70 / 107 of 108],
  [7], [subtraction, addition, multiplication on both sheets; text's worked addition], [all exact],
)

*Stages 1–2.* The misses are telling. For the Antonius question the rule chapter gives 0 for the last number of line 4 and sheet A gives 2. For "Pij" the rule chapter works the very case and gets the root 6; sheet B has 68 and uses 68 downstream. For the Maximilian question the text's own later steps use the roots the rules give (16 and 31), while sheet D shows 3 and 10 and uses those: the book carries two computations of the same question.

*Stages 3–7.* The rhomboids, branches, golden numbers and algebra agree exactly. Canal roots are reduced by 24 on both sheets, where the text's "alphabetic number" is 23. In the cipher, the text sends the "upper semidiameter" down the inner side of each rhomboid, avoiding cells already used for the branches; the sheets use the branch side, and with that reading sheet B's 108-cell grid agrees in 103 cells. Sheet D agrees in 70; after scoring we found that its lower semidiameters use root 1 instead of root 2 and that its right half takes the roots one place late from the fourth ring, as if a root had been skipped, and with both slips 107 of 108 cells agree. Against 10,000 rearrangements of each sheet's own cells, no rearrangement does as well (_p_ = 0.0001, Holm 0.0004); the other sheet's inputs match 6–8 cells.

*Sensitivity.* One changed letter alters a root in 97.8–99.0 % of single-letter changes; 2,000 random questions give 2,000 different root sets. Nothing at the front of the machine fixes its answer.

*The answers.* Sheet B ends with the numbers 7.8.9.18.11.5.17.9.20.12 … and the reading _Ghislerium cernes Petri gratissima proles / Ex Alexandrinis currere nemoribus_, an elegiac couplet naming Michele Ghislieri, born near Alessandria and elected Pius V on 7 January 1566. Sheet D ends with _Dena trino pollens mortem concedet heroi_, a hexameter: "ten and three"; Maximilian II, emperor from July 1564, died on 12 October 1576, in the 13th year of his reign. Both answers score as Latin (−2.06 and −2.29 nats per letter) far beyond the shuffles (mean −3.35, best −2.94 and −2.80) and the residue strings (mean −3.24, best −3.00 and −2.95), close to real Latin windows (mean −1.92); _p_ = 0.0001 for each of four comparisons, Holm 0.0004.

*Where the mechanism stops.* The division by the golden number and its square, which yields the two quotients that fix the start cell, the first letter and the length of the answer, is ruled and left empty on both answer sheets in both copies; the rule text's worked division (image 82) cannot be followed from what is written. The only worked letter count for a printed answer (Maximilian, image 90) uses a golden number of 0 where sheet D has 2, quantities that are not sheet D's, three wrong sums out of seven (6290 − 1536 = 4553; 4553 ÷ 16 = 252 remainder 16; 252 ÷ 14 = 17) and arrives at 42 letters; the printed answer has 35. Sheet C has no answer in either copy, and sheet A none in LJS 251.

= The machine chained end to end (version 1.1)

Version 1.1 runs a 9-word question through every stage the text gives in full. It adds the subtraction lines built from the roots (larger root P, smaller M, places as in the golden number), the multiplication with its zero cases, the division for a golden number of 0 or 1 (chapter VIII, notes 5–7), and the starting cell, first letter and letter count (chapter IX). Two parts cannot be coded from LJS 251. The page numbers run 84, 87 and 104, 107. The division rule breaks off at the foot of p. 84 with the catchword _per_. The index on p. 118 lists a "Tabula prima proportionalitatis multiplicis" that is not in the book. The tables of compound and equal proportions are ruled but blank. A third pre-registration was committed before scoring; seed 20261025.

#table(
  columns: (1fr, 1fr),
  [*Test*], [*Result*],
  [12\. Chained reproduction: printed values from the roots on, from the question alone], [B 130/192, C 83/126, D 133/192; random questions mean 13.8, 7.2, 16.9 (best 38, 30, 50); _p_ = 0.0001 each, Holm 0.0003],
  [13\. Departures from the rules, each stage fed the book's own numbers], [50 on the sheets, 14 in the text's worked algebra; 22 items with corrections],
  [14\. Departures among the 54 of 384 values that feed the division], [7 of 50; 7.03 expected; _p_ = 0.58 (smallest possible 1.6 × 10#super[−58])],
  [15\. Golden number of the answered questions by the rules], [B 8 (sheet 5), D 2: beyond the surviving rules],
  [16\. Cipher cells needing the missing multiple table], [49 % (B 53, D 51 of 108)],
)

The front, rhomboids and branches come out of the question exactly, and every root a sheet gets wrong is carried forward. On sheet B the wrong roots 2 and 9 (5 and 11 for 15 and 7) turn the golden number from 8 into 5, so every algebra value differs. The departures are copying and arithmetic slips. There are five wrong roots, a sign (P 21 for M 21) and one spiral line of sheet B's cipher, plus sheet D's two systematic slips. In the text, a partial product has 9861335100 for 9851335100, and the pope multiplication copies its products by 80 into the residue line. The golden-1 division swaps 7682 into 7862. The first-letter example divides 5840 by 23 as if it were 6840. Both worked additions leave out root 7. The Maximilian count has four slips: 6290 − 1538 = 4553, 56 ÷ 3 taken as 16, 4553 ÷ 16 = 252 rest 16, and 252 ÷ 14 = 17. Run by the rule from its own first numbers, it gives 46 letters, not 42; the printed answer has 35. That count uses a golden number of 0, where the rules give 2 for that question. Zero is the one case in which the surviving text allows a short division. Where the written letter count does run (golden 0 or 1, 3.4 % of 10,000 random questions), its results are unusable: median 224, a quarter zero or negative.

= Discussion

The procedure is real, and its copyists followed it with care through seven stages, down to grids of more than a hundred cells that the written rules rebuild almost exactly; the disagreements are of the kind a copyist makes (a skipped root, a wrong root in a sub-rule, an unreadable step) and of the kind an author makes when the text and the sheets were not finished together (different roots for the same question). The front of the machine is chaotic: one letter changes everything after it. Against that, the two printed answers read as Latin verse (an elegiac couplet and a hexameter) and name, correctly, a papal election two years after the book's own date and an emperor's death twelve years after it, and the step that would have to turn the arithmetic into those letters is not shown anywhere. A mechanism that keeps remainders mod 23 does not produce Latin hexameters except by design, and the design is not in the book. Version 1.1 adds that the sheets' arithmetic was really computed from their questions, but that no route in the surviving rules leads from either question to its verse, and that the slips are scattered rather than gathered where the answer is decided. The evidence weighs strongly toward answers composed first, with the calculation shown as far as it could be shown. Whether the original author or a later editor wrote the verses, and whether readers of the time saw the oracle as a game, a demonstration or a deception, needs the literature of the genre, which we have not read.

= Limits

Two of the six known copies were read. The transcription is by Claude, which also checked the numbers used in tests against the images; it awaits a palaeographer's reading. Stages 3–7 are coded for questions of 7–10 words only (all surviving sheets have nine). The general division and the answer stage are not implemented, because their rule and first table are lost from LJS 251; they may survive in Amsterdam BPH PH337, not consulted for them. So "where it breaks" marks where the book stops showing its work, not a proof that no rule could exist. The chained machine is coded for 9-word questions; for version 1.1 Claude (model Opus 5.5, in Claude Code) read the text's worked numbers again from the images, and the checks on them are by code. The sheet-D slips are exploratory; the sheets' reading of the upper semidiameter was seen before the cipher test was scored, and the text's reading is the primary score. The Latin-likeness test shows the answers are Latin; it cannot say who wrote them.

= References

#set par(justify: false)
- Philadelphia, University of Pennsylvania, Kislak Center, LJS 251; Ms. Codex 1201; Ms. Codex 1636. Images: Internet Archive item `ljs251`; Colenda IIIF.
- London, Wellcome Collection, MS.4464, catalogue record (works/gjew7h5p).
- Les Enluminures, _Hartmann Schopper (?), Ars artium sive ars magna cabalistica_, description TM 623.
- R. Hoche, "Schopper, Hartmann", _Allgemeine Deutsche Biographie_ 32 (1891), 372–373.
- C. Mundhenk, "Schopper, Hartmann", in W. Kühlmann et al. (eds), _Killy Literaturlexikon_ 10 (2011), 565–566 (not read).
- Source Library, _Great Kabbalistic Art: Hartmann Schopper, 1564–1569_ (BPH PH337), AI transcription and translation, CC BY-SA 4.0 (finding aid only).
- S. M. Stigler, _Casanova's Lottery_, Chicago 2003 (not read). P. Macry, _Giocare la vita. Storia del lotto a Napoli tra Sette e Ottocento_, Rome 1997 (not read).
- S. Holm, "A simple sequentially rejective multiple test procedure", _Scandinavian Journal of Statistics_ 6 (1979), 65–70.
