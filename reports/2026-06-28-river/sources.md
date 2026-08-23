# Sources - RiVER daily paper report

- Paper: `Reinforcement Learning without Ground-Truth Solutions can Improve LLMs`
  - arXiv: https://arxiv.org/abs/2606.27369v1
  - PDF: https://arxiv.org/pdf/2606.27369v1
  - Local HTML copy: `sources/river-arxiv.html`
  - Local PDF copy: `sources/river.pdf`
  - Local text extraction: `sources/river.txt`, `sources/river-layout.txt`

- Benchmark/context sources
  - AtCoder: https://atcoder.jp/
  - ALE-Bench GitHub: https://github.com/SakanaAI/ALE-Bench
  - ALE-Bench README copy: `sources/ale-bench-readme.md`
  - LiveCodeBench GitHub: https://github.com/LiveCodeBench/LiveCodeBench
  - LiveCodeBench README copy: `sources/livecodebench-readme.md`
  - USACO benchmark GitHub: https://github.com/princeton-nlp/USACO
  - USACO README copy: `sources/usaco-readme.md`

- Selected paper facts used
  - arXiv ID: `2606.27369v1`
  - Posted: `2026-06-25`
  - Authors: Yingyu Lin, Qiyue Gao, Nikki Lijing Kuang, Xunpeng Huang, Kun Zhou, Tongtong Liang, Zhewei Yao, Yi-An Ma, Yuxiong He
  - Institutions: University of California, San Diego; Snowflake AI Research
  - Method: Ranking-induced VERifiable framework (`RiVER`)
  - Training: 12 AtCoder Heuristic Contest tasks, AHC047-AHC062 candidate pool with 4 excluded
  - Backbones: Qwen3-8B and GLM-Z1-9B-0414
  - Main reported results: ALE rating +142 / +157; ALE rank percent -8.9 / -9.4; exact-solution benchmark average +2.4 / +3.5 points

- Image generation note
  - Generated with ChatGPT Image 2.0 into `/Users/mac/.codex/generated_images/019f0b50-e732-7d70-ae3d-0c8e97a15a60/`.
  - Cropped local copy used in report: `/Users/mac/Desktop/AI论文解读/reports/2026-06-28-river/river-chatgpt-infographic-cropped.png`.
  - The top generated header was removed because it contained a stale date.
