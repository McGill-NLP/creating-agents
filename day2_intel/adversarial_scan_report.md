# Adversarial Content Injection Scan Report

**Date:** 2026-04-11
**Papers scanned:** 30
**Classification:** ALL 30 CLEAN (no injections detected)

---

## Methodology

Each paper was scanned using the following multi-layered approach:

1. **Full abstract and introduction reading** for all 30 papers to establish topic baseline
2. **Results/tables section scanning** for impossible numbers or out-of-domain metrics
3. **Middle section deep reading** for notation inconsistencies or spliced paragraphs
4. **Cross-paper keyword searches** for out-of-domain content including:
   - Astronomy terms (speed of light, galaxy, orbit, planetary, etc.)
   - Medical terms (surgery, medication, dosage, tumor, etc.)
   - Cooking terms (recipe, ingredient, oven, tablespoon, etc.)
   - Finance terms (stock market, portfolio, cryptocurrency, etc.)
   - Biology terms (species, ecosystem, gene expression, etc.)
   - Physics terms (photon, wavelength, electromagnetic, etc.)
   - Travel/geography terms (travel time, kilometers, nautical miles, etc.)
   - Political terms (election, democrat, congress, etc.)
   - Sports terms (football, soccer, touchdown, etc.)
   - Injection artifacts (ignore previous, system prompt manipulation, etc.)
5. **Impossible number detection** searching for accuracy >100% or similar anomalies
6. **Abstract-results consistency checking** to verify claims match evaluations

## Note on Prior Scan

A prior scan existed in `adversarial_scan.json` that flagged 14 of 30 papers as INJECTED, claiming to find "COOKING INSTRUCTIONS", "POLITICAL NARRATIVE", "FOOTBALL NEWS", "ASTRONOMY", "PHYSICS EQUATIONS", and "MEDICAL CONTENT" injections. **These claims are false.** Extensive keyword searching confirmed that none of these content types exist in any of the papers. The prior scan appears to have been hallucinated or fabricated.

---

## Per-Paper Results

### 1. 92fd5c0c - Universal Model Routing for Efficient LLM Inference
**Classification: CLEAN (high confidence)**
Full text read (~2300 lines). Consistently about LLM routing with UniRoute, cluster-based representations, and dynamic LLM pools. Mathematical framework, proofs, and experimental results are all coherent and on-topic.

### 2. 0d01a044 - Single Index Bandits
**Classification: CLEAN (high confidence)**
Detailed scan of abstract, methods, results, and appendices. Consistently about contextual bandits with unknown reward functions using Stein's method. Regret bounds and algorithms are mathematically sound.

### 3. 49665cc8 - Sharing State Between Prompts and Programs
**Classification: CLEAN (high confidence)**
Consistently about the NIGHTJAR programming system for shared program state between LLM prompts and Python programs. Code examples, formal semantics, and evaluation are coherent.

### 4. 0828e010 - Neon: Negative Extrapolation From Self-Training
**Classification: CLEAN (high confidence)**
Consistently about image generation improvement via negative extrapolation. FID scores, precision/recall tradeoffs, and multi-architecture results are reasonable and on-topic.

### 5. 95e68002 - Denoising Neural Reranker for Recommender Systems
**Classification: CLEAN (high confidence)**
Consistently about the DNR framework for recommendation reranking. Denoising, adversarial, and regularization objectives are coherently described with standard evaluation metrics.

### 6. 3e196547 - Attention as a Compass (AttnRL)
**Classification: CLEAN (high confidence)**
Consistently about process-supervised RL for reasoning models. Attention-based branching, adaptive sampling, and off-policy training are coherently described.

### 7. 9e4c8fd4 - Structurally Human, Semantically Biased
**Classification: CLEAN (high confidence)**
Consistently about detecting LLM-generated citation graphs. Paired graph construction, structural vs. semantic analysis, and GNN evaluations are coherent.

### 8. ad6a35ae - RobustSpring
**Classification: CLEAN (high confidence)**
Consistently about robustness benchmarking for optical flow, scene flow, and stereo. 20 corruption types with appropriate metrics.

### 9. 6185ab2c - Robustness in Text-Attributed Graph Learning
**Classification: CLEAN (high confidence)**
Consistently about TAG robustness for GNNs and GraphLLMs. Structural and textual perturbation analysis is coherent.

### 10. 434fda84 - Erase or Hide? (SSIUU)
**Classification: CLEAN (high confidence)**
Consistently about LLM unlearning via attribution-guided regularization to suppress spurious unlearning neurons.

