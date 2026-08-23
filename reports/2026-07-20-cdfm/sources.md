# Sources — CDFM (2026-07-20)

## Primary and first-party

1. Qiao et al., **CDFM: Towards a General-Purpose Causal Discovery Foundation Model**, arXiv:2607.11508v1, 2026-07-13. https://arxiv.org/abs/2607.11508 ; PDF https://arxiv.org/pdf/2607.11508
   - Read locally from the v1 PDF. Numeric anchors in the report were checked against §6.1–6.5 and Tables 1–8.
   - Table 1: CDFM AUROC 0.864/0.878/0.885/0.887/0.888 for N=500/1000/2000/3000/4000; Table 2 F1 0.552/0.578/0.587/0.591/0.591.
   - Table 3: CDFM wins AUROC on all 15 listed mechanisms, but not every F1: CPT and Linear list stronger non-CDFM F1 baselines.
   - Table 4 (Causal Chamber A1): CDFM AUROC 0.952, F1 0.727, precision 0.889, recall 0.615, SHD 17.
2. CDFM official code: https://github.com/DMIRLAB-Group/CDFM
   - Shallow clone inspected on 2026-07-20: top-level README.md, pyproject.toml, one Causal Chambers notebook. It documents inference and installation, but this run did not find a complete visible training pipeline in the clone.
3. CDFM official weights/model card: https://huggingface.co/DMIRLAB/CDFM
   - Page indicated Safetensors, Apache-2.0, and 9.66M parameters at verification time.
4. CDFM PyPI package: https://pypi.org/project/cdfm-base/
5. Ruichu Cai / DMIR lab page: https://ruichucai.github.io/zh-cn/

## Independent / baseline context

6. Gamella, Peters, Bühlmann, **Causal chambers as a real-world physical testbed for AI methodology**, Nature Machine Intelligence 7, 107–118 (2025). https://www.nature.com/articles/s42256-024-00964-x
   - Independent source for the benchmark CDFM uses; explains why physical, intervenable systems are stronger external evidence than simulations, while still not a guarantee of transfer to complex systems.
7. Lorch et al., **Amortized Inference for Causal Structure Learning (AVICI)**, NeurIPS 2022. https://arxiv.org/abs/2205.12934 ; code https://github.com/larslorch/avici
   - Relevant published baseline for direct amortized graph prediction from datasets.

## Candidate discovery and scorecard

| Candidate | Novelty /25 | Evidence /25 | Industry /20 | Long-term /20 | Teaching /10 | Total | Evidence used |
|---|---:|---:|---:|---:|---:|---:|---|
| CDFM (selected) | 23 | 23 | 18 | 19 | 9 | **92** | Paper + code + weights + physical benchmark |
| ThReadMed-QA | 22 | 22 | 18 | 18 | 9 | 89 | Paper, dataset/metric details; high-stakes and weaker reproducibility chain |
| Paper-replication | 22 | 22 | 17 | 18 | 9 | 88 | Paper with 12 runs over 4 papers; narrow corpus |
| DAG-FM | 23 | 18 | 17 | 18 | 8 | 84 | Fresh related preprint; complete source package not verified this run |

Candidate links: CDFM https://arxiv.org/abs/2607.11508 ; ThReadMed-QA https://arxiv.org/abs/2607.12884 ; Paper-replication https://arxiv.org/abs/2607.02134 ; DAG-FM https://arxiv.org/abs/2607.11510 .

## Interpretation rule

- “作者报告/论文数据” means figures supplied by the paper’s authors. This run did not independently rerun CDFM.
- “本报告推演” is explicitly labeled and must not be read as a paper result.
- Causal discovery from observational data should not be equated with identifying interventional effects or approving automated decisions.
