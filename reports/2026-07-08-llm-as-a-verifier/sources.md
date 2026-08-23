# Sources

- arXiv abstract: https://arxiv.org/abs/2607.05391
- arXiv HTML: https://arxiv.org/html/2607.05391v1
- arXiv PDF: https://arxiv.org/pdf/2607.05391
- Official project page: https://llm-as-a-verifier.com/
- Official GitHub repository: https://github.com/llm-as-a-verifier/llm-as-a-verifier
- TurboAgent / Claude Code plugin: https://github.com/llm-as-a-verifier/TurboAgent
- Hugging Face Papers: https://huggingface.co/papers/2607.05391
- Local PDF text extraction: reports/2026-07-08-llm-as-a-verifier/sources/paper.txt
- Generated hero image: reports/2026-07-08-llm-as-a-verifier/llm-verifier-hero.png

## Candidate sweep notes

- Recent avoid-list from automation memory: HOLA, PairCoder, Persistent-State AI Control / Iterative VibeCoding, Program-as-Weights.
- Checked current arXiv `cs.AI` recent feed and search results for July 2026 agent/reasoning papers.
- Candidate titles observed included `DSpark: A High-Quality Large-Scale Dataset for Reinforcement Learning on Data Science Coding Tasks`, `AgentGym2: Scaling Agent Environments and Training for LLMs`, `Formal Disco: Formal Verification of Discrete-Time Lyapunov Stability Conditions`, and `LLM-as-a-Verifier`.
- Selected `LLM-as-a-Verifier` because it has the strongest combination of broad technical thesis, primary-source availability, official code/project page, cross-domain experiments, and long-term AgentOps relevance.

## Key checked facts

- Selected paper: `LLM-as-a-Verifier: A General-Purpose Verification Framework`.
- arXiv ID: `2607.05391`; submitted 2026-07-06.
- Authors: Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Yixing Jiang, Chelsea Finn, Marco Pavone, Ion Stoica, Azalia Mirhoseini.
- Institutions: Stanford University, UC Berkeley, NVIDIA Research.
- PDF: 31 pages by `pdfinfo`.
- Core idea: identify verification as a new scaling axis and use scoring-token probability distributions to produce continuous fine-grained verifier scores.
- Three scaling dimensions: score granularity, repeated evaluation, and criteria decomposition.
- Main benchmark anchors: Terminal-Bench V2 86.5%, SWE-Bench Verified 78.2%, RoboRewardBench 87.4%, MedAgentBench 73.3%.
- Terminal-Bench V2 candidate pool: GPT-5.5 under Capy; Pass@1 83.1%, Oracle Pass@5 92.1%, LLM-as-a-Verifier 86.5%.
- SWE-Bench Verified candidate pool: heterogeneous Claude Opus 4.5 / Gemini 3 Flash / MiniMax M2.5; Pass@1 mean 76.1%, Oracle 84.4%, LLM-as-a-Verifier 78.2%.
- Tie-rate factual anchor: coarse scoring induces 27% ties on Terminal-Bench V2; the verifier yields zero ties in the reported repeated-evaluation comparison.
- Progress-signal anchor: Spearman VOC 0.848 on successful Terminal-Bench V2 trajectories vs 0.769 on failed ones.
- RL anchor: roughly 1.8x sample efficiency on LIBERO with DSRL-SAC and roughly 1.1x on MATH with GRPO.
