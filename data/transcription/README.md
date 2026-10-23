# Transcription of Penn LJS 251 (machine reading, two passes)

Our diplomatic transcription of pages of the Philadelphia manuscript LJS 251, *Ars artium sive ars magna cabalistica*. The file names give the image number of the Internet Archive item `ljs251` (zero-based, `ljs251_NNNN.jp2`). Each page was converted to a JPEG of at most 2,200 pixels on the long side, and that JPEG was sent to the model. The SHA-256 in the logs is the hash of that JPEG.

| Pass | Model | Pages | Seed | Cost |
|---|---|---|---|---|
| A | Claude Opus 5.5 (`claude-opus-5-5`, Anthropic API) | images 8–102, 104, 106, 108 (part 1: rules and tables), 262, 266–274, 276–279 (end-of-book example sheets) | 25101 + image number | 6.81 USD |
| B | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | 33 rule and example pages (see `log_B.jsonl`) | 25102 + image number | 1.00 USD |

The two passes used different instructions and were not shown each other.

- **Refusals.** The model returned no text for images 66, 72, 266, 271, 272, 273 and 279 (`stop_reason` "refusal"). Those pages hold diagrams and the two answer sheets. Where they were needed (66, 266, 271, 272, 279), Claude read them from the images, and those readings are in `../examples.json` and `../sheets.json`.
- **Status.** These are machine readings, and they are untrusted. Claude checked every number used in a test against the page image. Known misreadings in pass A: image 23, line 1 "21" should be "11", and line 3 "2" should be "1"; image 89, the "5840" of the text may be "6840".
- **Agreement.** The median agreement of the numbers read by the two passes, page by page, is 0.93 (`../../results/passes.json`).

## Licence

The manuscript is in the public domain. This transcription is licensed CC BY 4.0 (see the main README).
