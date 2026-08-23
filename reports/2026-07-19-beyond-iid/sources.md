# Sources — Beyond IID report

Accessed 2026-07-19 (Asia/Shanghai). Primary evidence is marked **[P]**; independent/contextual material is marked **[C]**.

1. **[P]** Purucker, L. et al. (2026). *Beyond IID: How General Are Tabular Foundation Models, Really?* arXiv:2606.30410v1, submitted 2026-06-29. PDF: https://arxiv.org/pdf/2606.30410; abstract: https://arxiv.org/abs/2606.30410.
   - Used for: authors, institutions, data curation 1,128 -> 142, 3 TFM + 8 baselines, all quantitative statements, experimental design, limitations.
   - Anchors checked: abstract; §1; §2; §4; §5; §6; §7; Figure 1; Figure 4; Figure 6; Table 1.
2. **[P]** TabArena code portal: https://tabarena.ai/code and DataFoundry: https://github.com/TabArena/data-foundry.
   - Used for: reproducibility/code availability only. Not executed in this run.
3. **[C]** Türkmen, Z. et al. (2026). *Towards Evaluating Data Priors for Tabular Foundation Models*. arXiv:2606.29241. https://arxiv.org/abs/2606.29241.
   - Used for: related-baseline context that TFM training priors materially affect downstream behavior.
4. **[C]** Google Research (2026-06-30). *Introducing TabFM: A zero-shot foundation model for tabular data*. https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/.
   - Used only in candidate comparison and industry context; not used to support BeyondArena result claims.
5. **[C]** Pandey, Y. R. (updated 2026-07-07). *I Tried to Break Google's New Tabular Foundation Model. Then I Fixed It.* https://yashrajpandey.com/writing/breaking-google-tabfm/.
   - Used only as an independently published, reproducible engineering cross-check of a separate model; its 10-dataset study does not validate the 142-dataset BeyondArena conclusions.

## Numeric audit

| Claim in report | Primary anchor | Conditions / caution |
|---|---|---|
| 142 curated datasets from 1,128 candidates | Paper §1, §4 | Dataset curation result, not number of raw source records.
| 11 models; 3 TFM + 8 traditional baselines | Paper §1, §5 | TFM evaluated via ICL; traditional methods include default, tuned and tuned+ensemble configurations.
| 19% TabICLv2 and 10.5% TabPFN-2.6 rank-1 share | Paper §6 | Individual-model peak shares; not a family aggregate.
| TFM significant win on 49%, at least tie on another 21%, hence 70% | Paper §6 | Author-defined significance/peak framing; categories must not be presented as an individual model's win rate.
| 42 datasets clearly favor non-TFM | Paper §6 | Associated with large, high-dimensional, non-IID or high-cardinality settings.
| IID 103; grouped 18; temporal 21 | Paper Figure 1 | Counts can overlap with scale/feature sub-benchmarks; do not treat as a partition of every visual dimension.
