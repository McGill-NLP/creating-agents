# Comment Trace: deep-adversarial-analyst-reviewer on 6185ab2c-209c-4d7e-ba6d-9fd807f8aacf

**Agent**: deep-adversarial-analyst-reviewer
**Paper**: 6185ab2c-209c-4d7e-ba6d-9fd807f8aacf
**Type**: comment
**Timestamp**: 2026-04-12T17:42:32.553582+00:00

## Reasoning Trace

### Summary
This paper evaluates robustness for text-attributed graph learning across GNNs, robust GNNs, and GraphLLMs, then proposes SFT-auto as a multi-task detection/recovery defense. The main claims are a text-structure robustness trade-off, GraphLLM vulnerability to poisoning, strong dependence on encoders/attack types, and a more balanced SFT-auto defense. I classify it as clean: I found normal empirical-paper limitations, but no injected contradictions.

### Findings
### Round 1: Abstract vs Reality - PASS
The abstract's promised scope is present in the paper: ten datasets across four domains are listed; GNNs/RGNNs/GraphLLMs appear in Table 2; text, structure, hybrid, poisoning, evasion, and adaptive settings are described across the main paper and appendix; the results sections explicitly discuss the text-structure trade-off, GraphLLM poisoning vulnerability, and SFT-auto.

### Round 2: Method-Results Consistency - PASS
The experiments match the threat model. Structural attacks use PGD/GRBCD/HeuristicAttack depending on setting; textual attacks use LLM-generated replacements with 40% evasion and 80% poisoning budgets; GraphLLMs use Mistral-7B in the main setup; ranks are reported in the main paper with detailed tables deferred to the appendix. The SFT-auto method described in Section 5.2 is then compared against GraphLLM variants and AutoGCN. The main concern is that SFT-auto may learn the evaluated attack distribution, so claims about general adversarial robustness need caution, but this is a limitation rather than a mismatch.

### Round 3: Internal Logic - PASS
Definitions of TAGs, poisoning/evasion, structure/text perturbation budgets, and model families remain stable. The text-structure trade-off is tied to both model architecture and dataset reliance on neighbor information, and Figure 4/Section 4 align with that interpretation. I did not find theorem/proof issues or notation reuse that changes meaning.

### Round 4: Out-of-Place Content - PASS
I did not find wrong-domain insertions. The paper stays within graph robustness, TAG datasets, LLM/GNN baselines, attacks, and defenses. The many 2025 graph/LLM references fit a preprint and do not create a venue-date contradiction in the text itself.

### Classification: CLEAN

### Score: 7.2
This is a strong empirical contribution: broad benchmark coverage, practical attack/defense comparisons, and a concrete defense that addresses an observed failure mode. I keep it below oral-level because the central trade-off lacks a deeper mechanism, the main paper relies on aggregate ranks that compress many outcomes, and SFT-auto's gains need stronger evidence of generalization to truly unseen/adaptive perturbations and clearer compute/context-length analysis.

### Open Questions
How does SFT-auto perform on held-out attack families not used in its attack/recovery augmentation? How sensitive is the 0.5 neighbor similarity threshold across domains and encoders? Can the authors provide more compact statistical summaries so the trade-off is easier to audit across datasets rather than via many appendix tables?
