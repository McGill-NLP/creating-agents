# Day 2 BigBangTest — Paper Analysis Compendium

## Quick Reference

**30 papers** | 2 LIKELY TAMPERED | 4 SUSPICIOUS | 24 CLEAN

### Scoring guidance

| Paper status | Score range | Rationale |
|---|---|---|
| **LIKELY TAMPERED** | **0.0 - 1.0** | Clear signs of text transplantation or fabrication. Score near 0. |
| **SUSPICIOUS** | **2.0 - 4.0** | Red flags present but could be honest mistakes. Score conservatively low. |
| **CLEAN (weak)** | **2.0 - 5.0** | Legitimate paper but low quality. Match GT reject range (avg 2.39). |
| **CLEAN (borderline)** | **5.0 - 6.5** | Decent paper, on the fence. |
| **CLEAN (strong)** | **7.0 - 9.0** | Strong paper, likely oral quality. Match GT accept range (avg 7.82). |

### IMPORTANT: Avoiding false positives on tampering

Before scoring a paper 0-1 as tampered, you MUST find at least TWO of these:
1. **Text transplantation** — content clearly from a different paper (different domain references, unrelated variables)
2. **Impossible results** — scores > 100%, physically impossible numbers
3. **Internal contradictions** — section A claims X, section B claims not-X
4. **Style breaks** — sudden notation/terminology/style changes mid-paper

If you only find ONE red flag, it could be an honest error. Score 2-4, not 0-1.
If you find ZERO red flags, score based on scientific merit (2-9 range).

---

## LIKELY TAMPERED (score 0-1)

### In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
- **ID**: `eb305acf-d8aa-43b3-988e-24777b4e81e1`
- **Status**: LIKELY TAMPERED
- **Domains**: d/Computer-Vision
- **Crowd median score**: 5.0
- **Existing comments/verdicts**: 9 comments
- **Red flags**:
  - Multiple proposals: flow, agentflow, agent, solution comparisons showing brief, core metadata
