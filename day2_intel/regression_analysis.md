# Regression Analysis: Score Calibration for Day 2

## Data Overview

- **Ground truth**: 1,149 papers with avg_score (mean=3.33, std=3.15, range 0-10)
- **Our verdicts**: 814 verdicts across 420 papers from 7 agents
- **Overlap with GT**: 373 papers matched via frontend_paper_id
- **Core problem**: Our raw scores (mean=5.97, std=0.97) are severely compressed and positively biased vs GT (mean=2.57, std=2.66)

## Per-Agent OLS Calibration (gt = a * raw + b)

| Agent                    |  a      |  b      | R-sq   | RMSE  | n   |
|--------------------------|---------|---------|--------|-------|-----|
| adaptive-triage-deep     | -0.8755 |  8.2266 | 0.0412 | 2.503 |  98 |
| light-triage-engagement  | -0.4830 |  5.6287 | 0.0234 | 2.628 |  79 |
| preregistration          |  0.0152 |  2.8192 | 0.0000 | 2.822 |  36 |
| three-stage-budgeted     |  0.2657 |  1.6482 | 0.0157 | 2.625 |  99 |
| triage-then-deep         |  0.0023 |  2.4288 | 0.0000 | 2.607 |  60 |
| trust-weighted-consensus |  0.2853 |  0.8794 | 0.0048 | 2.645 | 273 |
| triage                   | (too few samples, uses TWC fallback)        |   2 |

**Key finding**: R-sq is extremely low across all agents (0-4%). Our agents have nearly zero linear correlation with ground truth scores. However, the calibration still fixes the **bias** problem.

## Ensemble Ridge Regression

Weights (gt = sum(w_i * score_i) + intercept):

| Agent                    | Weight  |
|--------------------------|---------|
| triage                   |  1.0417 |
| trust-weighted-consensus |  0.3770 |
| three-stage-budgeted     |  0.2713 |
| preregistration          |  0.2138 |
| triage-then-deep         | -0.0166 |
| light-triage-engagement  | -0.3971 |
| adaptive-triage-deep     | -0.8850 |

Intercept: -0.199, Ensemble R-sq: 0.0251, RMSE: 2.621

**Interpretation**: Trust-weighted-consensus and three-stage-budgeted get positive weights (their score direction matches GT somewhat). Adaptive-triage-deep gets a large negative weight, meaning higher scores from that agent actually predict *lower* GT scores (it over-rates weak papers).

## Distribution Comparison

|                  | Mean  | Std   | Corr w/ GT | RMSE vs GT |
|------------------|-------|-------|------------|------------|
| Raw average      | 5.762 | 0.932 | 0.066      | 4.214      |
| OLS calibrated   | 2.594 | 0.348 | 0.188      | 2.612      |
| Z-score calib    | 2.282 | 2.517 | 0.062      | 3.556      |
| Ground truth     | 2.574 | 2.655 | 1.000      | 0.000      |

## Which Agents to Trust

1. **Trust-weighted-consensus** has the most data (273 overlap samples) and positive regression weight
2. **Three-stage-budgeted** has moderate positive weight and reasonable coverage (99 samples)
3. **Adaptive-triage-deep** is anti-correlated with GT -- its high scores go to weak papers
4. **Preregistration** and **triage-then-deep** are essentially random (R-sq ~ 0)

## Recommended Formula for Day 2

**Use the OLS per-agent calibration** (method="ols_avg"):

```
For each agent score:  calibrated_i = a_i * raw_i + b_i
Final score = mean(calibrated_i for all available agents)
Clamp to [1, 10]
```

This fixes the bias (shifts mean from 5.76 to 2.59, matching GT 2.57) though the variance remains compressed (std=0.35 vs GT 2.66). The low R-sq means we cannot reliably rank papers, but we can at least center our distribution correctly.

**Usage**:
```python
from tools.calibrate_score import calibrate
score = calibrate({"trust-weighted-consensus": 6.0, "three-stage-budgeted": 5.5})
# Returns calibrated score ~2.5
```

**Critical insight**: The fundamental problem is not calibration but discrimination -- our agents give very similar scores to all papers (std < 1.0). For Day 2, the highest-leverage improvement is making agents produce a wider score range, not just post-hoc calibration.
