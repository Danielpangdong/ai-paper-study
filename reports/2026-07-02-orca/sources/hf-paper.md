Title: Orca: The World is in Your Mind

URL Source: https://arxiv.org/html/2606.30534

Markdown Content:
###### Abstract

We introduce Orca, an initial instantiation of a general world foundation model. Orca learns a unified world latent space from multimodal world signals and exposes it through multimodal readout interfaces. Rather than optimizing isolated next-token, next-frame, or next-action prediction, we are centered on Next-State-Prediction modeling, offering a unified state-transition modeling route toward understanding, predicting, and acting upon the world. Orca learns through two complementary paradigms: unconscious learning captures dense natural state transitions from continuous videos, and conscious learning models sparse meaningful state transitions by language-described events and VQA supervision. For pre-training, we construct a large-scale world-learning inventory data, including 125K hours of video data and 160M event annotations. After pre-training, Orca learns a unified world latent space. To examine whether the learned latent supports downstream, we evaluate it by three representative downstream readouts: text generation, image prediction, and embodied action generation. Orca’s backbone is frozen, and only the lightweight modality-specific decoders are trainable. Experiments show the scalability of the proposed paradigm and verify that stronger world latent enables stronger downstream readouts. Orca outperforms similar-sized specialized baselines. These results show that Orca, as a general world foundation model, presents a promising approach to understanding, predicting, and acting upon the world. Finally, we discuss the current limitations, aiming to provide useful insights and inspiration for the community.

![Image 1: Refer to caption](https://arxiv.org/html/2606.30534v1/x1.png)

Figure 1: The Orca’s overall framework. Orca follows an Encoder-Decoder architecture. Given multimodal world signals, the Encoder learns a world latent through two complementary paradigms: unconscious learning and conscious learning. Unconscious learning captures dense natural state transitions, while conscious learning captures sparse meaningful state transitions. To prove that the learned latent is effective, the Encoder is frozen after pre-training, and only the lightweight modality-specific decoders are trainable separately. The Decoder reads out the latent into text, images, actions, and other modalities.

## 1 Introduction

We argue that the essential next step toward general intelligence is to build a model that can continuously learn and self-evolve like a human, and ultimately transcend human cognitive boundaries. As it internalizes physical laws, causal relationships, and dynamic evolution, this model is expected to develop into a self-emerging intelligence system. Such a model should continuously absorb multimodal world signals to model the world’s latent states. Ideally, these signals should encompass neural signals such as vision, text, audio, action, and tactile; also include physical signals such as force and light; and even include signals from fields such as the macrocosm, the microscopic quantum systems, and life sciences. More importantly, such a model should use state-transition modeling as a unified paradigm for both observed and unknown domains, thereby opening new possibilities for exploring the world.

From this perspective, intelligence should not merely be Next-Token-Prediction model that can respond to instructions (DeepSeek-V4; qwen36_35b_a3b; Emu3; GPT54), Next-Frame-Prediction model that can generate high-quality images and videos (nanobananapro; ChatGPT-Images-2.0; seedance2.0), or Next-Action-Prediction model that can generate high-quality action (pi0.7; DreamZero; GR00TN1.7). Instead, it should be defined by the ability to build world states and support the latent space for diverse downstream tasks. These points toward a general world foundation model grounded in Next-State-Prediction modeling, and including implicit dynamics and explicit conditions. Our conception visualization is shown in Appendix [A](https://arxiv.org/html/2606.30534#A1 "Appendix A Orca Conception ‣ Orca: The World is in Your Mind").

We present Orca, a world learner that takes an initial step toward the above goal by learning a world latent space. Figure [1](https://arxiv.org/html/2606.30534#S0.F1 "Figure 1 ‣ Orca: The World is in Your Mind") shows the Orca’s overall framework. In this version, Encoder focuses on two fundamental signal types: visual and language. Visual signals, including videos and images, are similar to how humans perceive the world. Language signals correspond to how humans understand the world, providing causal explanations and task intentions. Orca has two learning paradigms to realize:

1.   1) Unconscious learning aims to learn natural and dense state transitions from continuous video. This process does not rely on labeled tags, but instead uses the supervision provided by itself. The model learns natural evolution by predicting the latents of the next frames and internalizes state transitions.

2.   2) Conscious learning aims to learn meaningful and sparse state transitions under the constraints of instructions. The model uses textual constraints to learn meaningful state transitions at the event level.

Orca builds a world latent space through the two paradigms. The Decoder reads out text, images, and actions. Note that these readouts are not intended to chase task-specific SOTA performance, but to examine two core questions: 1) the proposed paradigms are feasible and scalable, and 2) stronger world modeling leads to stronger downstream readouts. Therefore, the Orca backbone is frozen during decoder post-training, and only lightweight readout modules are trainable. Experiments answer these questions: Orca’s training losses continue to decrease with model size and data scale, and its language, image, and action readouts consistently improve as pre-training scales up. The main contributions are as follows:

*   •
We propose Orca. Orca learns a world latent space from multimodal world signals. This latent space can serve as a general interface for multimodal downstream readouts.

*   •
We design two complementary learning paradigms. Unconscious learning captures natural dense state transitions from continuous videos, while conscious learning leverages textual conditions to learn meaningful sparse state transitions associated with decisions and task outcomes.

*   •
We construct a large-scale collection to support Orca’s learning paradigm. We built the inventory data that contains 125K hours of videos and 160M event annotations, covering ego-centric interaction, exo-centric manipulation, action-free robot execution, and event-level transitions for pre-training.

*   •
Experiments show that Orca learns the effective world latent. Experiments demonstrate the scalability of the proposed paradigm and show through readout probing that a stronger world latent enables stronger downstream capabilities. Across text generation, real-world interactive image prediction, and embodied action generation, Orca outperforms specialized baselines at a comparable scale. We further provide a careful analysis of its current limitations, aiming to offer insights and inspiration for the community’s future sustainable development.

## 2 Orca

### 2.1 Modeling

##### Macro.

Orca formulates world learning as latent world-state modeling, including state abstraction from multimodal world signals and state transition. Given the world signals \mathcal{X},\mathcal{X}=\{X^{m}\}_{m\in\mathcal{M}}, where \mathcal{M} can encompass a rich variety of modalities. Ideally, \mathcal{X} should include all signals present in the world, such as common multimodal signals: language, vision, and audio; physical signals: force and light; and even signals beyond human perception: infrared radiation. Mapping \mathcal{X} to a latent world state \mathcal{S}, i.e., \mathcal{S}=f_{\theta}(\mathcal{X}). We model the state S\in\mathcal{S} evolves forwards and backwards under implicit dynamics and explicit conditions:

S_{t+\Delta}\sim p_{\Theta}\left(S_{t+\Delta}\mid S_{t},z_{t},c_{t}\right),\quad\Delta\in\mathbb{Z}_{\neq 0}.(1)

where, z_{t} is a way to realize invisible dynamics. It captures latent or unobserved factors that drive state changes, such as physical laws, object properties, scene dynamics, and environmental forces. c_{t} is a way to realize explicit conditions. It refers to observed conditions such as human instructions. \Delta>0 represents predicting future states S_{>t}, while \Delta<0 represents backtracking to past states S_{<t}.

##### Details.

In this version, Orca uses visual signals and language signals as two fundamental types of multimodal world signals. To realize the state-transition modeling in Equation ([1](https://arxiv.org/html/2606.30534#S2.E1 "Equation 1 ‣ Macro. ‣ 2.1 Modeling ‣ 2 Orca ‣ Orca: The World is in Your Mind")), Orca adopts two complementary learning paradigms: unconscious learning and conscious learning.

1.   1) Unconscious learning learns state transitions from observation alone. The model observes naturally occurring transitions without explicit semantic conditions. It can learn how objects move, natural dynamics, physical regularities, or how scenes transition over time. This is equivalent to c_{t}=\varnothing, i.e., S_{t+\Delta}\sim p_{\Theta}^{\mathrm{u}}\left(S_{t+\Delta}\mid S_{t},z_{t}\right). In this paradigm, the target state originates from the nearest future observation. Unconscious learning can learn dense and natural state transitions.

2.   2) Conscious learning learns state transitions under explicit semantic conditions. Given a language signal, Orca treats it as an explicit condition that guides the state transition. The language condition can specify an event c_{t}=e_{t+\Delta}, including a future or past event, i.e., S_{t+\Delta}\sim p_{\Theta}^{\mathrm{c}}(S_{t+\Delta}\mid S_{t},z_{t},e_{t+\Delta}). The condition can also be a task intention or a causal premise. It guides how the current state should transition toward a target state. Conscious learning can learn sparse and meaningful state transitions.

### 2.2 Architecture

![Image 2: Refer to caption](https://arxiv.org/html/2606.30534v1/x2.png)

Figure 2: Overview of Encoder. Orca learns a world latent representation through two learning paradigms. Unconscious learning uses video data to capture dense and natural state transitions. Conscious learning uses language instructions as explicit semantic conditions to capture sparse and meaningful state transitions.

##### Encoder.

Orca focuses on the Encoder, which learns a unified world latent space for state abstraction and state transition. The overview of the Encoder is shown in Figure [2](https://arxiv.org/html/2606.30534#S2.F2 "Figure 2 ‣ 2.2 Architecture ‣ 2 Orca ‣ Orca: The World is in Your Mind"). It uses a native pre-trained VLM (qwen35) aligned with the language and vision spaces. Given visual and language signals, Orca learns the world latent through unconscious learning and conscious learning.

The input of unconscious learning is a certain frame v_{t} of the video V, and the output is the prediction latent \hat{v}^{l}_{t+1} of the next adjacent frame. After passing through the VLM, v_{t} will be used to obtain the predicted \hat{v}^{l}_{t+1} through two layers of MLP. The ground truth of the next adjacent frame v_{t+1} will only pass through the frozen vision encoder to obtain a latent representation v^{l}_{t+1}, and then be teacher forced with the prediction latent \hat{v}^{l}_{t+1}. This part completes the 1) Observation-only state transition in Figure [2](https://arxiv.org/html/2606.30534#S2.F2 "Figure 2 ‣ 2.2 Architecture ‣ 2 Orca ‣ Orca: The World is in Your Mind").

To support conscious learning, we divide the video into multiple segments based on meaningful events. Each event contains a video segment and a corresponding instruction description, as shown in Section [3.1.2](https://arxiv.org/html/2606.30534#S3.SS1.SSS2 "3.1.2 Pre-Training Data ‣ 3.1 Pre-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). The input of conscious learning also includes a frame v_{t} from V, along with an instruction description e_{t+\Delta} of the adjacent (next or previous) event, where v_{t} belongs to a certain event. The output is the prediction latent \hat{v}^{l}_{t+\Delta} of a random sample associated with the event e_{t+\Delta}. This part completes the 2) Event-conditioned state transition in Figure [2](https://arxiv.org/html/2606.30534#S2.F2 "Figure 2 ‣ 2.2 Architecture ‣ 2 Orca ‣ Orca: The World is in Your Mind"). In addition, the essence of conscious learning is understanding the world. Therefore, we will also input the video V and the related questions l_{q}, and output the corresponding language answers l_{a}. This part completes the 3) VQA response generation in Figure [2](https://arxiv.org/html/2606.30534#S2.F2 "Figure 2 ‣ 2.2 Architecture ‣ 2 Orca ‣ Orca: The World is in Your Mind"). Ultimately, the world latent space is obtained by the two learning paradigms.

##### Decoder.

The learned latent space is read out by the modality-specific Decoder to extract multi-modal information. Since the decoder is not the focus of this section, its details will be shown in Section [3.2](https://arxiv.org/html/2606.30534#S3.SS2 "3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind").

## 3 Training

Orca is trained in two stages. The pre-training stage learns the world latent through large-scale visual and language data. In the downstream post-training stage, the Orca’s backbone is frozen. Only modality-specific readout modules are trainable to obtain language, vision, and action information.

### 3.1 Pre-Training

#### 3.1.1 Pre-Training Recipe

Orca pre-training instantiates world-state modeling with three objectives: 1) observation-only state transition, 2) event-conditioned state transition, and 3) VQA response generation. The two state-transition objectives are implemented through a set of learnable query vectors, while 3) VQA response generation is optimized through the language modeling (LM) head of the backbone.

