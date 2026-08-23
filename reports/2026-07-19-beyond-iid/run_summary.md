# Run summary — 2026-07-19 Beyond IID

## Selected paper

- **Beyond IID: How General Are Tabular Foundation Models, Really?** — Purucker et al., arXiv:2606.30410v1, submitted 2026-06-29.
- Authors/affiliations verified from paper PDF: Prior Labs; University of Freiburg; University of Mannheim; INRIA Saclay; Technion; ELLIS Institute Tübingen; Zuse School ELIZA; Probabl.
- Why selected: evidence density and teaching value beat newer candidates. It reports a documented, code-linked benchmark across 142 curated datasets and confronts the deployment gap between IID random-split results and temporal/grouped generalization.

## Candidate scorecard (100)

| Candidate | Novelty /25 | Evidence /25 | Industry /20 | Long-term /20 | Teaching /10 | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Beyond IID | 22 | 25 | 18 | 19 | 9 | **93** | Selected |
| TabFM | 23 | 21 | 19 | 18 | 9 | 90 | Strong follow-up; official release/code/weights but not as complete a paper-level evidence package |
| SensorFM | 22 | 20 | 19 | 18 | 8 | 87 | High-stakes health data and reproducibility constraints lower confidence |
| PUST | 22 | 18 | 17 | 18 | 8 | 83 | Fresh preprint; author-run result and code availability not confirmed in this run |
| LongCrafter | 20 | 18 | 16 | 17 | 9 | 80 | Interesting but source/code evidence weaker for today’s evidence-first choice |

## Source coverage and numeric checks

- Primary paper PDF and arXiv abstract page reviewed. PDF is 99 pages, 6,752,042 bytes; arXiv v1.
- Source/code endpoints: TabArena code and DataFoundry recorded in `sources.md`; not executed.
- Independent/context sources: data-prior study (arXiv:2606.29241), Google TabFM official release, independent TabFM reproduction.
- Quantitative anchors checked against primary text: 1,128 -> 142 curation; 11 models = 3 TFM + 8 traditional baselines; 19% / 10.5% individual rank-1 shares; 49% significant TFM wins, additional 21% parity, 42 clear non-TFM wins; Figure 1 counts IID 103 / grouped 18 / temporal 21.
- All results are labelled as author-run. No claim is made that a specific TFM, including TabFM, won this benchmark.

## Build and validation status

- Directory: `/Users/mac/Desktop/AI论文解读/reports/2026-07-19-beyond-iid/`
- Built: complete self-contained HTML, sources, email subject/body. `mail-safe.html` not required because complete HTML is compact and uses no external assets/JS.
- HTML contract: 14 required literal section titles present; three information visuals (inline SVG workflow; quantitative results; applicability matrix); no JavaScript or external CDN.
- HTML/UTF-8 validation passed: Python `HTMLParser` parsed it; all 14 required literal section titles are present; 3 figure modules are present; no script tags or external CDN assets; final file is 23,399 bytes.
- Link validation passed for the five direct primary/code links (arXiv abstract/PDF, TabArena code redirect, DataFoundry); source links are separately listed in `sources.md`.
- Browser proof passed through local Chromium at 1440×1080 and 390×844. `scrollWidth == clientWidth` at both sizes (1440 and 390 respectively); no console errors after adding a self-contained favicon. Screenshots: `/Users/mac/Desktop/AI论文解读/.playwright-cli/page-2026-07-18T23-08-46-424Z.png` (desktop) and `/Users/mac/Desktop/AI论文解读/.playwright-cli/page-2026-07-18T23-08-56-895Z.png` (mobile).
- Gmail send and Sent read-back verified at 2026-07-19 07:10:01 -05:00: subject and both recipients match; attachment `AI-Daily-Paper-Beyond-IID-2026-07-19.html` was read back as `text/html`, 23,399 bytes. Gmail Message ID: `19f777e6d5c3fe8d`.

## Evidence caveats

- The paper tests selected 2026-era open-source TFM implementations, not every current model or a future release.
- The 70% statement is author-defined family-level peak/significance coverage, not an individual model’s guaranteed win rate.
- Real deployment still requires time/group split selection, held-out evaluation, costs/latency and drift monitoring.
