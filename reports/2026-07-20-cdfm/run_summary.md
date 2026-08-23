# Run Summary — AI每日论文博客精选 (`ai`) — 2026-07-20

## Selected paper

- **CDFM: Towards a General-Purpose Causal Discovery Foundation Model** — Qiao et al., arXiv:2607.11508v1, submitted 2026-07-13.
- Selected at **92/100** over ThReadMed-QA (89), Paper-replication (88), and DAG-FM (84). It offered the best combined evidence package: paper-level tables, a public inference package and weights, an example notebook, synthetic multi-mechanism tests, and Causal Chambers physical-benchmark results.
- Differentiation: does not repeat recent agent harness, parametric-recall, or tabular-generalization topics. It focuses on causal graph discovery and its precondition: identifiability.

## Candidate scorecard

| Candidate | Novelty /25 | Evidence /25 | Industry /20 | Long-term /20 | Teaching /10 | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| CDFM | 23 | 23 | 18 | 19 | 9 | **92** | Selected |
| ThReadMed-QA | 22 | 22 | 18 | 18 | 9 | 89 | High-stakes health evaluation; public end-to-end reproduction chain not verified |
| Paper-replication | 22 | 22 | 17 | 18 | 9 | 88 | Strong workflow idea; only 4 papers / 12 runs |
| DAG-FM | 23 | 18 | 17 | 18 | 8 | 84 | Fresh related preprint; weaker verified package this run |

## Source coverage and numeric checks

- Primary: arXiv abstract page and v1 PDF reviewed. Tables 1–8 and §6.1–6.5 read through local PDF text extraction.
- Official assets: GitHub shallow clone inspected; Hugging Face model card verified (Safetensors, Apache-2.0, 9.66M parameters); PyPI URL recorded. The clone documented inference but exposed only README, pyproject and one notebook at the inspected depth, so full training reproducibility is **not** claimed.
- Author/lab: Ruichu Cai / DMIR lab page reviewed.
- Independent/related: Nature Machine Intelligence Causal Chambers paper and NeurIPS AVICI paper/code used for context and baseline framing.
- Numeric anchors checked: Table 1 AUROC (five sample regimes); Table 2 F1; Table 3 all-15 AUROC but CPT/Linear F1 exceptions; Table 4 A1 0.952 AUROC, 0.727 F1, SHD 17. All labelled author-run.

## Artifact contract

- Directory: `/Users/mac/Desktop/AI论文解读/reports/2026-07-20-cdfm/`
- Full self-contained attachment: `AI-Daily-Paper-CDFM-2026-07-20.html`.
- Companion files: `sources.md`, `email_subject.txt`, `email_body.txt`, this `run_summary.md`.
- No `mail-safe.html` planned: the full HTML has no external JS/CDN or image assets and is sized for attachment after validation.
- Fixed literal sections: 14 planned. Visuals: three information modules (method flow SVG, paper-data AUROC SVG/table, applicability matrix). No JavaScript.

## Validation and delivery

- Gmail Sent preflight query at start: `in:sent after:2026/07/19 subject:"【AI每日论文精选】"` returned no matching messages, so this run did not risk duplicating a prior delivery.
- HTMLParser and UTF-8 validation passed after the final mobile layout change: 14/14 required literal section titles, 3 figure modules (2 inline SVGs plus applicability matrix), no JavaScript, no external assets; final attachment is 23,341 bytes.
- In-app browser validation passed: desktop 1440×1080 and mobile 390×844 both had `scrollWidth == clientWidth` (1440/1440 and 390/390). The two wide SVGs intentionally scroll only inside their figure containers on mobile (332px client width / 786px figure scroll width) to preserve readable labels. Desktop console errors: none.
- Built, sent, and Sent-read-back verified at 2026-07-20 07:09:31 -04:00. Exact subject and both recipients matched; attachment `AI-Daily-Paper-CDFM-2026-07-20.html` was confirmed as `text/html`, 23,341 bytes. Gmail Message ID: `19f7ca4551253006`.

## Evidence caveats

- CDFM is an arXiv v1 and its reported scores are author-run; no independent rerun happened in this automation.
- Observational graph discovery does not establish intervention effects, especially under unmeasured confounding, selection bias, or non-identifiability.
- The physical benchmark gives useful external evidence but does not guarantee transfer to complex production domains.
