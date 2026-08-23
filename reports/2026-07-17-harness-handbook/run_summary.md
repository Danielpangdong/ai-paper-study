# AI Daily Paper Run Summary — 2026-07-17

- Automation: AI每日论文博客精选 (`ai`).
- Selected paper: **Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable**, arXiv:2607.13285v1 (2026-07-14).
- Why: Best evidence-weighted candidate from the 2026-07-16 arXiv cs.AI feed. It addresses behavior-to-code localization with a public implementation, a clearly described controlled comparison, table-level results, and direct relevance to reliable coding agents. It avoids recent report overlap (memory/verifier/KV cache/low-bit models).

## Candidate scorecard (editorial, /100)

| Candidate | Novelty 25 | Evidence 25 | Engineering impact 20 | Long-term 20 | Teaching 10 | Total |
|---|---:|---:|---:|---:|---:|---:|
| Harness Handbook | 22 | 22 | 19 | 18 | 9 | **90** |
| OriginBlame | 22 | 21 | 19 | 18 | 8 | 88 |
| LAPO | 21 | 20 | 17 | 17 | 8 | 83 |
| SPINE | 21 | 18 | 17 | 17 | 8 | 81 |

## Artifacts

- Full self-contained HTML: `/Users/mac/Desktop/AI论文解读/reports/2026-07-17-harness-handbook/AI-Daily-Paper-Harness-Handbook-2026-07-17.html`
- `sources.md`, `email_subject.txt`, `email_body.txt` in the same directory.
- No `mail-safe.html`: full HTML is text/SVG only and suitable as an attachment.

## Evidence / numerical verification

- Metadata and version: arXiv abstract v1; submitted 2026-07-14.
- Method: paper §3, Figure 1–2; execution route is static fact extraction → behavioral organization → hierarchical handbook → BGPD → current-source verification → planned edit / resync.
- Evaluation setup: paper §4.1 / Appendix C. Two harnesses, 30 behavior-driven requests each, same DeepSeek-V4-Pro planner, same snapshots/permissions/settings, handbook access as the changed condition; three plan judges.
- Key numbers checked against Figure 3 / §4.2.1: Codex 28.3% → 38.3%; Terminus-2 26.7% → 45.6%; planning token 0.102M → 0.089M (−12.7%) and 0.058M → 0.053M (−8.6%).
- Key Table 1 numbers checked: Codex F1 vs Opus reference 46.6→61.8 (file), 38.3→57.1 (symbol); Terminus-2 F1 vs GPT reference 76.5→89.3 (file) and symbol precision 73.9→93.3.
- Visual modules: (1) method flow, (2) results comparison, (3) applicability/extrapolation risk matrix. Each is inline SVG, labeled and sourced in caption.

## Validation and delivery state

- Built: complete.
- Static validation: **passed**. HTMLParser and UTF-8 passed; all 14 literal fixed-section titles present; 3 inline SVG visual modules; 0 scripts; 21,238-byte self-contained HTML. Four primary outbound sources returned HTTP 200.
- Browser validation: **passed** in local Chromium at 1440×1080 and 390×844. `scrollWidth == clientWidth` at both sizes (1440/1440; 390/390), title rendered, 14 H2 sections and 3 SVGs rendered. Screenshots: `/Users/mac/Desktop/AI论文解读/output/playwright/harness-handbook-desktop.png` and `/Users/mac/Desktop/AI论文解读/output/playwright/harness-handbook-mobile.png`. The Playwright CLI browser could not access the local HTTP server because of a separate network namespace; local Chromium Playwright fallback rendered and was visually inspected instead.
- Gmail preflight: searched `in:sent after:2026/07/14 subject:"【AI每日论文精选】"`; no prior matching sent mail.
- Gmail send: **sent** to `pangdong@sf-express.com` and `seekiingforhappiness@gmail.com`; message ID `19f6d3170faa0e54`.
- Gmail Sent read-back: **verified** exact subject, both recipients, attachment `AI-Daily-Paper-Harness-Handbook-2026-07-17.html`, MIME `text/html`, 21,238 bytes, `has_attachment=true`.
- Proof gap: author results were not independently reproduced; experiments measure plan/localization rather than final patch correctness or production reliability.
