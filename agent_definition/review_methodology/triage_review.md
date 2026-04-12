## Review Methodology: Triage Review

Not every paper deserves a full, deep review. A triage review is a deliberate lightweight pass designed to cover more papers with informed but shallow engagement. The goal is not to produce the definitive review — it is to produce a useful short take and decide whether the paper merits deeper work later.

Use this methodology when breadth matters more than depth, or when an initial scan tells you the paper does not justify a full workup.

---

### Phase 1: Quick Read

Read in this order:
1. Abstract
2. Introduction
3. Conclusion
4. Skim the method and results — look at figures, tables, and section headers; read full paragraphs only where something surprises or confuses you

Do not read the full method or full results unless your triage pass flags a reason to.

---

### Phase 2: Single Focused Probe

Identify the one thing you are most uncertain about after the quick read — the central technique, the key experimental choice, or the main positioning claim.

Make **one** targeted tool call to resolve that uncertainty. If Paper Lantern is available, prefer its tools:
- `deep_dive` if you need to understand how the technique works or where it is known to fail
- `explore_approaches` if you need to place the paper in the broader landscape
- `check_feasibility` if you are unsure whether the paper's claim is practically achievable

If Paper Lantern is not available, use web search (`WebSearch`, `WebFetch`) for the same purpose — a single targeted search to resolve the same uncertainty.

One call, not a research phase. If one call does not resolve your uncertainty, that itself is a finding.

---

### Phase 3: Short Take

Write a short review. Be explicit that this is a triage review — readers and other reviewers should know you did not do a deep pass, so they can calibrate their trust in your assessment and potentially follow up themselves.

---

## Methodology-Specific Subsections

Also include the following sections in your final review:

```
### Triage Notice
A one-line statement that this is a triage review based on a quick read, not a full evaluation.

### Probe
The one specific thing you investigated beyond the quick read, and what you learned from it. If no probe was needed, say so.

### Follow-Up Recommendation
Whether the paper merits a deeper review, and why — from yourself, another reviewer, or not at all.
```

---

## Verdict Score Calculation

Compute — do not intuit — the verdict from the signals you gathered during the three phases. Every input is recorded so the score is traceable.

### Calibration Rubric (integer final scores map to meaning)

- **10** — Landmark. Agenda-setting or likely to be built on for years.
- **9**  — Major contribution. Clearly above the bar for its venue.
- **8**  — Strong contribution. Likely to be built on.
- **7**  — Good paper. Solid execution of a worthwhile problem.
- **6**  — Adequate. Correct but not especially novel or broad.
- **5**  — **Default "nothing remarkable."** Correct but niche, or interesting but incomplete.
- **4**  — Below bar. Notable weaknesses but not broken.
- **3**  — Weak: sound methodology with a claim that does not hold up, or vice versa.
- **2**  — Serious problems, mostly salvageable with a rewrite.
- **1**  — Broken. Fatally flawed, fraudulent, or an AI-generated non-paper.

The formula is anchored to **5.0** (not the numerical midpoint 5.5) so that a paper with neutral/default inputs lands at "nothing remarkable," not at "above median."

### Constants (tune here, not inline)

    w_abstract    = 0.20
    w_intro       = 0.20
    w_conclusion  = 0.25
    w_figures     = 0.35   # heaviest — only direct evidence in a triage
    MIDPOINT      = 5.0
    c_triage      = 0.70   # triage confidence damping

### Step 1: Section impressions (Phase 1 quick read)

For each section you actually read, assign a sub-score on the Calibration Rubric:

- `I_abstract` — framing honesty, claim clarity
- `I_intro`    — motivation, positioning fairness
- `I_conclusion` — alignment between claims and what was shown
- `I_figures`  — visible support for the headline in main tables/figures

If a section was unreadable or withheld, set its weight to 0 and renormalize the remaining weights so they sum to 1.0.

### Step 2: Quick-read aggregate

    I_base = w_abstract·I_abstract + w_intro·I_intro + w_conclusion·I_conclusion + w_figures·I_figures

### Step 3: Probe delta (Phase 2)

The single targeted Phase 2 call adjusts `I_base` by one of:

- `+2.0` — probe strongly confirms the headline / de-risks the core uncertainty
- `+1.0` — probe mildly supports
- ` 0.0` — probe is inconclusive or did not resolve the uncertainty (record this)
- `−1.0` — probe mildly undermines the claim
- `−2.0` — probe surfaces a serious issue the quick read missed

### Step 4: Impact Vector (computing `α`)

Each signal applies or does not — no partial credit, no vibes. In the Scoring Breakdown, explicitly list which signals fired and why.

- **Novelty (+0.04)** — would a future paper cite this as "the first to do X"?
- **Reusability (+0.04)** — could the contribution be plugged into a different setting (different domain, different model scale, different task)?
- **Timeliness (+0.04)** — does this address a problem the field is currently stuck on?
- **Reproducibility (−0.03 if absent)** — is code, data, and sufficient detail available to reproduce?

Formula (max α = 1.12, min α = 0.97):

    α = 1.00 + 0.04·[novel] + 0.04·[reusable] + 0.04·[timely] − 0.03·[not_reproducible]

### Step 5: Final score

Compute everything as floats; round only at the final clamp:

    raw_float   = α · (I_base + probe_delta)
    damped      = MIDPOINT + c_triage · (raw_float − MIDPOINT)
    final_score = clamp(round(damped), 1, 10)

### Scoring Breakdown subsection (required in the review)

Add this subsection to the review. Record every variable:

```
### Scoring Breakdown
- I_abstract / I_intro / I_conclusion / I_figures (and any reweighting)
- I_base
- probe_delta (and what the probe was)
- α_components: which of novel/reusable/timely/not_reproducible fired (and why)
- α, raw_float, damped, final_score
```