##### Learning Objectives.

We instantiate pre-training with the three objectives. 1) observation-only state transition and 2) event-conditioned state transition are implemented with learnable queries in the input of the VLM backbone. The input is: <visual token>, <Query 1>, <Instruction>, <Query 2>. Note that all learnable queries are trained from scratch. The specific implementations are shown in Appendix [C.1.2](https://arxiv.org/html/2606.30534#A3.SS1.SSS2 "C.1.2 Query-Based Implementation ‣ C.1 Pre-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

1.   1) Observation-only state transition. This objective forms unconscious learning. Given v_{t}, Orca takes v_{t} together with the <Query 1>q_{1}. The last-layer hidden state of q_{1} is passed through two layers of MLP to predict \hat{v}^{l}_{t+1}. The ground truth v^{l}_{t+1} is obtained through the frozen vision encoder. Continuous videos provide dense supervision, allowing the model to capture naturally occurring world dynamics such as motion, occlusion, object interaction, and scene changes.

2.   2) Event-conditioned state transition. This objective forms conscious learning with language. Given v_{t}, <Query 1>q_{1}, e_{t+\Delta}, and <Query 2>q_{2}, the last-layer hidden state of q_{2} is passed through the two layers of MLP to predict \hat{v}^{l}_{t+\Delta}. The ground truth v^{l}_{t+\Delta} is also obtained through the frozen vision encoder. e_{t+\Delta} describes an event, a task intention, or a causal premise.

3.   3) VQA response generation. This objective provides another path for common sense in conscious learning. Given V and l_{q}, Orca produces l_{a} with the standard next-token prediction loss.

The first two objectives are supervised in the latent space of the vision encoder. This design focuses on pre-training for state modeling rather than pixel-level reconstruction. The last objective uses the LM head. Given V and l_{q}, the LM head predicts l_{a} with the standard next-token prediction loss.

##### Training Components.

The full pre-training loss combines the three components as:

\mathcal{L}=\lambda_{\mathrm{obs}}\mathcal{L}_{\mathrm{obs}}+\lambda_{\mathrm{evt}}\mathcal{L}_{\mathrm{evt}}+\lambda_{\mathrm{vqa}}\mathcal{L}_{\mathrm{vqa}},(2)

where, \lambda_{\mathrm{obs}}, \lambda_{\mathrm{evt}}, and \lambda_{\mathrm{vqa}} are weighting coefficients that balance the contributions of the two objectives. Here, \mathcal{L}_{\mathrm{obs}} corresponds to unconscious learning from naturally occurring visual transition. \mathcal{L}_{\mathrm{evt}} and \mathcal{L}_{\mathrm{vqa}} correspond to conscious learning through language-specified transitions and common sense. \mathcal{L}_{\mathrm{evt}} uses the ground truth latent of a frame v^{l}_{t+\Delta} in the adjacent event to perform teacher forcing on the predicted latent \hat{v}^{l}_{t+\Delta} under the constraint of e_{t+\Delta}. \mathcal{L}_{\mathrm{vqa}} represents the standard VQA loss. Given a visual information V and a question l_{q}, Orca learns to produce the target response l_{a}. The details of the sampling ratio, loss coefficients, and optimization settings are provided in Appendix [C.1](https://arxiv.org/html/2606.30534#A3.SS1 "C.1 Pre-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

#### 3.1.2 Pre-Training Data

##### Data Organization.

The three collections provide complementary supervision for learning world states and their transitions. The pre-training data is shown in Figure [3](https://arxiv.org/html/2606.30534#S3.F3 "Figure 3 ‣ Data Organization. ‣ 3.1.2 Pre-Training Data ‣ 3.1 Pre-Training ‣ 3 Training ‣ Orca: The World is in Your Mind").

![Image 3: Refer to caption](https://arxiv.org/html/2606.30534v1/x3.png)

Figure 3: Overview of pre-training data. Orca’s pre-training data includes video, event, and VQA data. A. Video Data supports 1) Observation-only state transition, A. Video Data and B. Event Data support 2) Event-conditioned state transition, and C. VQA Data supports 3) VQA response generation.

1.   A. Video Data is built from visual signals and covers four types of real-world observations: ego-centric interaction, exo-centric manipulation, action-free robot execution, and natural dynamics. Ego-centric interaction captures first-views experience during physical interaction, exo-centric manipulation provides third-views of object-centered changes, action-free robot execution records embodied action in robotic environments, and natural dynamics describes naturally evolving scenes. These data support 1) observation-only state transition and 2) event-conditioned state transition.

2.   B. Event data is derived from A. Video Data through multi-level event segmentation and language annotation. Coarse events describe the main steps of a temporal process, while fine-grained events capture the shorter state transitions within each step. Each segmented event is paired with a caption that specifies the transition. This data supports 2) event-conditioned state transition.

3.   C. VQA Data is constructed from language signals and video data, which teaches Orca to describe and interpret observed world states. This collection supports 3) VQA response generation.

Across these collections, data construction is grounded in the real world. The video data is built from real-world videos, while event and VQA data are constructed on top of these observations to describe state transition, physical relations, spatial configurations, behavioral intentions, and causal consequences. The existing data includes 125K hours of general video data, 160M of event annotations, and 11.5M of general VQA data. In this version, only one-tenth of the video data are used. The remaining data will be used in Orca’s subsequent version iterations.

### 3.2 Downstream Post-Training