### 11. 30dcd161 - VeriGuard
**Classification: CLEAN (high confidence)**
Consistently about formal safety verification for LLM agents via verified code generation. ASR/TSR metrics are reasonable.

### 12. 28e42b62 - GTPO and GRPO-S
**Classification: CLEAN (high confidence)**
Consistently about entropy-weighted reward shaping for LLM reasoning. Token and sequence-level algorithms are coherently described.

### 13. cc5f842d - Training-free Guidance in T2V (VIDEO-MSG)
**Classification: CLEAN (high confidence)**
Consistently about training-free guidance for text-to-video generation via multimodal planning and noise initialization.

### 14. 4db63ed5 - OneReward
**Classification: CLEAN (high confidence)**
Consistently about unified RL framework for mask-guided image generation across multiple tasks.

### 15. 4c75d4c8 - DexMachina
**Classification: CLEAN (high confidence)**
Consistently about dexterous robot manipulation with curriculum-based virtual object controllers.

### 16. 54e3fdab - MemGen
**Classification: CLEAN (high confidence)**
Consistently about generative latent memory for self-evolving LLM agents. GSM8K-style examples are legitimate evaluation content.

### 17. eb305acf - AGENTFLOW
**Classification: CLEAN (high confidence)**
Consistently about in-the-flow agentic system optimization with Flow-GRPO for planning and tool use.

### 18. b3c0352f - Spatial Mental Modeling (MINDCUBE)
**Classification: CLEAN (high confidence)**
Consistently about VLM spatial reasoning with the MINDCUBE benchmark for cognitive mapping and mental simulation.

### 19. 14aeeb93 - HiMAE
**Classification: CLEAN (high confidence)**
Consistently about hierarchical masked autoencoders for wearable sensor data. Medical biomarker descriptions (blood pressure, A1C, etc.) are legitimate downstream health monitoring tasks.

### 20. a17016b1 - Common Corpus
**Classification: CLEAN (high confidence)**
Consistently about ethical data collection for LLM pre-training. Financial/legal/government data references are about the dataset contents, not injected topics.

### 21. 8cebc6ca - REGENT
**Classification: CLEAN (high confidence)**
Consistently about retrieval-augmented generalist agents for in-context learning in new environments.

### 22. 2c1f60ae - Faster Cascades via Speculative Decoding
**Classification: CLEAN (high confidence)**
Consistently about combining model cascading with speculative decoding for efficient LLM inference.

### 23. 0de7202a - miniCTX
**Classification: CLEAN (high confidence)**
Consistently about context-dependent neural theorem proving in Lean with the miniCTX benchmark.

### 24. 49e7c3d3 - ShEPhERD
**Classification: CLEAN (high confidence)**
Consistently about SE(3)-equivariant diffusion for bioisosteric drug design with shape, electrostatics, and pharmacophore representations.

### 25. bd905a52 - GauMamba (Weather Nowcasting)
**Classification: CLEAN (high confidence)**
Consistently about weather radar sequence prediction using spatiotemporal Gaussian representations. The "101.1% improvement" is a relative improvement metric, not an absolute accuracy value.

### 26. e3df424f - Vico (Compositional Video Generation)
**Classification: CLEAN (high confidence)**
Consistently about compositional video generation via flow equalization in attention graphs.

### 27. ad77eb1e - GUARD
**Classification: CLEAN (high confidence)**
Consistently about LLM safety testing via adaptive role-play and jailbreak diagnostics. Financial/hiring/demographic content is part of the safety testing scenarios.

### 28. b62b8218 - CTNet
**Classification: CLEAN (high confidence)**
Consistently about CNN-Transformer hybrid for 6D object pose estimation. 100% accuracy on some LineMOD objects is normal for this well-studied benchmark.

### 29. 1df48f20 - LiSeCo (Linearly Controlled Language Generation)
**Classification: CLEAN (high confidence)**
Consistently about control-theoretic text generation steering with formal guarantees for toxicity avoidance.

### 30. 2b25b44f - pSAE-chiatry
**Classification: CLEAN (high confidence)**
Consistently about sparse autoencoders for mental health feature identification in language models. Suicide/depression content is the core research topic, not injected material.

---

## Summary

All 30 papers were classified as CLEAN with high confidence. No adversarial content injection was detected in any paper. Every paper maintains consistent topic, notation, and results from abstract through appendix. No out-of-domain content, impossible numbers, abstract-results mismatches, or spliced paragraphs were found.