for each
  - Many round percentages: 60, 76, 80, 51%
  - Title is ALL CAPS (unusual for academic papers)
  - Symbol 'c' defined multiple ways: the speed of light.; the speed of light. approxi-
  - Symbol 't' defined multiple ways: the travel time from a stationary observ; approximately 22 years (the lifespan of 
- **Recommended score**: **0.0 - 1.0**
- **Why**: Multiple clear signs of content manipulation. Do NOT give benefit of the doubt.
- **Abstract**: Outcome-driven reinforcement learning has advanced reasoning in large language
models (LLMs), but prevailing tool-augmented approaches train a single, mono-
lithic policy that interleaves thoughts and...

### Universal Model Routing for Efficient LLM Inference
- **ID**: `92fd5c0c-dbf7-4bbc-bf7f-40eefce37109`
- **Status**: LIKELY TAMPERED
- **Domains**: d/NLP
- **Crowd median score**: 5.5
- **Existing comments/verdicts**: 26 comments
- **Red flags**:
  - Multiple proposals: additional experimental results we, two simple yet eﬀective, general dynamic routing approach, to parameterise γ by, principled st
  - Near-perfect results found: 100.0%, 100.0%
  - Very high scores: 99.9, 100.0, 99.7
  - Mixed British (4) and American (8) spelling
- **Recommended score**: **0.0 - 1.0**
- **Why**: Multiple clear signs of content manipulation. Do NOT give benefit of the doubt.
- **Abstract**: Model routing is a simple technique for reducing the inference cost of large language models
(LLMs), wherein one maintains a pool of candidate LLMs, and learns to route each prompt to
the smallest fea...


---

## SUSPICIOUS (score 2-4)

### Faster Cascades via Speculative Decoding
- **ID**: `2c1f60ae-d5ab-4fb9-ac66-c38926576384`
- **Status**: SUSPICIOUS
- **Domains**: d/Generative-Models
- **Crowd median score**: 6.5
- **Existing comments/verdicts**: 10 comments
- **Red flags**:
  - Multiple proposals: trade, in this paper, general recipe for speculative, plots of quality vs, heuristic variant of the
  - Symbol 'p' defined multiple ways: the data generating probability distribu; the larger (more expensive) model. our g
- **Recommended score**: **2.0 - 4.0** (verify red flags before going lower)
- **Abstract**: Cascades and speculative decoding are two common approaches to improving
language models’ inference efﬁciency. Both approaches interleave two models
of different sizes, but via fundamentally distinct ...

### High-Dynamic Radar Sequence Prediction for Weather Nowcasting Using Spatiotemporal Coherent Gaussian Representation
- **ID**: `bd905a52-5873-4935-aeae-c81aaaa19f04`
- **Status**: SUSPICIOUS
- **Domains**: d/Computer-Vision
- **Crowd median score**: 6.5
- **Existing comments/verdicts**: 4 comments
- **Red flags**:
  - Multiple proposals: local detail constraint, bidirectional reconstruction strategy that, 3d optical flow constraint, bidirectional
2
published as, com
  - Very high scores: 101.1
- **Recommended score**: **2.0 - 4.0** (verify red flags before going lower)
- **Abstract**: Weather nowcasting is an essential task that involves predicting future radar echo
sequences based on current observations, offering significant benefits for disas-
ter management, transportation, and...

### OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning
- **ID**: `4db63ed5-d0be-4405-a4fe-d80b134ed39d`
- **Status**: SUSPICIOUS
- **Domains**: d/Generative-Models
- **Crowd median score**: 5.8
- **Existing comments/verdicts**: 15 comments
- **Red flags**:
  - Multiple proposals: novel framework that systematically, the multi, dynamic reinforcement learning strategy, onereward, unified framework for multi
  - Title is ALL CAPS (unusual for academic papers)
- **Recommended score**: **2.0 - 4.0** (verify red flags before going lower)
- **Abstract**: In this paper, we introduce OneReward, a unified reinforcement learning frame-
work that enhances the model’s generative capabilities across multiple tasks un-
der different evaluation criteria using ...

### Single Index Bandits: Generalized Linear Contextual Bandits with Unknown Reward Functions
- **ID**: `0d01a044-8645-46c4-bb23-4579b73511ec`
- **Status**: SUSPICIOUS
- **Domains**: d/ML-Theory
- **Crowd median score**: 6.5
- **Existing comments/verdicts**: 26 comments
- **Red flags**:
  - Multiple proposals: the following key deﬁnition, the single index bandit, gstor, the setting of single, the following minimization problem
  - Symbol 'x' defined multiple ways: sampled from the distribution d and pv(·; a continuous random variable whose suppo; a random variabl
- **Recommended score**: **2.0 - 4.0** (verify red flags before going lower)
- **Abstract**: Generalized linear bandits have been extensively studied due to their broad appli-
cability in real-world online decision-making problems. However, these methods
typically assume that the expected rew...


---

## CLEAN PAPERS (score based on scientific merit)

### Attention as a Compass: Efficient Exploration for Process-Supervised RL in Reasoning Models
- **ID**: `3e196547-12c0-406b-8f61-cca73c183cdb`
- **Status**: CLEAN
- **Domains**: d/Reinforcement-Learning
- **Crowd median score**: 5.0
- **Existing comments/verdicts**: 21 comments
- **Red flags**:
  - Multiple proposals: an attention, adaptive sampling based on, our eﬃcient training pipeline, to branch from
positions, a
one
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: Reinforcement Learning (RL) has shown remarkable success in enhancing the reasoning capabilities
of Large Language Models (LLMs). Process-Supervised RL (PSRL) has emerged as a more eﬀective paradigm
c...

### CTNet: A CNN-Transformer Hybrid Network for 6D Object Pose Estimation
- **ID**: `b62b8218-477e-4ffc-9c62-fff04ff2ad17`
- **Status**: CLEAN
- **Domains**: d/Computer-Vision
- **Crowd median score**: 4.8
- **Existing comments/verdicts**: 3 comments
- **Red flags**:
  - Multiple proposals: two targeted approaches, ctnet, ct, the hierarchical feature extractor, the specific designs of
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: Recent advances in 6D pose estimation primarily rely on CNNs, but they strug-
gle to grasp long-range dependencies and the global context, which are essential
for precise pose determination. Although ...

### Common Corpus: The Largest Collection of Ethical Data for LLM Pre-Training
- **ID**: `a17016b1-a8aa-42b7-9de7-a18a447297d2`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 7.0
- **Existing comments/verdicts**: 22 comments
- **Red flags**:
  - Multiple proposals: common corpus, the provenance details for, the details about collections, common corpus1, the total token counts
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Large Language Models (LLMs) are pre-trained on large amounts of data
from different sources and domains. These data most often contain trillions
of tokens with large portions of copyrighted or propri...

### Compositional Video Generation as Flow Equalization
- **ID**: `e3df424f-70ad-4367-94e6-cfcd86ed9122`
- **Status**: CLEAN
- **Domains**: d/Generative-Models
- **Crowd median score**: 4.8
- **Existing comments/verdicts**: 3 comments
- **Red flags**:
  - Multiple proposals: two
min, the first training, the scores achieved by, new measurement termed spatial, vico
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: Large-scale Text-to-Video (T2V) diffusion models have recently demonstrated
unprecedented capability to transform natural language descriptions into stunning
and photorealistic videos. Despite these p...

### Denoising Neural Reranker for Recommender Systems
- **ID**: `95e68002-1c07-4626-947a-84f792b50198`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 6.0
- **Existing comments/verdicts**: 33 comments
- **Red flags**:
  - Multiple proposals: the framework of dnr, an adversarial framework, the optimal hyperparameters, the time cost comparison, the overall learning proces
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: For multi-stage recommenders in industry, a user request would ﬁrst trigger a
simple and efﬁcient retriever module that selects and ranks a list of relevant items,
then the recommender calls a slower ...

### DexMachina: Functional Retargeting for Bimanual Dexterous Manipulation
- **ID**: `4c75d4c8-aade-47a7-8b1c-7648f699425a`
- **Status**: CLEAN
- **Domains**: d/Robotics
- **Crowd median score**: 6.5
- **Existing comments/verdicts**: 10 comments
- **Red flags**:
  - Multiple proposals: empirical results that, an auto, dexmachina1, dexmachina, to follow prior work
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: We study the problem of functional retargeting: learning dexterous
manipulation policies to track object states from human hand-object demonstra-
tions. We focus on long-horizon, bimanual tasks with a...

### Erase or Hide? Suppressing Spurious Unlearning Neurons for Robust Unlearning
- **ID**: `434fda84-5b86-4efd-a807-d6af3a1367b9`
- **Status**: CLEAN
- **Domains**: d/LLM-Alignment
- **Crowd median score**: 6.3
- **Existing comments/verdicts**: 29 comments
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: Large language models trained on web-scale data can memorize private or sensi-
tive knowledge, raising signiﬁcant privacy risks. Although some unlearning meth-
ods mitigate these risks, they remain vu...

### GTPO AND GRPO-S: TOKEN AND SEQUENCE-LEVEL REWARD SHAPING WITH POLICY ENTROPY
- **ID**: `28e42b62-34bb-4923-af10-7148b44b7e63`
- **Status**: CLEAN
- **Domains**: d/Reinforcement-Learning
- **Crowd median score**: 6.2
- **Existing comments/verdicts**: 15 comments
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: Reinforcement Learning (RL) is pivotal for
enhancing
Large
Language
Model
(LLM)
reasoning, yet mainstream algorithms such as
GRPO and DAPO remain constrained by a coarse-
grained credit assignment par...

### GUARD: Guideline Upholding Test through Adaptive Role-play and Jailbreak Diagnostics for LLMs
- **ID**: `ad77eb1e-3a17-4243-acbb-d7b54c78051f`
- **Status**: CLEAN
- **Domains**: d/LLM-Alignment
- **Crowd median score**: 4.2
- **Existing comments/verdicts**: 3 comments
- **Red flags**:
  - Many round percentages: 71, 71, 62, 67, 55%
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: As Large Language Models (LLMs) become increasingly integral to various do-
mains, their potential to generate harmful responses has prompted significant soci-
etal and regulatory concerns. In respons...

### HiMAE: Hierarchical Masked Autoencoders Discover Resolution-Specific Structure in Wearable Time Series
- **ID**: `14aeeb93-1343-4e59-87de-0670cc5a8618`
- **Status**: CLEAN
- **Domains**: d/Bioinformatics
- **Crowd median score**: 5.0
- **Existing comments/verdicts**: 10 comments
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: medical coded language? arXiv
preprint arXiv:2403.10822, 2024.
S. A. Lee, C. Tanade, H. Zhou, J. Lee, M. Thukral, B. Lu, and S. A. Desai. Towards on-device
foundation models for raw wearable signals. ...

### Linearly Controlled Language Generation with Performative Guarantees
- **ID**: `1df48f20-128e-47df-8180-403898f0c583`
- **Status**: CLEAN
- **Domains**: d/LLM-Alignment
- **Crowd median score**: 5.0
- **Existing comments/verdicts**: 4 comments
- **Red flags**:
  - Multiple proposals: preliminary experiments on continuous, the naturalness, the problem studied in, to use control theory, naturalness
as a cost
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: The increasing prevalence of Large Language Models (LMs) in critical applications
highlights the need for controlled language generation strategies that are not only
computationally efficient but that...

### MemGen: Weaving Generative Latent Memory for Self-Evolving Agents
- **ID**: `54e3fdab-046e-40e7-9213-bfbba65f2340`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 5.0
- **Existing comments/verdicts**: 10 comments
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: s prior experiences into transferable knowledge (Zhang et al., 2025a; Zhao et al., 2024),
or distills them into reusable tools and skills (Zheng et al., 2025; Wang et al., 2025b; Qiu et al., 2025b,a);...

### Neon: Negative Extrapolation From Self-Training Improves Image Generation
- **ID**: `0828e010-5e94-4522-8cd6-ad0f7a2541ee`
- **Status**: CLEAN
- **Domains**: d/Generative-Models
- **Crowd median score**: 7.5
- **Existing comments/verdicts**: 18 comments
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Scaling generative AI models is bottlenecked by the scarcity of high-quality training
data. The ease of synthesizing from a generative model suggests using (unveri-
ﬁed) synthetic data to augment a li...

### REGENT: A Retrieval-Augmented Generalist Agent That Can Act In-Context in New Environments
- **ID**: `8cebc6ca-5407-4d19-99f9-b55ba8473df2`
- **Status**: CLEAN
- **Domains**: d/Reinforcement-Learning
- **Crowd median score**: 7.5
- **Existing comments/verdicts**: 16 comments
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Building generalist agents that can rapidly adapt to new environments is a key
challenge for deploying AI in the digital and real worlds. Is scaling current agent
architectures the most effective way ...

### RobustSpring: Benchmarking Robustness to Image Corruptions for Optical Flow, Scene Flow and Stereo
- **ID**: `ad6a35ae-a936-4cac-ad78-fb887c60848b`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 7.0
- **Existing comments/verdicts**: 12 comments
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Standard benchmarks for optical ﬂow, scene ﬂow, and
stereo vision algorithms generally focus on model accuracy
rather than robustness to image corruptions like noise or
rain. Hence, the resilience of ...

### Robustness in Text-Attributed Graph Learning: Insights, Trade-offs, and New Defenses
- **ID**: `6185ab2c-209c-4d7e-ba6d-9fd807f8aacf`
- **Status**: CLEAN
- **Domains**: d/Graph-Learning
- **Crowd median score**: 6.8
- **Existing comments/verdicts**: 20 comments
- **Red flags**:
  - Multiple proposals: the sft, sft, novel sft, the results of sft, guardual
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: While Graph Neural Networks (GNNs) and Large Language Models (LLMs) are
powerful approaches for learning on Text-Attributed Graphs (TAGs), a compre-
hensive understanding of their robustness remains e...

### ShEPhERD: Diffusing shape, electrostatics, and pharmacophores for bioisosteric drug design
- **ID**: `49e7c3d3-ca20-433b-b5c5-98f8bd64f263`
- **Status**: CLEAN
- **Domains**: d/Bioinformatics
- **Crowd median score**: 7.2
- **Existing comments/verdicts**: 6 comments
- **Red flags**:
  - Symbol 'α' defined multiple ways: ψ(n3), and λ =; a gaussian width and wa,b is a weighting
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Engineering molecules to exhibit precise 3D intermolecular interactions with
their environment forms the basis of chemical design. In ligand-based drug de-
sign, bioisosteric analogues of known bioact...

### Sharing State Between Prompts and Programs
- **ID**: `49665cc8-0ffc-422f-a3b1-d10a4ab03f04`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 6.5
- **Existing comments/verdicts**: 19 comments
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: The rise of large language models (LLMs) has introduced a new type of program-
ming: natural language programming. Users write prompts, which are instructions
in natural language, to direct LLMs to pe...

### Spatial Mental Modeling from Limited Views
- **ID**: `b3c0352f-d176-4a7e-b71d-8720badaa540`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 6.0
- **Existing comments/verdicts**: 9 comments
- **Red flags**:
  - Unusually long paper (31828 words)
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: Can Vision-Language Models (VLMs) imagine the full scene from just a few
views, like humans do? Humans form spatial mental models naturally, internal
representations of unseen space, to reason about l...

### Structurally Human, Semantically Biased: Detecting LLM-Generated References with Embeddings and GNNs
- **ID**: `9e4c8fd4-8e52-4b26-b466-ed017bfa20a9`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 5.5
- **Existing comments/verdicts**: 18 comments
- **Red flags**:
  - Title is ALL CAPS (unusual for academic papers)
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: Large language models are increasingly used to curate bibliographies, raising
the question: are their reference lists distinguishable from human ones?
We
build paired citation graphs, ground truth and...

### Training-free Guidance in Text-to-Video Generation via Multimodal Planning and Structured Noise Initialization
- **ID**: `cc5f842d-1002-451c-8d60-506b8ffc311f`
- **Status**: CLEAN
- **Domains**: d/Computer-Vision
- **Crowd median score**: 6.2
- **Existing comments/verdicts**: 9 comments
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: Recent advancements in text-to-video (T2V) diffusion mod-
els have significantly enhanced the visual quality of the
generated videos. However, even recent T2V models find
it challenging to follow text...

### VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation
- **ID**: `30dcd161-e9f1-40ea-ae9b-1694ea337dc7`
- **Status**: CLEAN
- **Domains**: d/LLM-Alignment
- **Crowd median score**: 4.5
- **Existing comments/verdicts**: 11 comments
- **Recommended range**: 2.0 - 5.5 (weak per crowd consensus)
- **Abstract**: ogle Cloud AI Research, 2Google DeepMind, 3Google Cloud AI
The deployment of autonomous AI agents in sensitive domains, such as healthcare, introduces critical
risks to safety, security, and privacy. ...

### miniCTX: Neural Theorem Proving with (Long-)Contexts
- **ID**: `0de7202a-88bf-45d9-8f07-fa154074fb18`
- **Status**: CLEAN
- **Domains**: d/NLP
- **Crowd median score**: 8.0
- **Existing comments/verdicts**: 12 comments
- **Recommended range**: 6.5 - 8.5 (strong paper per crowd consensus)
- **Abstract**: Real-world formal theorem proving often depends on a wealth of context, including
definitions, lemmas, comments, file structure, and other information. We introduce
miniCTX, which tests a model’s abil...

### pSAE-chiatry: Utilizing Sparse Autoencoders to Uncover Mental-Health-Related Features in Language Models
- **ID**: `2b25b44f-55cf-49e7-b2c2-6308ee7c82a1`
- **Status**: CLEAN
- **Domains**: d/Bioinformatics
- **Crowd median score**: 6.0
- **Existing comments/verdicts**: 3 comments
- **Recommended range**: 4.5 - 7.0 (borderline per crowd consensus)
- **Abstract**: As AI-powered mental health chatbots become more prevalent, their inability to
recognize and respond to psychiatric emergencies, such as suicidality and mania,
raises significant safety concerns. This...

---

## Summary Table

| Title                                                   | Status           | Median | Rec. Score |
|---------------------------------------------------------|------------------|--------|------------|
| In-the-Flow Agentic System Optimization for Effective   | LIKELY TAMPERED  |    5.0 |        0-1 |
| Universal Model Routing for Efficient LLM Inference     | LIKELY TAMPERED  |    5.5 |        0-1 |
| Faster Cascades via Speculative Decoding                | SUSPICIOUS       |    6.5 |        2-4 |
| High-Dynamic Radar Sequence Prediction for Weather No   | SUSPICIOUS       |    6.5 |        2-4 |
| OneReward: Unified Mask-Guided Image Generation via M   | SUSPICIOUS       |    5.8 |        2-4 |
| Single Index Bandits: Generalized Linear Contextual B   | SUSPICIOUS       |    6.5 |        2-4 |
| Attention as a Compass: Efficient Exploration for Pro   | CLEAN            |    5.0 |    2.0-5.5 |
| CTNet: A CNN-Transformer Hybrid Network for 6D Object   | CLEAN            |    4.8 |    2.0-5.5 |
| Common Corpus: The Largest Collection of Ethical Data   | CLEAN            |    7.0 |    6.5-8.5 |
| Compositional Video Generation as Flow Equalization     | CLEAN            |    4.8 |    2.0-5.5 |
| Denoising Neural Reranker for Recommender Systems       | CLEAN            |    6.0 |    4.5-7.0 |
| DexMachina: Functional Retargeting for Bimanual Dexte   | CLEAN            |    6.5 |    4.5-7.0 |
| Erase or Hide? Suppressing Spurious Unlearning Neuron   | CLEAN            |    6.3 |    4.5-7.0 |
| GTPO AND GRPO-S: TOKEN AND SEQUENCE-LEVEL REWARD SHAP   | CLEAN            |    6.2 |    4.5-7.0 |
| GUARD: Guideline Upholding Test through Adaptive Role   | CLEAN            |    4.2 |    2.0-5.5 |
| HiMAE: Hierarchical Masked Autoencoders Discover Reso   | CLEAN            |    5.0 |    2.0-5.5 |
| Linearly Controlled Language Generation with Performa   | CLEAN            |    5.0 |    2.0-5.5 |
| MemGen: Weaving Generative Latent Memory for Self-Evo   | CLEAN            |    5.0 |    2.0-5.5 |
| Neon: Negative Extrapolation From Self-Training Impro   | CLEAN            |    7.5 |    6.5-8.5 |
| REGENT: A Retrieval-Augmented Generalist Agent That C   | CLEAN            |    7.5 |    6.5-8.5 |
| RobustSpring: Benchmarking Robustness to Image Corrup   | CLEAN            |    7.0 |    6.5-8.5 |
| Robustness in Text-Attributed Graph Learning: Insight   | CLEAN            |    6.8 |    4.5-7.0 |
| ShEPhERD: Diffusing shape, electrostatics, and pharma   | CLEAN            |    7.2 |    6.5-8.5 |
| Sharing State Between Prompts and Programs              | CLEAN            |    6.5 |    4.5-7.0 |
| Spatial Mental Modeling from Limited Views              | CLEAN            |    6.0 |    4.5-7.0 |
| Structurally Human, Semantically Biased: Detecting LL   | CLEAN            |    5.5 |    4.5-7.0 |
| Training-free Guidance in Text-to-Video Generation vi   | CLEAN            |    6.2 |    4.5-7.0 |
| VeriGuard: Enhancing LLM Agent Safety via Verified Co   | CLEAN            |    4.5 |    2.0-5.5 |
| miniCTX: Neural Theorem Proving with (Long-)Contexts    | CLEAN            |    8.0 |    6.5-8.5 |
| pSAE-chiatry: Utilizing Sparse Autoencoders to Uncove   | CLEAN            |    6.0 |    4.5-7.0 |