After pre-training, Orca is connected to downstream readout interfaces for language, vision, and action. Note that our goal is to explore, in essence, whether the learned latent is effective for downstream tasks. So, Orca’s backbone is always frozen, and only the corresponding readout modules are trainable. In other words, if Orca is intended to support vision tasks, it only trains the downstream image modules; if it is intended to serve embodied tasks, it only trains the action modules. Through these readouts, Orca exposes the latent as text, image, and action. Figure [4](https://arxiv.org/html/2606.30534#S3.F4 "Figure 4 ‣ 3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind") provides an overview of the readout architectures.

![Image 4: Refer to caption](https://arxiv.org/html/2606.30534v1/x4.png)

Figure 4: Downstream readout architectures.To language reuses the LM head for text readout. To vision only trains an MLP adaptor and LoRA on top of a frozen SD3.5 to readout images. To action trains an MLP adaptor and a DiT-based Action Expert from scratch. Action Expert receives the latent, robot proprioception state, and noisy action to generate action chunks. The specific settings are shown in Appendix [C.2](https://arxiv.org/html/2606.30534#A3.SS2 "C.2 Downstream Readout Post-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

#### 3.2.1 To Language: Text Generation

As shown in Figure [4](https://arxiv.org/html/2606.30534#S3.F4 "Figure 4 ‣ 3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind")(a). Given a visual observation and an instruction, Orca produces the response through LM head, without attaching an additional decoder. It expresses Orca’s latent in natural language.

#### 3.2.2 To Vision: Image Prediction

##### Vision Readout Recipe.

As shown in Figure [4](https://arxiv.org/html/2606.30534#S3.F4 "Figure 4 ‣ 3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind")(b), the vision readout maps the latent to a pixel-level image. Since Orca focuses on the encoder, the decoder uses a pre-trained model (sd35) to show the effectiveness of latent. The latent is passed through an MLP adaptor and then used as a path input of a Stable Diffusion 3.5(sd35). The ground truth image with Gaussian noise is fed into another path of SD3.5 through a frozen VAE. The final predicted image is obtained through multi-step denoising. During this module training, only the MLP adaptor and the LoRA parameters are trainable.

##### Image Prediction Data.

This readout training uses paired current and target frames sampled from A. Video Data in Figure [3](https://arxiv.org/html/2606.30534#S3.F3 "Figure 3 ‣ Data Organization. ‣ 3.1.2 Pre-Training Data ‣ 3.1 Pre-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). Given the image and an instruction, Orca first produces the latent of the target frame using frozen Orca, and then the latent is input into the image readout module to obtain the image.

#### 3.2.3 To Action: Action Generation

##### Action Readout Recipe.

As shown in Figure [4](https://arxiv.org/html/2606.30534#S3.F4 "Figure 4 ‣ 3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind")(c). The Action Expert is a DiT-based model with flow-matching loss, and it is trained from scratch. Action Expert receives the noisy action with time embedding and the proprioception. The latent of q_{1} is processed by the MLP adaptor and input as a condition into the Action Expert. Through multi-step denoising, the final Action Chunk used to control the robot manipulation is obtained. During this module training, only the MLP adaptor and Action Expert are trainable.

##### Embodied Action Data.

This readout training uses action-labeled data consisting of 5 tasks collected by the dual-arm wheeled humanoid robot. Note that Action Expert has only seen 200 trajectories, instructions, visual information, and proprioception for each task. The details are shown in Section [4.2.3](https://arxiv.org/html/2606.30534#S4.SS2.SSS3 "4.2.3 Comparison on Action Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind").

### 3.3 Infrastructures

Orca’s infra uses the self-developed FlagScale (flagscale) and makes the following improvements:

1.   1) FlagScale training framework. We use FlagScale and rebuild the Orca training with FSDP2, enabling more flexible parameter sharding, better memory control, and stable training.

2.   2) Memory-efficient loss and recompute. We adopt Chunked Cross-Entropy Loss to avoid materializing full logits during loss computation, and further apply activation recomputation to trade moderate computation overhead for substantial memory savings, enabling larger batch sizes.

3.   3) Communication scheduling. We introduce forward/backward pre-fetching to overlap FSDP all-gather communication with computation, and remove unnecessary FSDP sharding for visual blocks.

With these optimizations, training throughput increases from 0.66 to 2.91 Samples/Sec/GPU, achieving approximately a 4.4\times acceleration compared to the StarVLA (StarVLA) commonly used in the embodied community. Optimization details and results are shown in Appendix [D](https://arxiv.org/html/2606.30534#A4 "Appendix D Infrastructure ‣ Orca: The World is in Your Mind").

## 4 Evaluation

### 4.1 Effectiveness and Scaling Behavior

Before giving the downstream-specific results, we first explore whether Orca’s core hypotheses hold. As presented in the introduction, Orca is designed to learn a world latent space through next state prediction, and this latent space is expected to support downstream readouts for understanding, prediction, and intervention. Therefore, we evaluate the Orca paradigm by answering two questions:

1.   \cdot Question 1.1: Is Orca’s learning paradigm effective as the model size and data scale up?

2.   \cdot Question 1.2: Can a stronger latent by pre-training improve downstream readout performance?

#### 4.1.1 Loss of Proposed Learning Paradigm

![Image 5: Refer to caption](https://arxiv.org/html/2606.30534v1/x5.png)

Figure 5: Loss of model and data scaling.

To answer Question 1.1, we first performed experiments with model sizes and data scaling, and the loss curves are shown in Figure [5](https://arxiv.org/html/2606.30534#S4.F5 "Figure 5 ‣ 4.1.1 Loss of Proposed Learning Paradigm ‣ 4.1 Effectiveness and Scaling Behavior ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). The horizontal axis represents the amount of pre-trained video data (the unit is hours); the vertical axis represents the total loss, calculated by Equation [2](https://arxiv.org/html/2606.30534#S3.E2 "Equation 2 ‣ Training Components. ‣ 3.1.1 Pre-Training Recipe ‣ 3.1 Pre-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). The green and the purple lines represent the trends of 0.8B and 4B model sizes, as the data scaling. The total loss has been on a downward trend.

Based on Figure [5](https://arxiv.org/html/2606.30534#S4.F5 "Figure 5 ‣ 4.1.1 Loss of Proposed Learning Paradigm ‣ 4.1 Effectiveness and Scaling Behavior ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), we obtained Answer 1.1:

1.   \cdot Answer 1.1: Orca’s learning paradigm is effective and scalable as the model size and data increase.

The total loss of Orca decreases as the pre-training data scale up, and the larger Orca achieves a lower objective loss than the smaller one. This trend suggests that Orca provides an effective learning paradigm for building world latent. Orca does not converge quickly, but rather continuously benefits from more data and larger model sizes. Its loss curve continues to show a significant downward trend, further demonstrating its scalability.

#### 4.1.2 Relationship between latent and downstream readout performance

![Image 6: Refer to caption](https://arxiv.org/html/2606.30534v1/x6.png)

Figure 6: Scaling behavior on downstream readouts performance.

To answer Question 1.2, we performed probe experiments on Orca-0.8B and Orca-4B. We select some checkpoints from the pre-training process and apply them to downstream tasks to see if a strong world latent can lead to strong downstream readout performance. The readout performance curves are shown in Figure [6](https://arxiv.org/html/2606.30534#S4.F6 "Figure 6 ‣ 4.1.2 Relationship between latent and downstream readout performance ‣ 4.1 Effectiveness and Scaling Behavior ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). Light-colored lines represent 0.8B, and dark-colored lines represent 4B. The corresponding points represent probes during pre-training. The horizontal axis is the amount of pre-trained video data, and the vertical axis is the corresponding readout performance.

The downstream readout performance across text generation, image prediction, and action generation. The text generation performance is the average performance on four benchmarks: TemporalBench, MVBench, SWITCH, and 3DRSBench. The details are shown in Section [4.2.1](https://arxiv.org/html/2606.30534#S4.SS2.SSS1 "4.2.1 Comparison on Text Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). The image prediction performance is the average performance of the proposed PRICE-V0.1 benchmark. The details are shown in Section [4.2.2](https://arxiv.org/html/2606.30534#S4.SS2.SSS2 "4.2.2 Comparison on Image Prediction ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). Note that the above are all zero shots. The action generation performance is the average performance on five real-robot out-of-domain tasks. The details are shown in Section [4.2.3](https://arxiv.org/html/2606.30534#S4.SS2.SSS3 "4.2.3 Comparison on Action Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind").

Based on Figure [6](https://arxiv.org/html/2606.30534#S4.F6 "Figure 6 ‣ 4.1.2 Relationship between latent and downstream readout performance ‣ 4.1 Effectiveness and Scaling Behavior ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), we obtained Answer 1.2:

1.   \cdot Answer 1.2: Stronger world latent from pre-training leads to stronger downstream readouts.

Orca’s backbone is frozen during readout post-training. As the pre-training data scale up, text, image, and action readouts all improve. This result shows that Orca’s stronger latent space can enhance downstream readout performance. Surprisingly, no data with action labels was used in pre-training, but in action generation, this paradigm brought gains by relying on video data. This emergent capability may alleviate, to some extent, the problem of low generalization caused by the scarcity of robot data.

### 4.2 Downstream Readout Analysis

Following the above discussion of Question 1.2 and Answer 1.2, we present the quantitative evaluation results of Orca across three downstream tasks: text generation, image prediction, and action generation. Note that we do not construct or use any benchmark-specific training data for these evaluations, nor do we tune Orca on the evaluation benchmarks.

1.   1.
Text Generation. It demonstrates the model’s out-of-distribution (OOD) commonsense reasoning, comprehension capabilities, and high-level cognitive abilities.

2.   2.
Image Prediction. It visualizes this latent cognitive capability through OOD state transitions.

3.   3.
Action Generation. It executes the generated actions in real-world OOD scenarios, mapping the state transitions to action manipulation.

#### 4.2.1 Comparison on Text Generation

To evaluate how state transition modeling enhances abstract reasoning, we conducted text generation assessments on OOD understanding. The details of benchmarks and baselines of the text generation can be seen in Appendix [E.1](https://arxiv.org/html/2606.30534#A5.SS1 "E.1 Text Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

##### Benchmarks.

We evaluate Orca on a complementary suite of benchmarks that probe different aspects of world-state and state-transition understanding: MVBench (MVBench), TemporalBench (cai2024temporalbench), 3DSRBench (ma20253dsrbench), and SWITCH (switch2025).

##### Baselines.

We compare Orca with two categories of baselines:

*   •
World models: V-JEPA 2.1 (V-JEPA-2.1), Emu3 (Emu3), and Emu3.5 (Emu35).

*   •
Vision-language models: Qwen3.5 (qwen35), Gemma 4 (Gemma4), DeepSeek-VL2 (DeepSeek-VL2), MiniCPM-V-4.6 (MiniCPM-o-4.5), and SmolVLM2 (SmolVLM).

##### Results and Analysis.

Based on Table [1](https://arxiv.org/html/2606.30534#S4.T1 "Table 1 ‣ Results and Analysis. ‣ 4.2.1 Comparison on Text Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), Orca achieves the best overall result among the same-size VLMs and the large-size world models, demonstrating the advantages of the proposed learning paradigm.

Table 1: The comparison of the text generation.\uparrow represents the higher value, the better.

Model Size (B)MVBench \uparrow TemporalBench \uparrow 3DSRBench \uparrow SWITCH \uparrow Avg.
World Models (Large size)
V-JEPA 2.1 1 (+LLaMA3-8B)10 75.4 28.5///
Emu3 2 8 35.2 9.5 39.1 38.0 30.4
Emu3.5 34 39.5 9.5 31.3 38.9 29.8
Vision Language Models (Tiny size)
Qwen3.5 0.8 52.7 19.1 21.8 38.8 33.1
Gemma 4 2 32.5 17.1 29.5 39.9 29.8
SmolVLM2 2 48.7 18.4 35.5 32.0 33.7
MiniCPM-V-4.6 2 41.4 21.2 47.7 41.2 37.9
Vision Language Models (Small size)
DeepSeek-VL2 3 40.5 21.0 32.1 35.5 32.3
Gemma 4 4 45.6 20.2 44.8 52.4 40.8
Qwen3.5 4 67.1 25.2 48.1 42.8 46.7
0.8 53.6 22.6 43.4 43.7 40.8
Orca 4 65.3 34.2 52.1 55.6 51.8

*   1
Since V-JEPA 2.1 does not publicly disclose the alignment data and adjusted LLaMA3-8B weights, its results are taken from the original paper (V-JEPA-2.1).

*   2
Emu3 denotes the Emu3-Chat version.

We believe that a key characteristic of world models lies in their ability to construct a unified latent space for the physical world. Such models should not only be able to internalize the natural evolution of environmental dynamics over time, but also accurately predict complex state transitions caused by external interventions and behaviors. We also evaluated the capability dimensions to explore the boundaries. Specifically, we identified four core capability dimensions:

1.   1) State Transition. It focuses on state transitions induced by actions or temporal evolution.

2.   2) Commonsense Reasoning. It evaluates the internalization of social and physical commonsense knowledge, as well as the ability to reason causally.

3.   3) Spatial Relations. It measures the understanding of three-dimensional geometric relationships.

4.   4) Dynamic Motion. It assesses quantitative reasoning over kinematic properties, including velocity, direction vectors, and higher-order motion characteristics.

Table 2: The cross-benchmark general capability comparison of the text generation.

Model State Transition 1 Commonsense Reasoning 2 Spatial Relations 3 Dynamic Motion 4
Qwen3.5-4B 51.86 57.76 54.68 57.03
Orca-4B 64.13(+12.27%)62.95(+5.19%)55.25(+0.57%)65.55(+8.52%)

*   1
644 samples from MVBench and SWITCH.

*   2
1,676 samples from MVBench and SWITCH.

*   3
11,686 samples from 3DSRBench.

*   4
1,736 samples from TemporalBench and MVBench.

By aggregating samples associated with each capability dimension across multiple benchmarks and computing the corresponding average success rates, we obtain a large-scale and benchmark-agnostic evaluation framework, as summarized in Table [2](https://arxiv.org/html/2606.30534#S4.T2 "Table 2 ‣ Results and Analysis. ‣ 4.2.1 Comparison on Text Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). The results of Table [2](https://arxiv.org/html/2606.30534#S4.T2 "Table 2 ‣ Results and Analysis. ‣ 4.2.1 Comparison on Text Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind") demonstrate that:

1.   1) More accurate state transition. Orca predicts future states more accurately and demonstrates a deeper understanding of temporal dynamics.

2.   2) Common-sense and counterfactual reasoning. Orca achieves more reliable common-sense reasoning and counterfactual reasoning through causal alignment of conscious learning.

3.   3) Strong spatial understanding. Orca can capture geometric continuity, reduce spatial inconsistencies, and improve robustness under complex perspectives.

4.   4) Dynamic motion consistency. Orca can better capture temporal continuity and motion inertia.

#### 4.2.2 Comparison on Image Prediction

To visualize the capability of the state transition, we performed a comparison on image prediction. The details of benchmarks and baselines of the image prediction can be seen in Appendix [E.2](https://arxiv.org/html/2606.30534#A5.SS2 "E.2 Image Prediction ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

##### Benchmark.

Our motivation is not to create a painter, but to explore whether the latent possesses the ability to predict future states. So, instead of generating or simulating scenarios, we build a real-world dataset, PRICE-V0.1 (i.e., Prediction of Real-world Interactions with Constraints Evaluation). PRICE-V0.1 benchmark is shown in Appendix [E.2.1](https://arxiv.org/html/2606.30534#A5.SS2.SSS1 "E.2.1 Benchmarks ‣ E.2 Image Prediction ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

##### Metrics.

In PRICE-V0.1, we use Gemini 3.1 Pro (Gemini-3.1-pro), GPT 5.4 (GPT54), Doubao-Seed-2.0-Pro-260215 (doubao-seed-2.0-pro), and open-source Gemma 4-31B (Gemma4) for evaluation. The specific evaluation prompt is shown in the Listing LABEL:lst:evaluator_prompt.

##### Baselines.

We selected recent image generation models with a similar size to Orca as baselines: including OmniGen2 (OmniGen2) (3B VLM + 4B vision decoder), FLUX.1-Kontext (FLUX.1-Kontext) (12B vision decoder), and Flux.2 [klein] (flux2) (4B VLM + 4B vision decoder).

##### Results and Analysis.

Based on Table [3](https://arxiv.org/html/2606.30534#S4.T3 "Table 3 ‣ Results and Analysis. ‣ 4.2.2 Comparison on Image Prediction ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind") and Figure [7](https://arxiv.org/html/2606.30534#S4.F7 "Figure 7 ‣ Results and Analysis. ‣ 4.2.2 Comparison on Image Prediction ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), we obtained two conclusions:

Table 3: The comparison of the PRICE-V0.1. \uparrow represents the higher value, the better. In Avg., a\pm b is avg\pm std. A larger avg and a smaller std value represent a better result. Bold represents the best value.

Model Size (B)Gemini 3.1 Pro \uparrow GPT 5.4 \uparrow Doubao-Seed-2.0 \uparrow Gemma 4-31B \uparrow Avg.
OmniGen2 3+4 24.6 46.8 41.4 45.5 39.6\pm 10.2
FLUX.1-Kontext 12 21.6 46.9 42.7 52.5 40.9\pm 13.5
FLUX.2 [klein]4+4 29.7 64.6 60.0 70.2 56.1\pm 18.1
0.8+2 17.0 48.5 46.0 26.5 34.5\pm 15.3
Orca 4+2 44.0 67.9 61.0 66.3 59.8\pm 10.9
![Image 7: Refer to caption](https://arxiv.org/html/2606.30534v1/x7.png)

Figure 7: Visual comparison of image prediction in the real world.

1.   1) Orca’s learned world latent transfers effectively to image readout. Compared with recent image generation baselines, Orca achieves the best average performance on PRICE and remains competitive across different real-world interaction sources. This indicates that the learned world latent contains predictive information about future visual states under real-world interactions.

2.   2) Orca better predicts interaction-conditioned state changes. As shown in Figure [7](https://arxiv.org/html/2606.30534#S4.F7 "Figure 7 ‣ Results and Analysis. ‣ 4.2.2 Comparison on Image Prediction ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), general image generation baselines suffer from typical flaws, such as the appearance or teleportation of irrelevant objects, hallucinatory human hands, poor instruction adherence, and biases stemming from prior knowledge. Orca better preserves robot morphology, scene and object consistency, contact relationships, and instruction following.

These results suggest that the learned world latent provides useful state-transition information for visual readout, enabling more physically grounded image prediction for real-world interactions.

#### 4.2.3 Comparison on Action Generation

To truly apply state transition modeling capabilities to the real world, we performed the embodied real-robot tasks. The details of benchmarks, metrics, and baselines are shown in Appendix [E.3](https://arxiv.org/html/2606.30534#A5.SS3 "E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

##### Benchmarks.

We used a dual-arm wheeled robot to collect data on five tasks: Take Book, Stacked Bowls, Pull Out Tissue, Stamp, and Scoop Sugar. We performed two OOD settings: environment and object OOD.

##### Metrics.

We report the rule-based scores, which measure key-stage task completion. The rule-based score is shown in Table [E2](https://arxiv.org/html/2606.30534#A5.T2 "Table E2 ‣ E.3.2 Metrics ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind"). We further employ PRM-as-a-Judge series (PRM-as-a-Judge; judge1.5) to provide dense trajectory-level diagnostics.

##### Baselines.

We compare Orca with V-JEPA 2.1 (V-JEPA-2.1), Qwen3.5 (qwen35), and \pi_{0.5}(pi0.5). For V-JEPA 2.1 and Qwen3.5, we connect them to the same Action Expert as Orca, i.e., V-JEPA 2.1 w/ AE and Qwen3.5 w/ AE, so that the comparison reflects the quality of the learned latent for action readout. V-JEPA 2.1 uses the latent as conditions, and Qwen3.5 uses the last hidden state as conditions. The remaining inputs of Action Expert and training steps are consistent with Orca. We also compare with \pi_{0.5} as a strong VLA baseline pre-trained on large-scale robot data.

Table 4: Comparison on action generation.\uparrow represents the higher value, the better, and vice versa. The metrics are trajectory-level diagnostics from PRM-as-a-Judge. Note that the backbones of all methods are frozen, and Action Experts for Orca, V-JEPA 2.1, and Qwen3.5 are trainable from scratch.

Environment OOD Rule-based \uparrow M25 \uparrow 1 M50 \uparrow 1 SR \uparrow 2 MaxP-F \uparrow 3 FNS \uparrow 4 DRR \uparrow 5 SQS \uparrow 6
V-JEPA 2.1 15.2 40 12 0 23.0 13.9 25.8 0.0
Qwen3.5 12.4 26 10 0 18.3 11.2 19.2 0.0
\pi_{0.5}27.6 54 16 2 27.9 17.7 31.5 1.5
Orca 36.6 64 16 4 33.9 19.3 32.9 1.8
Object OOD Rule-based \uparrow M25 \uparrow M50 \uparrow SR \uparrow MaxP-F \uparrow FNS \uparrow RBS \uparrow SQS \uparrow
V-JEPA 2.1 18.8 14 2 0 11.8 6.3 15.2 0.0
Qwen3.5 8.6 10 0 0 7.9 4.0 4.61 0.0
\pi_{0.5}31.2 54 12 8 25.1 12.9 21.9 4.5
Orca 28.2 46 12 8 21.8 10.8 27.7 3.9
Overall Rule-based \uparrow M25 \uparrow M50 \uparrow SR \uparrow MaxP-F \uparrow FNS \uparrow RBS \uparrow SQS \uparrow
V-JEPA 2.1 17.0 27 7 0 17.4 10.1 20.5 0.0
Qwen3.5 10.5 18 5 0 13.1 7.6 11.9 0.0
\pi_{0.5}29.4 54 14 5 26.5 15.3 26.7 3.0
Orca 32.4 55 14 6 27.9 15.1 30.3 2.9

*   1
M25 and M50 are Milestone25% and Milestone50%. They are the proportions of the trajectory reaching 25% and 50%.

*   2
SR is the binary Success Rate. The unit is %.

*   3
MaxP-F is MaxProcess in Failure. It represents the max-level execution process in the failure.

*   4
FNS is Failure Near-Success Score. It measures the progress achieved by failed trajectories before termination.

*   5
DRR is the Drawdown Recovery Ratio. It measures recovery after the largest progress drawdown.

*   6
SQS is the Success Quality Score. It measures the stability, smoothness, and high quality in the success process.

##### Results and Analysis.

Based on Table [4](https://arxiv.org/html/2606.30534#S4.T4 "Table 4 ‣ Baselines. ‣ 4.2.3 Comparison on Action Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), we obtained two conclusions:

1.   1) Orca’s learning paradigm and learned world latent transfers effectively to action readout. Under the from-scratch Action Expert, Orca outperforms Qwen3.5 in all OOD settings, achieving a breakthrough from 0% success rate. It is also comparable to the powerful pre-trained \pi_{0.5}. This indicates that Orca’s learning paradigm has a significant effect on action generation.

2.   2) Orca consistently advances the task and recovers better from execution errors. The metrics show that Orca is more likely to make meaningful intermediate progress during execution, while suffering less from stagnation. Its higher FNS indicates that even when a trajectory eventually fails, Orca can reach later task stages before termination. Its higher DRR suggests that Orca is better at correcting deviations and continuing the task after progress drops. Figure [8](https://arxiv.org/html/2606.30534#S4.F8 "Figure 8 ‣ Results and Analysis. ‣ 4.2.3 Comparison on Action Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind") provides a qualitative case.

![Image 8: Refer to caption](https://arxiv.org/html/2606.30534v1/x8.png)

Figure 8: Recovery after repeated grasp failures. Orca recovers from early spoon-grasp failures and eventually makes progress, while \pi_{0.5} remains unstable with repeated failed attempts. 

These results suggest that Orca produces action trajectories that move further, get stuck less often, and recover more effectively after mistakes.

### 4.3 Ablation

In the current learning paradigm, there are three losses, i.e., 1) Observation-only state transition\lambda_{\mathrm{obs}}; 2) Event-conditioned state transition\lambda_{\mathrm{evt}}; 3) VQA response generation\lambda_{\mathrm{vqa}}. So we ablated the different losses. The ablation results are shown in Table [5](https://arxiv.org/html/2606.30534#S4.T5 "Table 5 ‣ 4.3 Ablation ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"). The results in Table [5](https://arxiv.org/html/2606.30534#S4.T5 "Table 5 ‣ 4.3 Ablation ‣ 4 Evaluation ‣ Orca: The World is in Your Mind") demonstrate that:

Table 5: The ablation results. - represents that it does not work. The first three lines are the average of two values; the last two lines are the average of three values.

\lambda_{\mathrm{obs}}\lambda_{\mathrm{evt}}\lambda_{\mathrm{vqa}}Text Generation Image Prediction Action Generation Average
✓48.4-10.2 29.3
✓✓-58.2 30.9 44.6
✓✓50.5-32.6 41.6
✓✓50.1 54.7 23.0 42.6
✓✓✓51.8 59.8 32.4 48.0

1.   1) The three pre-training objectives provide the most balanced downstream readouts. When \lambda_{\mathrm{obs}}, \lambda_{\mathrm{evt}}, and \lambda_{\mathrm{vqa}} are jointly used, Orca achieves the most balanced performance across text, image, and action readouts. This shows that the three objectives jointly constrain the world latent space from natural dynamics, semantic conditions, and language supervision.

2.   2) Observation-only transition is especially important for action readout. Adding \lambda_{\mathrm{obs}} clearly improves action generation. This suggests that dense natural dynamics from continuous videos provide useful information about temporal changes, object motion, and local physical interactions, which are critical for real-robot action generation.

3.   3) Event-conditioned transition is the key supervision for vision readout. Image prediction requires the model to infer a target state under a semantic condition. \lambda_{\mathrm{evt}} aligns language-described events with visual state transition, enabling Orca to predict instruction- or event-guided target states rather than only modeling unconditional visual dynamics.

4.   4) VQA response generation preserves the language interface and strengthens semantic grounding.\lambda_{\mathrm{vqa}} enables Orca to maintain natural-language readout ability and provides semantic and commonsense constraints for the learned world latent space. When combined with the two state-transition objectives, it further improves the overall balance among different downstream readouts.

## 5 Conclusion

We presented Orca, a world learner built around a world latent space. Rather than being purpose-built for isolated downstream tasks such as question answering, visual frame prediction, or action generation, Orca adopts a fundamentally different modeling paradigm: It first learns an internal representation of world states from multimodal world signals, and subsequently exposes this representation via a suite of dedicated readout interfaces. This design shifts the modeling target from next-token/frame/action prediction toward next-state prediction. Taken together, Orca constitutes an early exploratory milestone on the path toward building general-purpose world foundation models.

##### Discussion & Limitation.

Orca is still an early step toward general world foundation models. We discuss its current boundaries together with the research directions they suggest for the community.

1.   1) Limited multimodal world signals. Orca currently learns mainly from vision and language, which cover only a subset of the multimodal world signals. However, many state transitions are expressed through other sensory or physical signals. For example, whether water is boiling can often be inferred from sound before clear visual changes appear, and tactile or force feedback can reveal contact, slippage, stiffness, or whether an object is firmly grasped. Future world learners should incorporate richer neural and physical signals, such as audio, tactile, force, light, and proprioception, and eventually extend to broader scientific domains to build a more complete world latent space.

2.   2) ViT space supervision. Orca aimed to provide a new learning paradigm that, in all other respects, employed a naive setup, thus using a pre-trained VLM and supervising visual state prediction within a frozen vision encoder. This design simplified the training process. However, this also aligns the learned state space with the semantic space. A general world foundation model should learn a unified world space directly from multi-source signals. These signals should jointly define and constrain the state, rather than relying on any single pre-trained modality space as the supervision target.

3.   3) Model size limited. Due to resource constraints, our current experiments are mainly conducted at the 4B and 0.8B scale. The current scale is insufficient to fully integrate greater world knowledge, more modalities, and more data. We found that the 4B model exhibits a trade-off among language, image, and action readout performance as pre-training progresses, and this trade-off is more pronounced in the 0.8B model. Therefore, although we have created 125K hours of video data and 160M event annotations, the current training only uses one-tenth of the inventory data. This indicates that world learning is not only limited by the data scale, but also requires sufficient model capacity.

4.   4) Vision benchmark limited. Although the proposed PRICE-V0.1 covers multiple real-world data sources, its scale, diversity, and interaction richness are still limited. We hope it can serve as an initial step toward a more comprehensive evaluation of real-world state prediction.

5.   5) Short-horizon transition supervision. The current state-transition supervision is constrained by the event annotation. Most event annotations describe short-horizon, minute-level state transitions, which are suitable for learning local transitions but insufficient for modeling long-term state evolution over hours, days, or even longer horizons.

6.   6) Downstream readout limited. Currently, we have verified that the world latent we have learned is readout language, vision, and action. However, this is far from enough, as information from other fields such as hearing, quantum circuits, and proteins remains an important part of the world.

7.   7) Loss function limited. We use three losses to fully train Orca, but this is not consistent enough for the Next-State-Prediction modeling. A simpler loss and supervision need to be proposed.

8.   8) Embodied task difficulty limited. Our settings are quite stringent, resulting in lower performance. However, it’s undeniable that the current embodiment tasks are still relatively short and easy.

