# AI Daily Paper Run Summary — 2026-07-14

- Automation: AI每日论文博客精选 (`ai`)
- Run time: 2026-07-14 Asia/Shanghai
- Selected paper: **BitNet b1.58 2B4T Technical Report**, arXiv:2504.12285v2
- Authors / institutions: Shuming Ma et al.; Microsoft Research with listed academic affiliations.
- Report: `/Users/mac/Desktop/AI论文解读/reports/2026-07-14-bitnet-b158-2b4t/AI-Daily-Paper-BitNet-b1.58-2B4T-2026-07-14.html`

## Candidate selection (100 points)

| Candidate | Novelty /25 | Evidence /25 | Impact /20 | Long-term /20 | Teaching /10 | Total |
|---|---:|---:|---:|---:|---:|---:|
| BitNet b1.58 2B4T | 23 | 22 | 19 | 18 | 9 | **91** |
| Scalable oversight with weak LLMs | 21 | 22 | 17 | 19 | 8 | 87 |
| KIVI | 19 | 23 | 18 | 17 | 9 | 86 |
| bitnet.cpp CPU inference | 17 | 22 | 19 | 16 | 8 | 82 |

Selection reason: avoids the recent memory/agent and KV-cache reports while providing an end-to-end, publicly inspectable claim: method, 2B checkpoint, official inference code, and table-level baseline comparison. The paper is a technical report marked work in progress, therefore evidence confidence is medium rather than high.

## Evidence coverage and numerical checks

- Primary PDF v2, official GitHub, official Hugging Face checkpoint/API metadata, related official CPU-inference paper, independent related KIVI baseline, and Qwen2.5 technical report were collected in `sources.md`.
- Rechecked from paper Table 1: BitNet non-embedding memory 0.4 GB; CPU TPOT 29 ms; estimated energy 0.028 J; ARC-Challenge 49.91; GSM8K 58.38; MMLU 53.17; HumanEval+ 38.40; 16-task average 54.19.
- Rechecked from Table 2: BitNet / Qwen bf16 / GPTQ INT4 / AWQ INT4 memory = 0.4 / 2.6 / 0.7 / 0.7 GB; average = 55.01 / 55.72 / 52.15 / 51.17.
- Conditions preserved: latency uses an Intel i7-13800H, 8 threads, 128 generated tokens; BitNet uses bitnet.cpp while baselines use llama.cpp. Energy is a 7nm arithmetic-operation model at sequence length 512, not device-metered power.
- Metadata discrepancy surfaced: paper uses 2B naming, current official repository table lists 2.4B. Report does not collapse this into a single exact count.

## Artifact and validation

- Required literal sections: 14 / 14.
- Visual modules: 3 / 3 — inline SVG method flow; memory/latency comparison; limitations/adoption matrix. All are HTML/SVG and carry source/interpretation notes.
- No JavaScript and no external CSS/CDN. No local asset references.
- `mail-safe.html`: not needed; complete self-contained HTML is suitable for attachment (19,623 bytes).
- HTMLParser / UTF-8: passed; fixed literal sections 14/14; `<svg>` 1; `<table>` 2; scripts 0; no local references.
- External link audit: all seven report links returned HTTP 200 on 2026-07-14.
- Browser proof: desktop 1440×1080 and mobile 390×844 inspected through local HTTP serving (the browser blocks `file:` URLs). Screenshots: `/Users/mac/Desktop/AI论文解读/output/playwright/bitnet-desktop-top.png`, `bitnet-desktop-mid.png`, `bitnet-mobile-top.png`, `bitnet-mobile-mid.png`. No overlap, blank graphic, or page-level horizontal overflow observed; wide tables use an intentional horizontally scrollable container with sticky first column.
- Browser console's only error was a harmless missing `favicon.ico` 404 from the temporary local HTTP server.

## Delivery

- Gmail precheck: no matching Sent message before send.
- Send status: sent.
- Read-back status: verified in Sent.
- Message ID / thread ID: `19f5dbc821d05a28`.
- Sent read-back: subject and both recipients (`pangdong@sf-express.com`, `seekiingforhappiness@gmail.com`) confirmed; attachment `AI-Daily-Paper-BitNet-b1.58-2B4T-2026-07-14.html`, `text/html`, 19,623 bytes, confirmed.

## Proof gap

- Built, validated, sent, and read-back verified are complete. The paper's benchmark and energy claims are author-reported; this automation did not independently train the model, run its benchmark suite, or meter hardware power. The report flags this rather than presenting an author table as production proof.

## Avoid-next directions

- BitNet b1.58 / ternary native-weight training / 1-bit LLM inference.
- Do not repeat generic quantization, KV-cache compression, or a claim that low-bit inference universally lowers production cost.
