# Sources

- arXiv abstract/API: https://arxiv.org/abs/2606.30534
- arXiv PDF downloaded locally: `sources/orca.pdf`
- Extracted PDF text: `sources/orca.txt`
- arXiv HTML saved locally: `sources/arxiv-html.html`
- Official project page: https://orca-wm.github.io/
- Project page saved locally: `sources/project.html`
- Hugging Face Papers: https://huggingface.co/papers/2606.30534
- Hugging Face markdown/html saved locally: `sources/hf-paper.md`, `sources/hf-paper.html`
- Papers With Code search saved locally: `sources/paperswithcode-search.html`; no stable Orca-specific source was used.
- Semantic Scholar API saved locally: `sources/semantic-scholar.json`; returned 429, so it was not used as a factual source.

Key checked facts:

- Selected paper: `Orca: The World is in Your Mind`.
- arXiv ID: `2606.30534`; published 2026-06-29, v2 updated 2026-06-30.
- Authors: 57 authors under Orca Team; first authors include Yihao Wang, Yuheng Ji, Mingyu Cao, Yanqing Shen, Runze Xiao.
- Institution shown by paper/project page: Beijing Academy of Artificial Intelligence.
- Core idea: Next-State-Prediction over isolated next-token, next-frame, or next-action prediction.
- Data inventory: 125K hours of video, 160M event annotations, 11.5M VQA data; paper states this version uses one-tenth of video data.
- Evaluation readouts: text generation, image prediction, embodied action generation; Orca backbone frozen during readout post-training.
- Main reported comparisons used in report: text average Orca-4B 51.8 vs Qwen3.5-4B 46.7; PRICE-V0.1 Orca-4B+2B 59.8 vs FLUX.2 [klein] 56.1; action overall rule-based Orca 32.4 vs pi0.5 29.4.
- Training infrastructure result: 2.91 samples/sec/GPU on H100, 4.4x over StarVLA pipeline in paper table D1.
- Image generation note: built-in image generation created `/Users/mac/.codex/generated_images/019f1fea-5857-7eb3-a755-e9bda55e412f/ig_0366f5b4babc8983016a459cbc95a8819186f21773cab6bae5.png`; copied into this report as `orca-hero.png`.