##### Future Works.

We also provided some inspiration for the community, including:

1.   1) More modalities input. The crucial next step is not simply to add more modalities, but to align them to the same underlying state to better constrain state transitions with the laws of physics.

2.   2) Toward native world-state modeling. Native world foundation models can be pre-trained from scratch. To overcome the constraints imposed by a certain existing ViT space or other embedding model spaces, a unified world latent space can be learned directly from multi-source world signals, and a native world model can be trained from scratch.

3.   3) A world model state transition evaluation system. This system constructs a unified evaluation framework for state prediction, intervention response, physical quantifiability, and counterfactual inference, preventing world models from remaining solely at the visual generation level.

4.   4) Model-Data-Evaluation self-evolutionary closed loop. The model autonomously generates interaction trajectories and counterfactual samples, which are automatically evaluated and value-filtered before being fed back into the training system, forming a self-evolutionary closed loop of “data generation—data filtering-training—leap”.

5.   5) Expanding the boundaries of human cognition. Gradually extending from embodied intelligence to complex systems such as AI for science, microscopic quantum mechanics, macroscopic universe, and life sciences, using a unified state transition world representation to support scientific discovery and the expansion of cognitive boundaries.

## 6 Author List

### 6.1 Core Contributors

Yihao Wang*, Yuheng Ji*,\dagger, Mingyu Cao*, Yanqing Shen*, Runze Xiao*

