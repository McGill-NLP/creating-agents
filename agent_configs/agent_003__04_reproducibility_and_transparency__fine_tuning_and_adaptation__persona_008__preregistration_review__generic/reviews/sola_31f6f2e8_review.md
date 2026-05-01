# Review: Reversible Lifelong Model Editing via Semantic Routing-Based LoRA

Paper ID: 31f6f2e8-0fb2-46ff-ab65-f3408612f6e1
Reviewer role: Reproducibility & Transparency Evaluator
Methodology: Preregistration Review

## Summary

This paper proposes SoLA, a framework for lifelong model editing that assigns each edit an independent LoRA module, freezes it after training, and maps it to inputs via semantic routing using the hidden representation of the last token as a key. The central claims are: (1) SoLA avoids catastrophic forgetting and semantic drift by freezing both LoRA modules and keys after each edit, (2) edits can be precisely revoked by removing their key from the routing table (a claimed first in the literature), and (3) a master decision mechanism integrates routing into the edited layer itself, eliminating auxiliary routing networks. From a reproducibility standpoint, the paper presents a compelling and architecturally clean idea, but I find myself somewhat concerned about several gaps in the experimental specification that would make independent replication challenging — though not impossible.

## Predictions (Phase 2)

Based on reading the introduction, method, and experimental setup (but not results), and informed by prior work on MELO and ELDER:

**Expected outcomes:**
- I would expect SoLA to perform comparably to or slightly better than MELO on edit reliability (ERR) and task retention (TRR), given that frozen per-edit LoRA modules with fixed keys should avoid MELO's cluster drift problem. On SCOTUS with BERT, I would predict ERR around 0.93-0.97 and TRR around 0.90-0.95.
- On zsRE with T5, I would expect ERR around 0.70-0.80 and TRR around 0.95-0.98, roughly in line with GRACE and MELO.
- On hallucination correction (GPT2-XL), the PPL-based metrics are harder to predict, but I would expect SoLA to achieve PPL values competitive with MELO (ERR ~15-18, TRR ~1-2) given the similar architectural philosophy.
- Parameter efficiency should be very high — likely the best among all methods — since only one small LoRA module is active during each edit.

**What would surprise me:**
- If SoLA substantially outperformed ELDER on all metrics simultaneously, that would be surprising, since ELDER's learned router should theoretically be more expressive than a static nearest-key lookup.
- If the rollback mechanism worked perfectly across all conditions without any degradation, that would also be surprising, as downstream edits may implicitly depend on earlier ones.

**What would change my mind:**
- If SoLA showed significant degradation in ERR or TRR beyond ~400 sequential edits, it would suggest the semantic routing approach doesn't scale as claimed.
- If the parameter count grew substantially with number of edits (contradicting the 0.08M claim), the efficiency argument would weaken.

## Actual Results

The paper reports:
- SCOTUS (BERT): ERR=0.97, TRR=0.95, Avg=0.96 — best among all methods
- zsRE (T5): ERR=0.73, TRR=0.99, Avg=0.86 — best average, though CLEAR had highest ERR (0.99)
- Hallucination (GPT2-XL): ERR=15.15, TRR=1.01, ARR=7.35 — best or near-best across metrics
- Table 2 (UniEdit, WikiBigEdit) confirms strong performance with larger models (LLaMA-3-8B, DeepSeek-R1-8B, Qwen2-7B)
- Rollback demonstration (Table 3) shows clean revocation on zsRE examples
- Ablations show rank=4 is optimal, mid-layer editing (3-5) works best

## Prediction-Result Gap

My predictions were reasonably well-calibrated:
- **SCOTUS ERR/TRR**: I predicted 0.93-0.97 / 0.90-0.95; actual was 0.97 / 0.95 — upper end of my prediction, confirming the frozen-key advantage.
- **zsRE**: I predicted ERR 0.70-0.80; actual 0.73 — squarely in range. TRR predicted 0.95-0.98; actual 0.99 — slightly exceeded.
- **Hallucination PPL**: ERR=15.15 matched my expectation of being competitive with MELO (17.45). Slightly better than expected.
- **Positive surprise**: The consistency across Figure 4 — SoLA maintains near-perfect stability across 1000 edits on SCOTUS — exceeded my expectations. Most methods degrade visibly after 400+ edits.
- **No surprise**: The rollback demo (Table 3) was limited to 5 examples on zsRE, which doesn't stress-test the mechanism as thoroughly as I'd hoped.

## What You Learned

The main thing this paper taught me that I didn't fully anticipate: the degree to which simply freezing per-edit LoRA modules and their corresponding keys provides such strong protection against catastrophic forgetting. The stability curves in Figure 4 are genuinely impressive — the method maintains near-constant performance across the full editing sequence. This suggests that the key bottleneck in prior methods (MELO, GRACE) was not the LoRA architecture itself but the mutable nature of routing/clustering state. That is a somewhat insightful finding.

However, the paper did not surprise me on the reversibility front — the demonstration was too limited to be convincing beyond simple, independent single-hop edits.

## Findings

### Method Description Completeness

The method section provides a clear and, I think, largely sufficient description for reimplementation. The semantic routing mechanism (Section 3.3) is well-specified: the last token's hidden representation serves as the key, LoRA modules are assigned per-edit and frozen, and cosine similarity (implied by "distance metric") is used for matching. The master decision mechanism (Section 3.4, Equation 3) is clearly formulated with threshold alpha=0.01.

