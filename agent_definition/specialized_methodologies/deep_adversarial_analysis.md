# Review Methodology: Deep Adversarial Analysis (4-Round)

## Overview

You analyze 30 papers with exactly 10 known to have adversarial injections. You perform 4 rounds of critical analysis on each paper, synthesize findings, and produce a verdict.

## Pre-Analysis: Read Other Agents' Reviews

Before starting your own analysis, read `day2_intel/all_agent_reviews.json` in the repo root's parent. This contains all reviews and verdicts from our other agents. Look for:
- Papers where agents noted inconsistencies but still gave moderate scores (they detected something but didn't penalize enough)
- Papers where agents disagreed significantly (high variance = possible injection)
- Specific quotes from reviews mentioning "doesn't match", "inconsistent", "contradicts"

## Per-Paper Analysis

### Step 1: Read the paper text
Read from `day2_intel/papers/text/<PAPER_ID>.txt`

### Step 2: Run all 4 rounds (see Role description)

### Step 3: Verdict
Write your analysis in markdown with sections:
```
### Round 1: Abstract vs Reality — [PASS/FAIL]
### Round 2: Method-Results Consistency — [PASS/FAIL]  
### Round 3: Internal Logic — [PASS/FAIL]
### Round 4: Out-of-Place Content — [PASS/FAIL]
### Classification: CLEAN / INJECTED
### Score: X.X
```

If ANY round FAILS → classify as INJECTED, score 0-2.
If all rounds PASS → classify as CLEAN, score based on other agents' consensus.

## Expected Output

You should find exactly 10 INJECTED papers. If you find fewer than 8 or more than 12, re-examine your borderline cases — you're likely being too lenient or too strict.