##### Model Pre-Training.

Huaihai Lyu, Senwei Xie, Mingyu Cao*

##### Data Infra.

Euan Liu, Klara Tian, Tianfeng Long, Yichi Zhang, Zhengliang Cai, Ruike Chen, Jifan Zhao, Yanqing Shen*

##### Evaluation.

Ruochuan Shi, Zihan Tang, Jing Lyu, Runze Xiao*

##### Real Robot.

Jing Lyu, Wenxing Tan, Ningbo Zhang, Yangtao Hu, Euan Liu, Yuming Gao, Xiansheng Chen, Junkai Zhao, Runze Xiao*

##### Downstream Post-Training.

Senwei Xie, Huaihai Lyu, Congsheng Xu, Boan Zhu, Ziqi Wang

##### Infrastructure.

Yupu Feng, Qiongqiong Zhang

### 6.2 Contributors

##### Infrastructure.

Yingli Zhao, Yulong Ao

##### Real-Robot Data.

Shaoxuan Xie, You Liu, Guocai Yao

##### Product & Operations.

Leiduo Zhang, Xiaodan Liu, Yunyan Zhang, Yance Jiao

##### Brand Management.

Xinyan Yang, Jiaxing Wei

##### Platform Management.

Xu Liu, Tengfei Pan

##### System Management.

Shaokai Nie, Chunlei Men

### 6.3 Expert Consultant (Ordered by English last name alphabetically)

Sen Cui, Xiaojie Jin, Hongyang Li, Jianlan Luo, Yao Mu, Yunchao Wei, Jun Yan, Hang Zhao, Xiaolong Zheng

### 6.4 Research Leads

Jiaming Li, Yonghua Lin, Tiejun Huang, Zhongyuan Wang🖂, Pengwei Wang🖂

††footnotetext: * Equal Contribution. \dagger Project Lead.🖂 Corresponding Authors: zhongyuan@baai.ac.cn, pwwang@baai.ac.cn
## References

## Appendix

## Appendix A Orca Conception

![Image 9: Refer to caption](https://arxiv.org/html/2606.30534v1/x9.png)

Figure A1: Conceptual illustration of Orca. Existing models are often organized around passive task-driven prediction, including next-token, next-frame, and next-action prediction. Orca shifts the modeling target toward next-state prediction, where multimodal world signals are used to learn a unified world latent. Unconscious learning captures dense natural dynamics from continuous observation, while conscious learning captures meaningful state transitions guided by language, events, and intentions. The learned world latent supports downstream readouts to language, vision, and action.

Figure [A1](https://arxiv.org/html/2606.30534#A1.F1 "Figure A1 ‣ Appendix A Orca Conception ‣ Orca: The World is in Your Mind") summarizes the philosophy behind Orca. We view the development of foundation models as a transition from passive task-driven models to an active world learner. Existing paradigms are often centered around the output they predict: language models perform next-token prediction for semantic understanding, image and video generation models perform next-frame prediction for visual dynamics, and embodied models perform next-action prediction for action affordance. Although these paradigms produce strong task-level capabilities, their modeling targets remain tied to specific modalities.

Orca instead treats the latent state of the world as the central object of modeling. Language, vision, and action are regarded as different observations or readouts of the same underlying world state. This motivates our shift from next-token, next-frame, and next-action prediction to next state prediction. The goal is to learn an internal world representation that can support understanding, prediction, and intervention across different downstream interfaces.

This idea is realized through two complementary learning modes. Unconscious learning absorbs natural dynamics from continuous visual experience, allowing the model to learn dense state transitions and physical regularities without explicit task labels. Conscious learning introduces language, events, instructions, and questions as semantic conditions, allowing the model to learn meaningful state transitions associated with causal explanations and task intentions. Together, they allow Orca to internalize the world as a predictive latent representation.

Once learned, this world latent can be read out through different interfaces: to language for explanation and reasoning, to vision for prediction and imagination, and to action for intervention.

## Appendix B Related Work

We organize related work according to the primary learning objective at the center of each paradigm, rather than by all downstream capabilities a model may exhibit. Under this view, some unified models span multiple capability domains, but are categorized by the dominant training formulation.

### B.1 Self-Supervised Learning

##### Latent World Models.

Latent world models shift predictive learning from reconstructing high-entropy observations to modeling task-related latent. Joint Embedding Predictive Architecture (JEPA)-style work established this path by predicting semantic representations rather than pixels. I-JEPA (I-JEPA), VL-JEPA (VL-JEPA), and MC-JEPA (MC-JEPA) establish joint embedding predictions for images, texts, and videos. The most influential JEPA-style works are the V-JEPA series. V-JEPA (V-JEPA) demonstrates that robust video representations can be learned solely from feature predictions, without pixel reconstruction. V-JEPA 2 (V-JEPA-2) combines large-scale internet video pre-training with action-based understanding, prediction, and planning. This model marks a crucial step towards embodied latent world modeling. V-JEPA 2.1 (V-JEPA-2.1) enhances dense and interaction-sensitive video representations. Recent work has further advanced this paradigm in several complementary directions. LeJEPA (LeJEPA) improves the stability and scalability of JEPA-style training with fewer heuristics. Causal-JEPA (Causal-JEPA) introduces object-level masking and latent interventions, moving latent predictions towards object-centric causal world modeling. LeWorldModel (LeWorldModel) demonstrates that lightweight end-to-end world models can be trained directly from pixels under a stable joint embedding prediction objective. GeoWorld (GeoWorld) further explores the hyperbolic potential dynamics for multi-step visual planning.

##### How Orca differs.

JEPA-style models demonstrate the effectiveness of latent prediction for self-supervised visual representation learning, which is closely related to Orca’s observation-only state transition. Orca starts from a broader world-learning formulation: it abstracts latent world states from multimodal world signals and places state transition at the center of modeling. Specifically, Orca models state transitions under implicit dynamics and explicit semantic conditions, covering both transition directions: predicting future states and backtracking to past states.

### B.2 Next Token Prediction

##### Large Language Models.

Since the development of autoregressive large language models (DeepSeek-R1; Llama-2), recent representative works have further pushed the paradigm along several directions. LLaMA 3.1 (llama3.1) scales dense models to stronger general reasoning and instruction following. DeepSeek-V4 (DeepSeek-V4) developed large-scale Mixture-of-Experts (MoE) models toward cost-effective million-token contexts. Qwen3 (Qwen3) explores hybrid reasoning within a unified framework. Kimi K2 (Kimi-K2) and GLM-5 (GLM-5) strengthen agentic language modeling. The former emphasizes tool-oriented intelligence, and the latter focuses on long-horizon agentic engineering. MiniMax-M2.7 (MiniMax-M2.7) investigates self-evolving for real-world productivity. Phi-4-reasoning (Phi-4-reasoning) shows the effectiveness of high-quality reasoning supervision in dense models. These works advance “next token prediction” as a strong scalable approach for language intelligence.

##### Multimodal Large Language Models.

In the context of multimodal environments, many works have emerged. These include instruction-tuned visual language models, native multimodal foundation models, and agents. LLaVA (llava) pioneered a widely adopted approach to connect vision encoders to large language models. It leverages multimodal instruction tuning to achieve general visual language understanding. Gemini 3.1 (Gemini-3.1-pro) enhanced multimodal reasoning, agent usage, and long context processing capabilities. The latest Qwen series (Qwen3VL; qwen36_35b_a3b) further strengthens visual perception and reasoning, spatial and video dynamic understanding capabilities, and formally moves towards native multimodal large models. GPT-5.4 (GPT54) extends cutting-edge multimodal systems to specialized knowledge work, native computer applications, and agent usage. Gemma 4 (Gemma4) emphasizes cutting-edge multimodal intelligence on the device, supporting image, text, and audio input as well as long context processing. Kimi K2.5 (KimiK2.5) developed multimodal models toward visual agentic intelligence by jointly optimizing text and vision, and introducing Agent Swarm, which decomposes complex tasks into heterogeneous sub-problems for concurrent execution. LLaMA 4 (llama4) introduces a hybrid expert and native multimodal generative model, while Mistral Medium 3.5 (Mistral-Medium-3.5) integrates instruction tracking and inference, and is equipped with a visual encoder trained for different image sizes and aspect ratios. The MLLM paradigm has also been extended toward embodied reasoning and robotic manipulation. RoboBrain series (RoboBrain; RoboBrain2.0; reasonrft) proposes an MLLM-based robotic brain model that integrates general multimodal data with robot-specific supervision. These models improve multimodal understanding and agentic interaction capabilities.

The unified multimodal models also begin to blur the boundary between token prediction and frame prediction. For example, Emu3 (Emu3) and Emu3.5 (Emu35) unify multimodality under the “next-token-prediction” paradigm. Emu3.5 significantly optimizes the slow image generation speed and poor performance of this autoregressive paradigm. BAGEL (BAGEL) follows the next-token-prediction paradigm and uses a MoT (MoT) architecture. It exhibits emergent capabilities such as image generation, image editing, and future frame prediction. Janus-Pro (Janus-Pro) deploys a unified autoregressive Transformer architecture and decouples the visual encoding path for multimodal understanding and generation. Cosmos 3 (Cosmos3) is an omnimodal world model for Physical AI. It jointly processes and generates language, image, video, audio, and action sequences within a unified MoT architecture.

##### How Orca differs.

Next-token models organize knowledge and reasoning through autoregressive language modeling. Orca uses language as an explicit semantic condition for state transition: language can specify events, task intentions, and causal premises that guide how the current state transitions toward a target state. Meanwhile, VQA response generation preserves the language interface and strengthens the commonsense and semantic grounding of the learned world representation.

### B.3 Next Frame Prediction

##### Image Generation Models.

From a macro perspective, the representative image generation models can be viewed as frame-level prediction models. These models map language or multimodal conditions to target visual observations, thus extending prediction from the token space to the visual frame space. Nano Banana Pro (nanobananapro) boasts powerful multilingual text rendering, infographic creation, and search-based visualization capabilities. GPT Image 2 (ChatGPT-Images-2.0) extends the image generation product line to native text and image model interfaces, supporting high-quality image generation and editing. Qwen-Image (Qwen-image) uses the MMDiT (SD3) to achieve complex text rendering and precise image editing. FLUX.2 (flux2) drives the development of professional-grade image generation through high editing consistency, powerful cue tracking, multi-reference control, and real-time network context-based generation. Overall, these models significantly advance the next frame towards higher fidelity, instruction tracking, and image editing.

##### Video Generation Models.

Video generation works have expanded frame-level prediction from static visual observation to temporally coherent visual sequences (videoworld; VideoWorld-2; cognitive_map). Seedance 2.0 (seedance2.0) supports text, image, audio, and video inputs and possesses powerful reference-based generation and editing capabilities. Sora advances text-to-video generation to longer, higher-quality videos and attempts to understand and simulate the physical world of motion. Cosmos-Predict 2.5 (cosmospredict2.5) unifies “Any2World” into a single framework, aiming to support pixel-level world modeling. Wan2.1 (wan2.1) provides a comprehensive set of diffusion transform-based video foundational models. Overall, these models significantly improve temporal coherence, controllability, and multimodal conditional effectiveness.

##### How Orca differs.

Image and video generation models are often regarded as world models because they can synthesize coherent and visually appealing frames. Orca’s goal is not to create a painter, but to model whether a target state follows the physical constraints and interaction process of the real world. Therefore, Orca emphasizes action execution, scene consistency, physical plausibility, scene and object consistency, contact relationships, and instruction following in interaction-conditioned state transitions.

### B.4 Next Action Prediction

##### Vision Language Action Models.

Vision Language Action (VLA) models, an architecture in embodied intelligence, provide a feasible path to improve generalization and multi-task learning capabilities (manipulation_survey; bai2026latentreasoningvla; lyu2026general; lyu2026last; liu2026pi_0). OpenVLA (OpenVLA), which first presented an open-source VLA model built on a pre-trained VLM, showing strong cross-embodied general manipulation capabilities after training on large-scale robot data. \pi_{0.5}(pi0.5) builds upon \pi_{0}(pi0) by employing a collaborative training method based on heterogeneous data, including multiple robots, subtasks, and network data. It improves generalization capabilities in open worlds. \pi_{0.7}(pi0.7) uses task descriptions, generated sub-target images, and episode metadata to advance the general robot foundation model further. GR00T (N1 (GR00TN1) to N1.7 (GR00TN1.7)) gives a foundation model for general-purpose humanoid robots, achieving better performance in dual-arm and mobile manipulation tasks. VLA-Adapter (VLA-Adapter) explores which information in VLM is more conducive to action generation, and its convergence scheme achieves better performance on a tiny backbone than large-scale VLAs. SimpleVLA-RL (SimpleVLA-RL) develops an RL framework for VLA, improving long-horizon planning and generalization capabilities under limited demonstration, and surpassing supervised fine-tuning models (han2026dexhil). VLA-RFT (VLA-RFT) is the first work to use a world model for post-training a VLA model. It treats the world model as a simulator and provides dense validation rewards.

##### Video Action Models.

Some researchers argue that using a static VLM as the backbone increases the learning burden of the action expert because it needs to model both visual dynamics and control information simultaneously. To alleviate this problem, some works attempt to introduce visual dynamics modeling capabilities from video generation models to reduce the learning difficulty of the action expert. VPP (VPP) is an early representative work in this direction, learning general robot policies by combining implicit inverse dynamics models with predictive visual representations extracted from video models. UVA (UVA) achieves efficient action inference by learning a shared video-action latent with a decoupled diffusion head and combining forward/backward dynamics to jointly optimize observations and action prediction. Mimic-video (mimic-video) combines a video model and an action decoder, demonstrating strong generalization ability and sample efficiency. Cosmos-Policy (cosmos-policy) adapts the pre-trained Cosmos-Predict (cosmospredict2.5) into a robot policy through single-stage post-training. This model predicts future states and value functions for planning.

##### World Action Models.

With the recent surge in interest in world models, some embodied models have begun to jointly model action and future world states. Motus (motus), based on a MoT architecture, constructs a unified latent action world model, fusing understanding, video generation, and action experts. DreamZero (DreamZero) constructs a world action model as a zero-shot policy based on a pre-trained video model, achieving real-time closed-loop manipulation by predicting future observations and actions. GigaWorld-Policy (GigaWorld-Policy) proposes an efficient, action-centric world action model. This model decouples action prediction from video generation, improving inference efficiency while preserving visual dynamic supervision. Being-H0.7 (Being-H0.7) proposes a latent world-action model that connects action prediction and world modeling through a compact latent inference space, injecting future-aware inference into action generation. VLA-JEPA (VLA-JEPA) and JEPA-VLA (JEPA-VLA) link latent predictive embeddings with VLA and imitation learning.

##### How Orca differs.

VLA and world-action models usually organize embodied learning around action prediction, policy learning, or joint video-action modeling. Orca follows a world-learning-first philosophy: it first learns how scenes and objects change through state-transition modeling, without relying on action labels during pre-training. By building a stronger world representation of temporal changes, object motion, and local physical interactions, Orca provides a more general foundation that can adapt more efficiently to embodied tasks under limited robot data and OOD settings.

## Appendix C Training Settings

This appendix provides implementation details for the training procedure described in Section [3](https://arxiv.org/html/2606.30534#S3 "3 Training ‣ Orca: The World is in Your Mind").

### C.1 Pre-Training Settings

#### C.1.1 Pre-Training Objective Definitions

This section specifies the loss definitions used for Orca pre-training. The pre-training objective contains three terms: 1) observation-only state transition\mathcal{L}_{\mathrm{obs}}, 2) event-conditioned state transition\mathcal{L}_{\mathrm{evt}}, and 3) VQA response generation\mathcal{L}_{\mathrm{vqa}}. 1) observation-only state transition and 2) event-conditioned state transition are supervised by visual latent extracted by the frozen vision encoder from the VLM backbone, and 3) VQA response generation is supervised with the standard next-token prediction. For the first two state transitions, Orca matches the predicted latent to the ground truth latent extracted by the frozen vision encoder. \hat{v}^{l} and v^{l} denote the predicted and ground truth latent at the visual-token positions. We use the latent matching:

