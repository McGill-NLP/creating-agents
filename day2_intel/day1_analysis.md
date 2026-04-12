# Day 1 Ground Truth Analysis

## Dataset Overview
- **File**: 1162 papers (1148 with valid frontend_paper_id, 14 without)
- **Columns** (22): paper_id, year, title, authors, primary_area, decision, venue, scores, avg_score, presentations, avg_presentation, soundnesses, avg_soundness, contributions, avg_contribution, confidences, avg_confidence, keywords, citations_serper, frontend_paper_id, submission_date, normalized_citations
- **Ground truth signals**: acceptance decision, per-reviewer scores (list), avg_score, normalized_citations
- **Decision split**: 195 Accept (Oral), 967 reject
- **avg_score distribution**: min=0.00, max=10.00, mean=3.30, median=2.93, stdev=3.15
  - Oral papers: mean=7.82, median=8.00 (range 6.0-10.0)
  - Rejected: mean=2.39, median=1.80 (472 have avg_score=0, likely desk-rejected with no reviews)

## Our Agents' Performance

**Total verdicts submitted**: 814 across 420 unique papers (373 overlap with GT)

| Agent | Verdicts | GT overlap | Pearson | Spearman | Our mean | GT mean |
|---|---|---|---|---|---|---|
| trust-weighted-consensus | 317 | 141 | 0.38 | 0.32 | 5.46 | 4.74 |
| three-stage-budgeted | 115 | 66 | **0.74** | **0.65** | 5.64 | 4.81 |
| adaptive-triage-deep | 131 | 53 | 0.40 | 0.39 | 6.39 | 4.50 |
| light-triage-engagement | 110 | 43 | 0.42 | 0.39 | 5.93 | 4.86 |
| triage-then-deep | 72 | 31 | 0.71 | 0.57 | 5.94 | 4.73 |
| preregistration | 50 | 20 | 0.51 | 0.36 | 7.00 | 5.27 |
| triage | 19 | 2 | n/a | n/a | - | - |

*(Correlations computed on papers with nonzero GT avg_score only, to exclude desk-rejects)*

- **Best**: three-stage-budgeted (Spearman 0.65, Pearson 0.74)
- **Worst**: trust-weighted-consensus (Spearman 0.32) -- highest volume, lowest correlation
- **Runner-up**: triage-then-deep (Spearman 0.57, Pearson 0.71)

## Critical Gaps

1. **We reviewed ZERO Oral papers.** All 373 GT-matched papers were rejected. The platform had 156 Oral papers with verdicts from other teams -- we missed all of them.
2. **Coverage**: We covered only 373/1148 (32%) of GT papers. 776 papers had no verdict from us.
3. **Systematic positive bias**: Our mean score = 5.97 vs GT mean = 2.62 on matched papers (bias = +3.35). Even excluding desk-rejects, we score ~1 point above GT on average.
4. **Narrow range**: Our stdev = 0.97 vs GT stdev = 2.66. We cluster tightly around 5-7 while GT spans 0-10. We do not use the low end of the scale enough.

## Day 2 Recommendations

- **Prioritize Oral papers** -- these are high-signal, high-GT-score papers we completely missed
- **Widen score range** -- especially use scores below 5 more aggressively for weak papers
- **Scale up three-stage-budgeted and triage-then-deep** -- best correlation agents
- **trust-weighted-consensus** has volume but worst discrimination -- consider recalibrating or deprioritizing
