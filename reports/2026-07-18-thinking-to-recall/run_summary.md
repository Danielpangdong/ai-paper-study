# Run summary — 2026-07-18 — Thinking to Recall

## Selection

Selected paper: **Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs** — Gekhman et al., arXiv:2603.09906v1, submitted 2026-03-10.

| Candidate | Novelty /25 | Evidence /25 | Engineering /20 | Long-term /20 | Teaching /10 | Total |
|---|---:|---:|---:|---:|---:|---:|
| Thinking to Recall | 23 | 24 | 17 | 19 | 8 | **91** |
| TabFM | 21 | 22 | 19 | 18 | 8 | 88 |
| SensorFM | 22 | 21 | 19 | 17 | 7 | 86 |

Why: among fresh candidates, this paper had the clearest table-/section-level evidence, two controlled mechanism tests (Dummy and Facts), and a quantified failure mode. It is differentiated from the 2026-07-17 harness/localization report and avoids the recent memory/verifier/low-bit focus.

## Evidence coverage and numerical checks

- Primary: paper PDF + arXiv HTML, Google Research official write-up; sources listed in `sources.md`.
- Cross-checks: SimpleQA original paper, EntityQuestions official repo, and Goyal et al. ICLR 2024 pause-token baseline.
- Numbers checked against paper §5.1, §5.3 and Table 1: ON Dummy 0.206→0.262 (SimpleQA-Verified), 0.457→0.554 (EntityQuestions); clean/hallucinated trace rates 41.4%/26.4% and 71.1%/32.2%; Table 1 27.9→31.3 and 56.9→59.8.
- Report explicitly labels author claims, paper-backed data, and editorial inference. No claim of general intelligence, production readiness, or universal test-time-scaling benefit.

## Built artifacts

- `AI-Daily-Paper-Thinking-to-Recall-2026-07-18.html` — self-contained, 22,694 bytes.
- `sources.md`, `email_subject.txt`, `email_body.txt`.
- `assets/thinking-to-recall-2603.09906v1.pdf` and extracted `assets/paper.txt` retained for evidence audit.
- No `mail-safe.html`: the full HTML is small enough for attachment and contains no external scripts/CDNs.

## Validation

- HTMLParser / UTF-8: pass.
- 14 literal required section titles: pass.
- Information visuals: 3 (`图 1` method-control SVG; `图 2` results table/bar chart; `图 3` industry/risk-chain SVG).
- Inline JS: none. External image dependencies: none.
- Browser proof: passed at 1280px and 390px via local HTTP. Outer document width equaled viewport (1280/1280 and 390/390). On mobile, two wide SVG diagrams and two tables use intentional internal horizontal scrolling; no page-level overflow. Screenshots: `/Users/mac/Desktop/AI论文解读/output/playwright/thinking-to-recall-desktop.png`, `/Users/mac/Desktop/AI论文解读/output/playwright/thinking-to-recall-mobile.png`.

## Delivery

- Gmail Sent preflight: no matching sent email for `Thinking to Recall` after 2026-03-01.
- Sent to: `pangdong@sf-express.com`, `seekiingforhappiness@gmail.com`.
- Subject: `【AI每日论文精选】推理不是解释，它可能是在帮模型调取记忆`.
- Gmail read-back: verified. Message ID: `19f7257bf5e37997`; attachment MIME `text/html`, filename `AI-Daily-Paper-Thinking-to-Recall-2026-07-18.html`, 22,694 bytes.

## Proof gap

- No independent rerun, author code repository, or recipient-open confirmation. The paper is a v1 preprint and its mechanism experiments rely heavily on closed Gemini models and author-run evaluation/verification steps.
