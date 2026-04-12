# Component Regression Analysis — Day 1 Review Scoring

## Data Summary

Ground truth: 1162 ICLR 2025 papers, of which **690 have actual review scores** (avg_score > 0).
472 papers have avg_score = 0 (no reviews / withdrawn). All regressions below use only non-zero GT papers.

GT score distribution (non-zero): mean=5.56, std=2.03, min=1.0, max=10.0, median=5.75

### Reviews with Parseable Scoring Breakdowns per Agent

| Agent | API Comments | With Scoring Breakdown | Matched to non-zero GT |
|-------|-------------|----------------------|----------------------|
| trust-weighted-consensus | 351 | 266 | 117 |
| adaptive-triage-deep | 183 | 56 | 23 |
| triage-then-deep | 92 | 9 | 2 |
| three-stage-budgeted | 117 | 9 | 2 |
| triage | 132 | 14 | 0 |

Note: Most Scoring Breakdowns were added mid-session. The three-stage and triage-then-deep agents posted most of their Scoring Breakdown reviews on papers NOT in the ICLR 2025 GT set.

### Simple Final Score Correlations (from reviewed_papers.json, GT > 0 only)

| Agent | N | Pearson r | Spearman rho | Bias | RMSE | Calibrated R2 | Calibrated RMSE |
|-------|---|-----------|-------------|------|------|--------------|----------------|
| triage | 5 | 0.835 | 0.763 | +0.25 | 1.03 | 0.697 | 1.00 |
| **triage-then-deep** | **31** | **0.711** | **0.569** | **+1.21** | **1.63** | **0.505** | **1.08** |
| preregistration | 20 | 0.510 | 0.355 | +1.73 | 2.14 | 0.260 | 1.21 |
| consensus | 163 | 0.392 | 0.326 | +0.77 | 1.73 | 0.153 | 1.55 |
| adaptive-triage-deep | 45 | 0.369 | 0.349 | +1.94 | 2.52 | 0.136 | 1.61 |
| light-triage-engagement | 21 | 0.365 | 0.340 | +0.76 | 1.72 | 0.134 | 1.52 |

**CRITICAL: Previous correlations (r=0.74 for three-stage) were inflated by including 472 zero-score papers.** When those are excluded, correlations drop significantly. The best real correlator is triage-then-deep at r=0.711.

## Component Regression Coefficients

### Consensus (trust-weighted-consensus)

**Full model** (Ridge alpha=1.0, n=117):
```
gt_score = 0.4411 * S_consensus - 0.0787 * T_breadth + 0.4920 * damped - 0.2636
R2 = 0.2234, r = 0.485
```

**Simple model** (S_consensus only):
```
gt_score = 0.5876 * S_consensus + 1.4446
R2 = 0.2068, r = 0.455
```

**Baseline** (final_score only):
```
gt_score = 0.894 * final_score - 0.076
R2 = 0.1264, r = 0.356
```

**Component importance:**
| Component | Individual r | Coefficient | Interpretation |
|-----------|-------------|-------------|----------------|
| S_consensus | 0.455 | +0.44 | Most important -- weighted median of trusted reviewers |
| damped | 0.397 | +0.49 | Useful second signal, partially redundant with S_consensus |
| T_breadth | 0.064 (n.s.) | -0.08 | Barely matters -- more reviewers does not help prediction |
| delta_skim | 0.000 | 0.00 | Constant zero in all reviews -- not used at all |

Key finding: The damping formula compresses the score range. S_consensus alone is nearly as good as the full formula. delta_skim is never applied.

### Adaptive (adaptive-triage-deep)

n=23 with non-zero GT

**Final score calibration** (best model):
```
gt_score = 1.400 * final_score - 4.054
R2 = 0.335, r = 0.579
```

**raw_float calibration** (WORSE):
```
gt_score = -0.124 * raw_float + 5.614
R2 = 0.061, r = 0.247
```

The negative coefficient on raw_float means HIGHER raw scores predict LOWER GT scores. This is because the adaptive agent scores almost everything 6-7 (59% = 7, 38% = 6), providing no useful discrimination.

### Triage-Then-Deep (best correlator)

Only 2 Scoring Breakdowns matched to GT, so no component regression possible.

**Final score calibration** (n=31):
```
gt_score = 0.862 * agent_score - 0.391
R2 = 0.505, r = 0.711, RMSE_calibrated = 1.077
```

Score distribution: uses values {2.5, 3, 4, 5, 5.5, 6, 6.5, 7, 8} -- widest range of any agent, which explains the best correlation.

## R2 Comparison: Component vs Simple Score

| Agent | Simple Score R2 | Component R2 | Improvement |
|-------|----------------|-------------|-------------|
| consensus | 0.126 | 0.223 | +77% |
| adaptive | 0.136 | 0.335 | +146% |
| triage-then-deep | 0.505 | n/a | (insufficient component data) |

## Score Compression Analysis (Root Cause of Poor Correlation)

| Agent | Score Range Used | Score Std | GT Std | Compression Ratio |
|-------|-----------------|-----------|--------|-------------------|
| consensus | 3-7 | 0.68 | 2.03 | 3.0x compressed |
| adaptive | 5-8 | 0.53 | 2.03 | 3.8x compressed |
| triage-then-deep | 2-8 | 1.06 | 2.03 | 1.9x compressed |
| preregistration | 5-9 | 0.90 | 2.03 | 2.3x compressed |

triage-then-deep has the LEAST compression, which directly explains its superior correlation.

## Bias Decomposition (MSE = bias2 + scatter)

| Agent | Total MSE | bias2 (%) | scatter (%) |
|-------|-----------|-----------|-------------|
| consensus | 2.99 | 20% | 80% |
| triage-then-deep | 2.66 | 55% | 45% |
| adaptive | 6.35 | 59% | 41% |
| preregistration | 4.58 | 66% | 34% |

For consensus, most error is scatter (imprecision). For other agents, most error is systematic bias (over-scoring).

## Optimal Score Distribution

Using the consensus component model:
- Predicted range: 1.88 to 6.09
- Predicted mean: 4.73, std: 0.84
- GT range: 1.0 to 10.0
- GT mean: 4.73, std: 1.73

The component model correctly centers predictions but still under-predicts variance by ~2x. The spread correction in optimal_weights.py addresses this.

## Day 2 Recommended Simplified Formulas

### 1. Consensus Agent
Current: final = round(5.0 + c * (alpha * S_areas - 5.0))
Recommended: final = round(0.59 * S_consensus + 1.44)
- Drops damping entirely, uses S_consensus directly

### 2. Triage-Then-Deep (keep, it works)
Current formula is good. Apply post-hoc calibration:
calibrated = 0.86 * final_score - 0.39

### 3. Adaptive Agent
Fix score compression. Current agent produces 60% 7s and 38% 6s.
- Lower damping anchor from 5.0 to 4.5
- Widen alpha range or remove alpha entirely
- Apply: calibrated = 1.18 * final_score - 3.11

### 4. Universal Spread Correction (apply to ALL agents)
```
adjusted = 5.56 + (raw_score - agent_mean) * (2.03 / agent_std)
```

## Files Produced

- /home/toolkit/creating-agents/tools/optimal_weights.py -- Python module with:
  - compute_optimal_score(components, agent_type) -- component-level optimal scoring
  - calibrate_final_score(score, agent_type) -- simple linear recalibration
  - ensemble_calibrate(agent_scores) -- multi-agent ensemble (correlation-weighted)
  - apply_spread_correction(score, agent_type) -- distribution-matching transform
  - DAY2_RECOMMENDATIONS -- printable recommendations
