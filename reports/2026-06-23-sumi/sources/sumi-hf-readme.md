---
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
tags:
- diffusion
- discrete-diffusion
- uniform-diffusion
---



# Sumi-7B

<p align="left">
  <a href="https://www.nlp.ecei.tohoku.ac.jp/projects/sumi/"><img src="https://img.shields.io/badge/%F0%9F%8C%90%20Project%20HP-1f72b8" alt="Project Page"></a>
  <a href="https://arxiv.org/abs/2606.19005"><img src="https://img.shields.io/badge/arXiv-2606.19005-b31b1b?logo=arxiv&logoColor=white" alt="arXiv"></a>
</p>
Sumi is a native uniform diffusion language model trained from scratch, so it runs full bidirectional attention and denoises a canvas of randomly corrupted tokens.
We provide Sumi in a custom model class, therefore you need to set `trust_remote_code=True` to use it in transformers.

We recommend `transformers==5.8.1`.

For more details, please refer to [our project page](https://www.nlp.ecei.tohoku.ac.jp/projects/sumi/) and [technical report](https://arxiv.org/abs/2606.19005).

## Quickstart

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