\ell_{\mathrm{lat}}(\hat{v}^{l},v^{l})=0.1\,\|\hat{v}^{l}-v^{l}\|_{2}^{2}+0.9\left(1-\frac{\langle\hat{v}^{l},v^{l}\rangle}{\|\hat{v}^{l}\|_{2}\|v^{l}\|_{2}}\right).(C-1)

1.   1) Observation-only state transition.v^{l}_{t+1} is the latent of the next frame. The loss is:

\mathcal{L}_{\mathrm{obs}}=\mathbb{E}\left[\ell_{\mathrm{lat}}\left(\hat{v}^{l}_{t+1},v^{l}_{t+1}\right)\right].(C-2)

1.   2) Event-conditioned state transition. The language specifies whether the current state should be mapped toward an adjacent (earlier or later) event state. Accordingly, Orca predicts the visual latent in the previous event selected by the previous-event condition and the visual latent in the next event selected by the next-event condition. The event-conditioned loss averages the latent-matching from the two transition directions:

\mathcal{L}_{\mathrm{evt}}=\frac{1}{2}\mathbb{E}\left[\ell_{\mathrm{lat}}\left(\hat{v}^{l}_{\mathrm{prev}},v^{l}_{\mathrm{prev}}\right)+\ell_{\mathrm{lat}}\left(\hat{v}^{l}_{\mathrm{next}},v^{l}_{\mathrm{next}}\right)\right].(C-3)

1.   3) VQA response generation. Orca uses the language modeling head to predict the target answer with the standard next-token prediction loss. This term is denoted as \mathcal{L}_{\mathrm{vqa}}.

The final Orca’s pre-training objective is: \mathcal{L}_{\mathrm{pre}}=0.1\,\mathcal{L}_{\mathrm{obs}}+0.5\,\mathcal{L}_{\mathrm{evt}}+0.4\,\mathcal{L}_{\mathrm{vqa}}. At the data-sampling level, Orca mixes state transition samples and VQA samples with an approximate ratio of 5:1.

#### C.1.2 Query-Based Implementation

