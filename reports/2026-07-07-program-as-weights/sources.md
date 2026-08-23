# Sources

- arXiv abstract: https://arxiv.org/abs/2607.02512
- arXiv HTML: https://arxiv.org/html/2607.02512v1
- arXiv PDF: https://arxiv.org/pdf/2607.02512
- Official GitHub organization: https://github.com/programasweights
- Official demo: https://programasweights.com
- Hugging Face Papers: https://huggingface.co/papers/2607.02512
- Papers With Code search checked: https://paperswithcode.com/search?q=Program-as-Weights
- Local PDF text extraction: reports/2026-07-07-program-as-weights/sources/paw_pdf.txt
- Generated hero image: reports/2026-07-07-program-as-weights/paw-hero.png

Key checked facts:

- Selected paper: `Program-as-Weights: A Programming Paradigm for Fuzzy Functions`.
- arXiv ID: `2607.02512`; submitted 2026-07-02.
- Authors: Wentao Zhang, Liliana Hotsko, Woojeong Kim, Pengyu Nie, Stuart Shieber, Yuntian Deng.
- Institutions: University of Waterloo, Cornell University, Harvard University.
- Core idea: compile fuzzy functions from natural-language specifications into compact locally executable neural artifacts.
- System: 4B compiler, frozen lightweight interpreter, current best instantiation is Text-to-LoRA.
- Dataset: FuzzyBench, 10M examples across 29 thematic versions and more than 800 sub-categories.
- Main result used in report: PAW Qwen3-0.6B 73.78% exact match on FuzzyBench vs Qwen3-32B prompting 68.70%; roughly 50x less inference memory.
- Local execution facts used in report: about 430MB shared GGUF base plus about 23MB per-program LoRA adapter; roughly 30 tokens/s on MacBook M3; Q5_K_M + Q4_0 table reports 31.6 tokens/s with 0.48s cold load.
