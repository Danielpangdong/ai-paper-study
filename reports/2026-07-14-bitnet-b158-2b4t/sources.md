# Sources — BitNet b1.58 2B4T

Accessed 2026-07-14 (Asia/Shanghai). Primary evidence is the v2 PDF; numerical claims in the report cite its table/section directly.

1. Ma et al. (2025), [BitNet b1.58 2B4T Technical Report, arXiv:2504.12285v2](https://arxiv.org/abs/2504.12285v2). Primary paper and version metadata.
2. [PDF v2](https://arxiv.org/pdf/2504.12285v2). Method: §2–3; results: Table 1–4, §4; deployment: §5; limitations/future work: §7; evaluation conditions: Appendix B.
3. [Microsoft/BitNet](https://github.com/microsoft/BitNet). Official inference implementation, current README, MIT licence, hardware support and build instructions.
4. [microsoft/BitNet-b1.58-2B-4T](https://huggingface.co/microsoft/BitNet-b1.58-2B-4T). Official public checkpoint / model card. Hugging Face API checked: public, non-gated, revision `04c3b9ad9361b824064a1f25ea60a8be9599b127`, last modified 2025-12-17.
5. Wang et al. (2024), [1-bit AI Infra: Part 1.1, Fast and Lossless BitNet b1.58 Inference on CPUs](https://arxiv.org/abs/2410.16144). Official implementation-oriented companion evidence.
6. Liu et al. (2024), [KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache](https://arxiv.org/abs/2402.02750). Independent related low-bit serving baseline; not evidence that BitNet itself wins.
7. Yang et al. (2024), [Qwen2.5 Technical Report](https://arxiv.org/abs/2409.12186). Related baseline model family; BitNet's direct numerical comparison remains author-run and is not independently replicated here.

## Verification notes

- `Table 1`: non-embedding memory, CPU TPOT, estimated energy, 16 benchmark values. CPU testing: Intel i7-13800H, 8 threads, 128 generated tokens; BitNet uses bitnet.cpp while baselines use llama.cpp.
- `Table 2`: Qwen2.5 1.5B bf16/GPTQ INT4/AWQ INT4 versus BitNet; all instruction-tuned checkpoints.
- `Table 4`: arithmetic-operation energy model at 7nm with sequence length 512. This is not whole-system measured energy.
- The paper says “2B”; the current official BitNet repository table says “2.4B”. The report retains both labels and treats this as a parameter-counting discrepancy rather than resolving it by assumption.
