---
library_name: transformers
license: other
base_model: Qwen/Qwen3-VL-8B-Thinking
tags:
- llama-factory
- full
- generated_from_trainer
model-index:
- name: HiViG-critic
  results: []
datasets:
- OpenGVLab/ScaleCUA-Data
language:
- en
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# Model Card for HiViG-critic for HiViG (History-aware Visually Grounded) test-time intervention framework


## Model Description

HiViG (History-aware Visually Grounded), a test-time intervention framework designed to equip CUAs with history state tracking and visually grounded error analysis. Inside our framework, we propose HiVis-critic, a multimodal model to serve as an intervention engine with these dual critique generation capabilities.

**Key Highlights:**

* 📝 **HiViG-critic for history state tracking**: maintains a macro-action history, a compact record of past interactions to date, recursively compressing past interactions into multi-step achieved goals, enabling better history-aware planning of policies over long horizons.  
* 🎯 **HiViG-critic for visually grounded error analysis**: verifies raw execution coordinates against actual visual states. If a proposed action is flawed, the model identifies the error dimension to provide the policy with corrective guidance before execution.  
- **Developed by:** Jaewoo Lee, Zaid Khan, Archiki Prasad, Justin Chih-Yao Chen, Supriyo Chakraborty, Kartik Balasubramaniam, Sambit Sahu, Elias Stengel-Eskin, Hyunji Lee, Mohit Bansal
- **Model type:** `Qwen3ForCausalLM`, fine-tuned Large Language Model
- **Language(s) (NLP):** English
- **License:** MIT
- **Finetuned from model:** Qwen3-VL-8B-Thinking


### Model Sources
- **Repository:** https://github.com/G-JWLee/HiViG
- **Paper:** [A History-Aware Visually Grounded Critic for Computer Use Agents](TBD)

## Overview of HiViG

![Overview of HiViG](https://raw.githubusercontent.com/G-JWLee/HiViG/main/assets/overview.png
)

## Uses

### Test-time intervention
The HiViG-critic model serves as an intervention engine with these dual critique generation capabilities to aid policies in long-horizon GUI tasks, enabling precise error analysis before execution and providing a history state tracking that allows better decisions.

## Citation
If you find this work useful, please consider citing us:
```bibtex
@article{lee2026hivig,
      title={A History-Aware Visually Grounded Critic for Computer Use Agents},
      author={Jaewoo Lee and Zaid Khan and Archiki Prasad and Justin Chih-Yao Chen and Supriyo Chakraborty and Kartik Balasubramaniam and Sambit Sahu and Elias Stengel-Eskin and Hyunji Lee and Mohit Bansal},
      year={2026},
      journal={arXiv preprint arXiv:2606.11078},
      url={https://arxiv.org/abs/2606.11078},
}
```