However, I would gently note a few gaps that might cause difficulty for an implementer:
- The exact distance function dist(q, k_i) is not explicitly named — cosine similarity is implied but not stated.
- The initialization scheme for the LoRA A and B matrices is mentioned (A from Gaussian, B from zero) following the standard Hu et al. (2022) convention, which is fine, but the specific Gaussian parameters (mean, variance) are not given.
- How the semantic key e is computed from the hidden representation of the last token is described, but the specific layer from which it is extracted is not always clear (is it the same edited layer? the input to that layer?).
- The training procedure for each individual LoRA module (optimizer, learning rate, number of steps/epochs) is not specified in the method section and I could not find it in the experimental setup either.

### Experimental Setup Completeness

This is perhaps my most significant concern from a reproducibility standpoint. While the paper provides a reasonable overview of the experimental setup, several critical details appear to be missing:

**Datasets:**
- SCOTUS, zsRE, and hallucination correction benchmarks are referenced but preprocessing details are sparse.
- The exact number of sequential edits performed is not always clearly stated (Figure 4 suggests ~1000 for SCOTUS, but Tables 1-2 don't specify).
- For UniEdit and WikiBigEdit (Table 2), dataset sizes and splits are not described.

**Hyperparameters:**
- LoRA rank is set to 4 (from ablation), but the learning rate, optimizer, batch size, number of training steps per edit, and weight decay are not reported.
- The threshold alpha=0.01 is specified, which is good.
- How many epochs/steps each individual LoRA module is trained for each edit is not stated — this is a critical detail since overfitting to a single edit would be easy with a small LoRA module.

**Compute:**
- A single NVIDIA A100 40GB GPU is mentioned for the ablation study (Table 4), but the hardware for the main experiments (Tables 1-2) is not specified.
- Training time per edit is partially reported in the ablation (Table 4-5, "Edit Time(min)"), showing ~5.86-9.21 minutes depending on layer selection, but total training time for the full editing sequence is not provided.
- No random seeds or variance across runs are reported.

**Evaluation:**
- Metrics (ES, ERR, TRR, ARR) are defined clearly.
- However, whether results are averaged over multiple runs or represent a single run is not stated.
- No confidence intervals or standard deviations are provided.

### Code and Artifact Availability

- No code repository URL is provided in the paper or the submission metadata (github_repo_url is null).
- No trained model weights are available.
- No indication of when or whether code will be released.
- The paper does not mention any plans for artifact release, which is somewhat disappointing for a method that claims to be a "first" in reversible model editing.

### Computational Requirements

Based on what is reported and can be inferred:
- A single A100 40GB GPU appears sufficient for the main experiments (BERT, T5-small, GPT2-XL).
- Edit time is approximately 5-6 minutes per edit (rank=4, mid-layer), meaning 1000 edits would require roughly 83-100 GPU-hours — substantial but not unreasonable.
- For larger models (Table 2: LLaMA-3-8B, DeepSeek-R1-8B, Qwen2-7B), the computational requirements are not stated at all. These would likely require significantly more memory and time.
- Storage scales linearly with number of edits (one LoRA module + one key per edit), but the actual storage overhead is not quantified.

### Transparency Assessment

- The paper does not discuss negative results or failed approaches.
- No mention of how many hyperparameter configurations were tried before arriving at rank=4 and alpha=0.01.
- The relationship between the submission and any preprint is not discussed.
- No responsible ML checklist is referenced or included.
- The paper does acknowledge the limitation that performance depends on semantic representation quality, which I appreciate.

### The Email Test Result

**Significant gaps.** A competent researcher with the paper alone would be able to understand the method and implement the core architecture, but would need to make several educated guesses about training hyperparameters (learning rate, optimizer, number of steps per edit), could not verify their results against the reported numbers without substantial experimentation, and would have no code to reference. The missing training details for individual LoRA modules are particularly problematic — this is the core operation of the method, and its specification is incomplete.

### Overall Reproducibility Verdict

**Significant gaps.** The method is clearly described at a conceptual and architectural level, and the key design choices (frozen keys, per-edit LoRA, master decision threshold) are well-specified. However, the absence of training hyperparameters, lack of variance reporting, no code release, and incomplete compute specifications create substantial barriers to independent replication. A motivated researcher could likely reproduce the general trends, but matching the exact numbers in Tables 1-2 would require significant trial and error.

## Open Questions

1. Could the authors specify the complete training protocol for each individual LoRA module — optimizer, learning rate, schedule, number of steps/epochs, and any regularization?
2. Are the results in Tables 1-2 from a single run or averaged across multiple seeds? If the latter, what is the variance?
3. Is there a plan to release code and/or trained model weights? This would substantially strengthen the contribution.
4. How does the storage overhead (number of stored LoRA modules + keys) scale in practice — could you provide a concrete memory footprint for 100, 500, and 1000 edits?
5. For the larger-scale experiments in Table 2, what hardware was used and what was the per-edit training time?
6. The rollback demonstration in Table 3 covers only 5 independent, single-hop examples. Have you tested rollback in scenarios where later edits are causally dependent on earlier ones?
