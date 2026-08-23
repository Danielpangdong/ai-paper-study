# Sumi: Open Uniform Diffusion Language Model from Scratch

<p align="left">
  <a href="https://www.nlp.ecei.tohoku.ac.jp/projects/sumi/"><img src="https://img.shields.io/badge/%F0%9F%8C%90%20Project%20HP-1f72b8" alt="Project Page"></a>
  <a href="https://arxiv.org/abs/2606.19005"><img src="https://img.shields.io/badge/arXiv-2606.19005-b31b1b?logo=arxiv&logoColor=white" alt="arXiv"></a>
  <a href="https://huggingface.co/tohoku-nlp/sumi-7b"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Model-ffcc00" alt="Hugging Face"></a>
</p>

We provide the tools to evaluate the **Sumi 7B uniform-diffusion language model** using lm-eval, as well as the model's own definition files for reference.

Sumi is a native uniform diffusion language model trained from scratch, so it runs full bidirectional attention and denoises a canvas of randomly corrupted tokens; the scoring and generation reflect that.
We provide Sumi in a custom model class, therefore you need to set `trust_remote_code=True` to use it in transformers.

## Structure
- **`src/sumi_eval/`** — a [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
  plugin (`--model sumi`) that scores Sumi via the diffusion **NELBO** (loglikelihood /
  multiple-choice tasks) and generates via **iterative denoising** (`generate_until` tasks).
- **`model/`** — the model definition (`modeling_sumi.py`, `generation_sumi.py`,
  `configuration_sumi.py`): the same `trust_remote_code` files shipped with the HF model,
  included here for reference.


## Install

We use `uv` as the environment manager.

```bash
uv sync
```

## Run the evaluation

We provide the eval set by registering a custom model to the standard lm-eval.

### Multiple-choice / loglikelihood Tasks

```bash
uv run sumi-eval --model sumi \
  --model_args pretrained=tohoku-nlp/sumi-7b,canvas_length=2048,num_timesteps=128,effective_snr=1,ll_eosbos=1 \
  --tasks arc_easy --num_fewshot 0
```


### Generation Tasks

```bash
uv run sumi-eval --model sumi \
  --model_args pretrained=tohoku-nlp/sumi-7b,fill_mode=anchor,sampler=adaptive,\
max_new_tokens=256,num_denoising_steps=256,canvas_length=2048,gen_batch_size=8 \
  --tasks humaneval --num_fewshot 0 --confirm_run_unsafe_code
```

In our report, we used `fill_mode=anchor` with `max_new_tokens`
(max answer length), and adaptive sampler — `sampler=adaptive`.

Code tasks also need `--confirm_run_unsafe_code`. `--limit N` runs a subset.


## Inference

You can run the model directly from `transformers` (we recommend `transformers==5.8.1`) with `trust_remote_code=True`.

Sumi is a uniform diffusion model, so `generate()` does **not** decode left-to-right. Instead, it denoises a full fixed-length canvas of randomly corrupted tokens (`canvas_length`, default `2048`): the prompt is frozen at the front, an end-of-document delimiter (`<|endoftext|><|beginoftext|>`) is anchored `max_new_tokens` positions after it to match the training distribution, and the remaining positions are denoised as bidirectional context. The returned text is cut at the first `<|endoftext|>`.

> **Note:** Anchoring the delimiter is a temporary constraint imposed by the model's pretraining setup. We plan to release an SFT version to mitigate this.

```python
import torch
from transformers import AutoModelForMaskGeneration, AutoTokenizer

model_id = "tohoku-nlp/sumi-7b"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForMaskGeneration.from_pretrained(
    model_id, trust_remote_code=True, dtype=torch.bfloat16
).to("cuda").eval()

prompt = "Our journey into exploring diffusion language model begins,"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
out = model.generate(
    **inputs,
    max_new_tokens=256,       # content budget; the EOS/BOS delimiter is anchored here
    num_denoising_steps=64,   # refinement iterations — the main quality/compute dial
    sampler="ancestral",      # "ancestral" (default) or "adaptive" (sharper, for code/math)
    temperature=0.7,
)
print(tokenizer.decode(out.sequences[0], skip_special_tokens=True))
```

`generate()` returns the trimmed completion in `out.sequences` and the full untrimmed canvas in `out.canvas`.

## Citation

```bibtex
@misc{ye2026sumi,
      title={Sumi: Open Uniform Diffusion Language Model from Scratch}, 
      author={Mengyu Ye and Keito Kudo and Wataru Ikeda and Ryosuke Matsuda and Keisuke Sakaguchi and Jun Suzuki},
      year={2026},
      eprint={2606.19005},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2606.19005}, 
} 
```
## License
This model is licensed under Apache 2.0. It is intended for research and educational use.