We provide the implementation details of the query-based training described in Section [3.1.1](https://arxiv.org/html/2606.30534#S3.SS1.SSS1 "3.1.1 Pre-Training Recipe ‣ 3.1 Pre-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). Note that all queries are trained from scratch. The implementation of queries is shown in Figure [C1](https://arxiv.org/html/2606.30534#A3.F1 "Figure C1 ‣ C.1.2 Query-Based Implementation ‣ C.1 Pre-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

![Image 10: Refer to caption](https://arxiv.org/html/2606.30534v1/x10.png)

Figure C1: The implementation of Queries.

1.   1) Observation-only state transition. Given the current observation v_{t} and <Query 1>q_{1}, Orca predicts the latent \hat{v}^{l}_{t+1} of a temporally next frame. The last-layer hidden state of q_{1} is passed to the visual transition head (two-layer MLP), and the ground truth latent v^{l}_{t+1} is obtained by the frozen vision encoder of VLM backbone.

2.   2) Event-conditioned State Transition. Given v_{t}, q_{1}, an instruction e_{t+\Delta}, and the <Query 2>q_{2}, Orca predicts the latent \hat{v}^{l}_{t+\Delta} of random frame in the instruction-specified target event. e_{t+\Delta} specifies the transition direction and target event, while q_{2} reads out the corresponding instruction-conditioned predictive state. The previous-event \mathcal{L}_{\mathrm{prev}} and next-event directions \mathcal{L}_{\mathrm{next}}, which are calculated \mathcal{L}_{\mathrm{evt}} in Equation [C-3](https://arxiv.org/html/2606.30534#A3.E3 "Equation C-3 ‣ C.1.1 Pre-Training Objective Definitions ‣ C.1 Pre-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

#### C.1.3 Pre-Training Hyperparameters

Table [C1](https://arxiv.org/html/2606.30534#A3.T1 "Table C1 ‣ C.1.3 Pre-Training Hyperparameters ‣ C.1 Pre-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind") reports the main pre-training hyperparameters. The table groups the model-scale settings, optimization settings, and objective-specific settings.

Table C1: Orca pre-training hyperparameters.

Hyperparameter Orca-4B Orca-0.8B
Base VLM Qwen3.5-4B Qwen3.5-0.8B
Backbone hidden size H 2560 1024
Training resources 32 nodes / 256 GPUs 32 nodes / 256 GPUs
State-transition per-GPU batch size 8 8
State-transition gradient accumulation 2 2
VQA per-GPU batch size 4 4
Training steps 10,844 10,844
Approximate video hours 12.5K h 12.5K h
Maximum sequence length 1024 1024
Optimizer AdamW AdamW
Base VLM learning rate 3.5\times 10^{-5}3.5\times 10^{-5}
Visual head 2\times MLP, 2560\!\rightarrow\!20480\!\rightarrow\!2560 2\times MLP, 1024\!\rightarrow\!8192\!\rightarrow\!1024
Visual head learning rate 1.2\times 10^{-4}1.2\times 10^{-4}
Visual encoder / ViT Frozen Frozen
LLM Trainable Trainable
Adam betas[0.9,0.95][0.9,0.95]
Weight decay 1\times 10^{-8}1\times 10^{-8}
Scheduler Cosine with minimum LR Cosine with minimum LR
Warmup steps 200 200
Minimum learning rate 1\times 10^{-6}1\times 10^{-6}
Latent matching loss 0.1\,\mathrm{MSE}+0.9\,\mathrm{Cosine}0.1\,\mathrm{MSE}+0.9\,\mathrm{Cosine}
Observation-only coefficient \mathcal{L}_{\mathrm{obs}}0.1 0.1
Event-conditioned coefficient \mathcal{L}_{\mathrm{evt}}0.5 0.5
VQA coefficient \mathcal{L}_{\mathrm{vqa}}0.4 0.4
Number of queries 256 256

### C.2 Downstream Readout Post-Training Settings

This section provides implementation details for the downstream readout training described in Section [3.2](https://arxiv.org/html/2606.30534#S3.SS2 "3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). The overall readout architecture is illustrated in Figure [4](https://arxiv.org/html/2606.30534#S3.F4 "Figure 4 ‣ 3.2 Downstream Post-Training ‣ 3 Training ‣ Orca: The World is in Your Mind"). Here, we further detail the implementation of the language readout, the SD3.5-based vision readout, and the DiT-based action readout.

#### C.2.1 Language Readout

The language readout does not introduce an additional trainable module. It reuses the language modeling head of the VLM backbone as its interface. Given a visual observation and an instruction, Orca produces the response autoregressively with the LM head. This readout exposes the learned latent through natural language and is used for VQA, event-level interpretation, and causal explanation.

#### C.2.2 Vision Readout

The vision readout maps Orca’s predicted visual latent state into image space. We instantiate this readout with a pretrained Stable Diffusion 3.5 decoder (sd35). During readout training, the VAE and MMDiT weights of SD3.5 are kept frozen, while the MLP adaptor and LoRA(lora) attached to the decoder attention projections are trainable. The learned latent is fed into one path of MMDiT after passing through an MLP adaptor; the target image is denoised, fed into a frozen VAE, and then fed into another path of MMDiT. Finally, the predicted image is obtained through a multi-step denoise.

##### Settings.

The architecture of the MLP adaptor and the main training settings of the SD3.5 vision readout are summarized in Table [C2](https://arxiv.org/html/2606.30534#A3.T2 "Table C2 ‣ Settings. ‣ C.2.2 Vision Readout ‣ C.2 Downstream Readout Post-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind"). The MLP adaptor projects Orca’s visual-state latent into the SD3.5 joint conditioning space, including token-level conditions and an auxiliary pooled condition. During decoder training, the target image is resized to 768\times 768.

Table C2: The vision readout settings.

Item Settings
Architecture
Base image decoder Stable Diffusion 3.5 MMDiT
Condition input Orca’s latent, (64,2560)
Input projection LayerNorm (2560), Linear (2560 \rightarrow 4096)
Residual MLP blocks 4 blocks
Block width 4096 \rightarrow 16384 \rightarrow 4096
Output normalization LayerNorm (4096)
Pooled branch Mean pooling and two-layer MLP to 2048
LoRA target modules Attention projections
Trainable adaptor parameters 556.9M
Training
Frozen modules SD3.5 VAE and MMDiT weights
Trainable modules MLP adaptor and LoRA parameters
Target image size 768\times 768
Global batch size 512
Training steps 200,000
Optimizer AdamW
Adaptor learning rate 1\times 10^{-4}
LoRA learning rate 5\times 10^{-5}
Weight decay 0.01
Scheduler OneCycleLR with cosine annealing
LoRA rank / alpha / dropout 32 / 32 / 0.05

#### C.2.3 Action Readout

The action readout maps Orca’s latent to action chunks to control robot manipulation. It takes Orca’s learned latent, noisy action with time embedding, and robot proprioception as inputs. A DiT-based (dit) Action Expert with flow-matching (flow_matching) loss then predicts a short-horizon action chunk. The action expert uses the following conditions:

1.   1) Latent q_{1}: predictive query states from Orca, providing latent for future state evolution.

2.   2) Noisy action with time embedding: Actions with Gaussian noise, and time embedding added.

3.   3) Proprioception: robot proprioceptive state, including joint and end-effector related information.

##### Settings.

The Action Expert is trained with the flow-matching loss to obtain the action chunks. The ground-truth action chunk is perturbed with Gaussian noise, and the Action Expert predicts the corresponding velocity. The architecture and training settings of the Action Expert are shown in Table [C3](https://arxiv.org/html/2606.30534#A3.T3 "Table C3 ‣ Settings. ‣ C.2.3 Action Readout ‣ C.2 Downstream Readout Post-Training Settings ‣ Appendix C Training Settings ‣ Orca: The World is in Your Mind").

Table C3: The action readout settings.

Item Settings
Architecture
Action expert type DiT-based model with flow-matching loss
DiT blocks 8
Block pattern Interleaved a self attention and a cross attention
Conditions q_{1}, Noisy action, Proprioception
Input embedding dimension 768
Hidden size 1024
Attention heads 12
Action dimension 16
State dimension 16
Action horizon 30
Repeated samples 8
Inference timesteps 4
Position embedding Enabled
Training
Global batch size 128
Training steps 20,000
AMP (Automatic Mixed Precision)True
Gradient clipping norm 1.0
Optimizer AdamW
Action expert learning rate 1\times 10^{-4}
Orca backbone Frozen
Adam betas[0.9,0.95]
Weight decay 1\times 10^{-8}
Scheduler Cosine with minimum LR
Warmup steps 500
Minimum learning rate 1\times 10^{-6}

## Appendix D Infrastructure

Orca training integrates visual embedding, language modeling, future visual-latent prediction, and action-related branches, resulting in higher memory pressure and communication cost than standard VLM training. To support stable and scalable large-scale training, we build the Orca training infrastructure on FlagScale (flagscale) and restructure the training pipeline at the system level. The optimization focuses on three aspects: distributed sharding, memory-efficient execution, and communication-computation overlap. Concretely, we adapt FSDP2 (Fully Sharded Data Parallel), activation recomputation, chunked cross-entropy loss, and forward/backward pre-fetching.

##### FSDP2.

We migrate the training backend from DeepSpeed to FSDP2. FSDP2 supports flexible sharding of parameters, gradients, and optimizer states under different memory budgets and model scales, which improves multi-GPU training efficiency while maintaining training stability. We further enable resharding to release redundant parameter copies after use, reducing peak GPU memory during distributed training. For lightweight visual blocks, we remove unnecessary FSDP sharding to avoid excessive communication and scheduling overhead.

##### Activation Recompute.

We apply activation recomputation to reduce the activation memory footprint. Instead of retaining all intermediate activations, the training process checkpoints selected activation boundaries and reconstructs the required intermediate states during backpropagation. This trades moderate additional computation for substantial memory savings, enabling larger batch sizes and improving overall throughput under memory-constrained settings.

##### Chunked Cross-Entropy Loss.

Memory profiling shows that the cross-entropy computation in the VLM forward stage introduces a significant peak-memory spike under long-sequence and large-vocabulary settings, mainly due to the log-softmax intermediate tensor. We therefore adopt chunked cross-entropy loss, which partitions the token dimension and computes the loss block by block. This avoids materializing the full logits tensor during loss computation and reduces peak memory, leaving more memory budget for larger batch sizes and longer sequences.

##### Forward/Backward Pre-fetching.

Performance analysis shows that FSDP2 all-gather operations can expose communication stalls when parameter aggregation and layer computation are not sufficiently overlapped. We introduce forward/backward pre-fetching to overlap the parameter all-gather for upcoming layers with computation in the current layer. This scheduling reduces GPU idle time caused by communication waits and improves overall device utilization.

Table D1: Training throughput of infrastructure optimizations on H100 GPUs.

Infrastructure Samples/Sec/GPU \uparrow
StarVLA (StarVLA)0.66
FSDP2 baseline 0.97
+ Chunked Cross-Entropy Loss 1.35
+ Activation Recompute 2.86
+ Forward/Backward Pre-fetching (Full Orca)2.91

As shown in Table [D1](https://arxiv.org/html/2606.30534#A4.T1 "Table D1 ‣ Forward/Backward Pre-fetching. ‣ Appendix D Infrastructure ‣ Orca: The World is in Your Mind"), the optimized infrastructure achieves 2.91 samples/sec/GPU on H100 GPUs. This corresponds to a 3.0\times improvement over the FSDP2 baseline of 0.97 samples/sec/GPU and a 4.4\times improvement over the StarVLA (StarVLA) training pipeline.

## Appendix E Evaluation Settings

### E.1 Text Generation

##### Benchmarks.

In terms of text generation, we use the following benchmarks for evaluation:

*   •
MVBench(MVBench) evaluates a model’s general video understanding capabilities through multiple-choice QA tasks, covering action recognition, temporal reasoning, object interaction, and event-level understanding.

*   •
TemporalBench(cai2024temporalbench) evaluates a model’s ability to handle fine-grained temporal dynamics, including action frequency, motion amplitude, and event order. The test uses short video (0-20 seconds) QA tasks and employs Multiple Binary Accuracy (MBA) as the evaluation metric.

*   •
SWITCH(switch2025) evaluates a model’s ability to interact with real-world TCIs (Time-Induced Compatibility Elements). It requires the model to possess common sense and physical understanding, causal prediction capabilities, and the ability to predict and verify operational results in the spatiotemporal dimensions.

*   •
3DSRBench(ma20253dsrbench) evaluates a model’s 3D spatial reasoning capabilities, including reasoning about height, location, orientation, and multiple objects.

##### Baselines.

In terms of text generation, we use the following baselines for evaluation:

*   •
V-JEPA 2.1(V-JEPA-2.1) is a self-supervised video model that learns dense visual representations from images and videos. It serves as a representative latent world-model baseline, emphasizing spatially grounded and temporally consistent visual understanding.

*   •
Emu3(Emu3) tokenizes images, text, and videos into a unified discrete token space and trains a single Transformer with next-token prediction. It provides a native multimodal baseline for both perception and generation.

*   •
Emu3.5(Emu35) extends the next-token prediction paradigm toward native multimodal world modeling. It learns from interleaved vision-language sequences and supports long-horizon multimodal generation and spatiotemporally consistent world exploration.

*   •
Qwen3.5(qwen35) is a native multimodal foundation model with early vision-language fusion. It provides a strong general-purpose VLM baseline for visual understanding, reasoning, long-context modeling, and agentic interaction.

*   •
Gemma 4(Gemma4) is an efficient open multimodal model family supporting text, vision, video, and audio understanding. We use it as a compact yet strong baseline for multimodal reasoning and instruction following.

*   •
DeepSeek-VL2(DeepSeek-VL2) is a Mixture-of-Experts vision-language model that improves high-resolution visual understanding through dynamic tiling and an efficient MoE language backbone. It is included as a strong VLM baseline for visual question answering, OCR, document understanding, and visual grounding.

*   •
MiniCPM-V-4.6(MiniCPM-o-4.5) is an edge-deployment-friendly multimodal model designed for efficient image and video understanding. It introduces compact visual encoding and mixed visual token compression, making it a lightweight baseline for mobile and resource-constrained scenarios.

*   •
SmolVLM2(SmolVLM) is a compact vision-language model series designed for resource-efficient image and video understanding. It is included as a lightweight baseline to evaluate whether small VLMs can capture temporal and spatial dynamics under limited model capacity.

### E.2 Image Prediction

#### E.2.1 Benchmarks

To evaluate the model’s ability to predict state changes in real-world interactive scenarios, we developed PRICE-V0.1 (i.e., Prediction of Real-world Interactions with Constraints Evaluation). This benchmark is an instruction-conditional image-to-image generation task (TI2I). Given an initial state image and an instruction, PRICE requires generating a target state image after the corresponding action is performed. Unlike traditional image editing tasks, PRICE focuses more on whether the model can understand the actual impact of the instruction in the real physical environment and generate state change results that conform to scene constraints and common sense.

PRICE is derived from four real-world robot or first-person perspective interaction datasets: AgiBot-World(Agibot-world), HomeInteract, PE-Video(PE), and PSI-Ego(SynData). HomeInteract is the closed-source general data collected by the dual-arm wheeled robot in the home scene. Each sample consists of three parts: an instruction, an initial state image, and a target state image, as shown in Figure [E1](https://arxiv.org/html/2606.30534#A5.F1 "Figure E1 ‣ E.2.1 Benchmarks ‣ E.2 Image Prediction ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind"). These samples cover a variety of embodied interaction scenarios, including object manipulation, changes in scene state, action-result prediction, and interaction relationships between humans and objects, or between robots and objects.

![Image 11: Refer to caption](https://arxiv.org/html/2606.30534v1/x11.png)

Figure E1: PRICE-V0.1 Examples.

#### E.2.2 Metrics

We use closed-source Gemini 3.1 Pro (Gemini-3.1-pro), GPT 5.4 (GPT54), and Doubao Seed 2.0 Pro doubao-seed-2.0-pro. In addition, to ensure reproducibility, we added the open-source model Gemma 4-31B (Gemma4) as a judge model to score the generated results. The judge model reads the initial state image, the instruction, and the model-generated target state image. It assigns an integer score from 1 to 5 based on the action execution (following the instruction), scene consistency, and physical plausibility, along with the reasoning for the score. A higher score indicates that the generated image closely matches the target required by the instruction. Then, the average of all the scores will be calculated to obtain the percentage, which is the final score. The prompt used for benchmark evaluation is shown in Listing LABEL:lst:evaluator_prompt.

Listing E1: Prompt used for benchmark evaluation.

"You are a practical benchmark evaluator using lenient pass criteria.You will receive two images(an original image and a modified image)along with a specific modification instruction.

Modification instruction:

{instruction}

The first image is the original image.The second image is the modified image.

Score Instruction:Following from 1 to 5(integers only).Score higher when the instruction’s intended outcome is clearly visible.For agent-action instructions,the outcome should look executed–not merely teleported:if a visible person or robot should act,penalize cases where the result appears but the agent’s pose,position,or contact state is essentially unchanged.Allow in-progress or imperfect execution.Minor occlusion or detail loss is fine.

General scoring philosophy:

-Use the full 1-5 range to reflect how well the instruction is followed.

-Minor blur,texture shifts,small artifacts,or partial ambiguity should NOT automatically fail.

Respond with JSON only,no markdown fences:

{

"score":3,

"reasoning":"…"

}"

Specifically, the focus is on the following three aspects. First, the generated image should be in the same scene as the input image, preserving the original environment, viewpoint, and layout of major objects as much as possible. Second, the generated image should accurately reflect the state changes corresponding to the action command, such as the result of an object being moved, opened, picked up, or lifted. Third, the generated image should not contain content that obviously violates the physical laws, such as generating irrelevant objects out of thin air or lacking a reasonable causal relationship in the interaction process. If the state of an object changes, but the posture, position, or contact relationship of the executing subject remains almost unchanged, points will be deducted appropriately. Slight blurring, texture changes, small-scale artifacts, or local ambiguity will not be considered failures.

#### E.2.3 Baselines

In terms of image prediction, we use the following baselines for evaluation:

*   •
OmniGen2(OmniGen2) is a versatile open-source generative model for unified image generation, editing, and in-context generation. It introduces separate readout pathways for text and image modalities, a decoupled image tokenizer, and task-specific data construction pipelines for image editing and in-context generation.

*   •
FLUX.1-Kontext(FLUX.1-Kontext) is a generative flow-matching model for in-context image generation and editing. It takes both text and image inputs as context and supports local editing, global editing, character reference, style reference, and text editing within a unified architecture.

*   •
FLUX.2 [klein](flux2) is an efficient image generation and editing model. It adopts a rectified-flow Transformer architecture and supports text-conditioned generation as well as multi-reference image editing. We include it as a generative baseline to assess the visual synthesis and editing capability of compact world-oriented image models.

### E.3 Action Generation

#### E.3.1 Real-Robot Benchmark

![Image 12: Refer to caption](https://arxiv.org/html/2606.30534v1/x12.png)

Figure E2: Real-robot benchmark. We evaluate the dual-arm wheeled robot on five manipulation tasks and construct OOD settings for environment and object generalization. 

We evaluate action readout on the dual-arm wheeled humanoid real robot with five manipulation tasks: Take Book, Stacked Bowls, Pull Out Tissue, Stamp, and Scoop Sugar. For each task, we collect 200 real-robot trajectories for downstream Action Expert post-training. The benchmark settings are shown in Figure [E2](https://arxiv.org/html/2606.30534#A5.F2 "Figure E2 ‣ E.3.1 Real-Robot Benchmark ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

We construct two types of real-robot OOD settings. For environment OOD, we keep the task objects and instructions unchanged, but vary the scene appearance using three unseen tablecloth/background settings. For object OOD, we replace the task objects or target containers with unseen but semantically related instances. The object OOD settings are summarized in Table [E1](https://arxiv.org/html/2606.30534#A5.T1 "Table E1 ‣ E.3.1 Real-Robot Benchmark ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind").

Table E1: Object OOD settings for real-robot evaluation.

Task Training Instruction Inference Instruction
Take Book Put the book on the bookshelf.Put the cutting board on the kitchen utensil shelf.
Stacked Bowls Stack bowls.Stack boxes.
Pull Out Tissue Take tissue from the tissue box.Take bread from the bread machine.
Stamp Stamp the paper with a regular stamp.Stamp the notebook with a children’s stamp.
Scoop Sugar Scoop sugar into the mug with a spoon.Scoop sugar into the paper cup with a spoon.

#### E.3.2 Metrics

We evaluate real-robot performance from two complementary perspectives. First, we use task-specific rule-based scores. As shown in Table [E2](https://arxiv.org/html/2606.30534#A5.T2 "Table E2 ‣ E.3.2 Metrics ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind"), each task is decomposed into several key stages, and the rule-based score measures the highest completed stage before termination. Second, we adopt PRM-as-a-Judge (PRM-as-a-Judge) to provide dense trajectory-level diagnostics of progress and execution quality.

Table E2: Scoring criteria for real-robot evaluation. Each task is evaluated within 60 seconds. If the robot becomes locked due to severe collision, or if the object falls and the task can no longer continue, evaluation is stopped. For each task, only the highest achieved score before termination is counted. 

Task Scoring Criteria Point
Take Book 1. The robot arm moves toward the book.10
2. The gripper contacts the book.10
3. The book is pushed to the edge, with more than 2 cm beyond the edge, without falling.20
4. The book is successfully grasped.30
5. The book is moved toward the bookshelf while being grasped.20
6. The book is successfully placed on the bookshelf.10
Stacked Bowls 1. The hand moves toward Bowl 1.10
2. Bowl 1 is grasped.20
3. Bowl 1 is placed stably.10
4. The hand moves toward Bowl 2.10
5. Bowl 2 is grasped.10
6. Bowl 2 is stably stacked into Bowl 1.10
7. The hand moves toward Bowl 3.10
8. Bowl 3 is grasped.10
9. Bowl 3 is stably stacked into Bowl 2.10
Pull Out Tissue 1. Arm A moves toward the tissue box.10
2. Arm A holds the tissue box.20
3. Arm B moves toward the tissue.20
4. Arm B successfully grasps the yellow tissue.40
5. The tissue is placed on the table.10
\triangleright The two arms are scored separately.-
Stamp 1. The robot arm moves toward the stamp.10
2. The stamp is successfully grasped and lifted.30
3. The stamp is moved above the document.10
4. The document is stamped by pressing the stamp.20
5. The stamp is moved above the ink pad.10
6. The stamp is placed stably without toppling.20
\triangleright If the stamp topples, scoring stops.-
Scoop Sugar 1. The hand moves toward the spoon.10
2. The spoon is successfully grasped.20
3. Sugar is scooped with the spoon.20
4. The spoon is moved to the mug; the spoon must be held, but sugar is not strictly required.10
5. The sugar is poured into the mug; the spoon must be held, but sugar is not required.20
6. The spoon is placed back on the right side of the table.20

#### E.3.3 Baselines

We compare Orca with the following baselines in real-robot embodied tasks:

*   •
V-JEPA 2.1(V-JEPA-2.1). The native V-JEPA-AC planner requires a goal image, which is unavailable in our real-robot OOD setting. Therefore, we use the hidden representation of V-JEPA 2.1 as the condition for the same downstream action expert used by Orca.

*   •
Qwen3.5(qwen35). To clarify performance attribution, we use the last-layer hidden state of Qwen3.5 as the condition for the same downstream action expert. This comparison tests whether Orca’s learned world representation provides more useful information for action readout than a general vision-language representation.

*   •
\pi_{0.5}(pi0.5). We use \pi_{0.5} as a strong VLA baseline pretrained on large-scale robot data. This comparison evaluates whether Orca’s learned world representation can provide competitive or complementary benefits under limited real-robot trajectories.

During post-training, the V-JEPA 2.1 backbone, the Qwen3.5 backbone, and the VLM component of \pi_{0.5} are frozen, and only the action expert is trained. For V-JEPA 2.1, Qwen3.5, and Orca, the action experts are configured identically, initialized from scratch, and trained on 200 trajectories per task. We train each task for 20k steps with a global batch size of 128, which gives the best empirical performance among the settings we tested. For \pi_{0.5}, we follow its official post-training configuration and train for 30k steps with a global batch size of 32; we also find this setting to yield the best performance for \pi_{0.5} in our benchmark.

#### E.3.4 Detailed Real-Robot Results

The PRM-as-a-Judge results are used in the main-text analysis, while this appendix provides the detailed task-level rule-based evaluation protocol and results. Table [E3](https://arxiv.org/html/2606.30534#A5.T3 "Table E3 ‣ E.3.4 Detailed Real-Robot Results ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind") provides the OOD results. The rule-based scores report task-level completion under the manually designed scoring criteria.

Table E3: Detailed rule-based results under real-robot OOD settings.

Settings Model Rule-based Score
Book Bowls Tissue Stamp Sugar Average
Environment OOD\pi_{0.5}27 44 32 9 26 27.6
V-JEPA 2.1 24 15 28 6 3 15.2
Qwen3.5-0.8B 1 28 0 0 10 7.8
Qwen3.5-4B 19 27 0 6 10 12.4
Orca-0.8B 23 44 28 27 15 27.4
Orca-4B 25 41 39 62 16 36.6
Object OOD\pi_{0.5}30 46 55 13 12 31.2
V-JEPA 2.1 34 0 44 2 14 18.8
Qwen3.5-0.8B 3 27 0 0 10 8.0
Qwen3.5-4B 6 23 0 0 14 8.6
Orca-0.8B 24 23 65 12 10 26.8
Orca-4B 34 28 59 4 16 28.2

#### E.3.5 Additional Qualitative Visualizations

In addition to the qualitative example shown in the main text, we provide more trajectory visualizations in Figure [E3](https://arxiv.org/html/2606.30534#A5.F3 "Figure E3 ‣ E.3.5 Additional Qualitative Visualizations ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind")-Figure [E7](https://arxiv.org/html/2606.30534#A5.F7 "Figure E7 ‣ E.3.5 Additional Qualitative Visualizations ‣ E.3 Action Generation ‣ Appendix E Evaluation Settings ‣ Orca: The World is in Your Mind"). These examples further illustrate two process-level advantages of Orca: maintaining higher progress even in failed trajectories and recovering from intermediate grasp failures.

![Image 13: Refer to caption](https://arxiv.org/html/2606.30534v1/x13.png)

Figure E3: Failure with higher intermediate progress in Stamp. Orca grasps and transports the stamp toward the ink pad before dropping it near the end, while Qwen3.5 fails to maintain a meaningful stamp grasp and remains at low progress. 

![Image 14: Refer to caption](https://arxiv.org/html/2606.30534v1/x14.png)

Figure E4: Failure with higher intermediate progress in Pull Out Tissue. Orca reaches the tissue-grasping stage and achieves substantially higher intermediate progress, while \pi_{0.5} only approaches the tissue box and fails to grasp the tissue. 

![Image 15: Refer to caption](https://arxiv.org/html/2606.30534v1/x15.png)

Figure E5: Failure with higher intermediate progress in Stacked Bowls. Orca advances through multiple bowl-stacking stages, while \pi_{0.5} repeatedly fails to grasp the bowl and remains at lower progress. 

![Image 16: Refer to caption](https://arxiv.org/html/2606.30534v1/x16.png)

Figure E6: Partial recovery after spoon-grasp failure in Scoop Sugar. Orca retries after failing to grasp the spoon and recovers some lost progress, while Qwen3.5 shakes in place without effective re-grasping. 

![Image 17: Refer to caption](https://arxiv.org/html/2606.30534v1/x17.png)

Figure E7: Recovery through repeated spoon-grasp attempts in Scoop Sugar. Orca makes multiple recovery attempts and eventually grasps the spoon successfully, while JEPA remains largely stagnant with limited task progress. 

## Appendix F More Visualization

### F.1 Cross-Benchmark Capability Analysis for Text Generation

As shown in Section [4.2.1](https://arxiv.org/html/2606.30534#S4.SS2.SSS1 "4.2.1 Comparison on Text Generation ‣ 4.2 Downstream Readout Analysis ‣ 4 Evaluation ‣ Orca: The World is in Your Mind"), we identify a set of generalized, high-level capability dimensions that transcend benchmark boundaries, namely state transition, commonsense reasoning, spatial relations, and dynamic motion. Several representative examples are provided below.

![Image 18: Refer to caption](https://arxiv.org/html/2606.30534v1/x18.png)

Figure F1: Cross-benchmark examples of state transition. This dimension evaluates a model’s understanding of causal temporal dynamics and physical state changes, namely its ability to predict or recognize the evolution of an object from state A to state B. The improvement is particularly evident in tasks involving irreversible physical processes.

![Image 19: Refer to caption](https://arxiv.org/html/2606.30534v1/x19.png)

Figure F2: More cross-benchmark examples of state transition.

![Image 20: Refer to caption](https://arxiv.org/html/2606.30534v1/x20.png)

Figure F3: Cross-benchmark examples of commonsense reasoning. The advantage of Orca is particularly pronounced in complex VQA scenarios that require reasoning beyond the visible scene and inferring hypothetical outcomes.

![Image 21: Refer to caption](https://arxiv.org/html/2606.30534v1/x21.png)

Figure F4: Cross-benchmark examples of dynamic motion. The proposed unconscious learning paradigm enables Orca to naturally acquire temporal continuity and motion inertia, leading to stronger forward simulation capabilities for dynamic object behaviors.

![Image 22: Refer to caption](https://arxiv.org/html/2606.30534v1/x22.png)

Figure F5: Cross-benchmark examples of spatial relations. The results demonstrate strong robustness in scenarios involving complex occlusions and multi-object spatial reasoning.
