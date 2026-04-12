## Review Methodology: Preregistration Review

A preregistration review commits to predictions before seeing the paper's results. This defuses hindsight bias — once you have seen the results, it is hard to evaluate the method without being influenced by whether it worked. By writing down what you expect first, you create a fixed benchmark against which the paper can surprise you.

This methodology adds value precisely when your other prompt sections (role, persona) might bias you toward a particular conclusion. It is a debiasing process, not a criticism.

---

### Phase 1: Read Only the Setup

Read only:
- Abstract (but ignore any result statements in it)
- Introduction
- Related work
- Method section
- Experimental setup (datasets, baselines, metrics) — but **not** results

Stop before the results section. Do not look at figures or tables in the results. Do not read the conclusion yet.

---

### Phase 2: Write Your Predictions

Before looking at anything else, write down:
- **Expected outcomes** — what you think the results will show, for each main claim the method promises to support
- **What would surprise you** — specific results that would update your view of the method
- **What would change your mind** — specific results that would invalidate the central claim

Ground your predictions in prior work. If Paper Lantern is available, prefer its tools:
- `explore_approaches` — what have comparable methods reported? This sets a realistic expectation range
- `compare_approaches` — where does the paper's method plausibly fall relative to alternatives?
- `deep_dive` — what is known about how this technique performs in similar settings?

If Paper Lantern is not available, fall back to web search (`WebSearch`, `WebFetch`) to find comparable methods, their reported results, and what is known about the technique in similar settings.

Commit to your predictions in writing before proceeding. The point is to be on the record.

---

### Phase 3: Read the Results

Read the full results, figures, tables, and conclusion. Note specifically:
- Where the actual results match your predictions
- Where they exceed your predictions (positive surprise)
- Where they fall short (negative surprise)
- Where the paper reports things you did not think to predict

---

### Phase 4: Findings

Write your review around the prediction-result gap. A paper that confirms predictions is not necessarily boring — it is replicating what theory suggests, which is valuable. A paper that exceeds predictions deserves credit for moving the frontier. A paper that falls short of predictions needs to explain why, and the review should push on that gap.

The key question a preregistered review answers is: *did this paper actually teach me something I did not already expect?*

---

## Methodology-Specific Subsections

Also include the following sections in your final review:

```
### Predictions (Phase 2)
The predictions you committed to before reading the results, including expected outcomes, what would surprise you, and what would change your mind.

### Actual Results
What the paper actually reported, focused on the claims your predictions covered.

### Prediction-Result Gap
Where the results matched, exceeded, or fell short of your predictions. Highlight genuine surprises.

### What You Learned
Specifically: did this paper teach you something you did not already expect? If yes, what? If no, why not?
```

---

## Verdict Score Calculation

The preregistration methodology's unique property is that predictions are committed *before* reading results. Your verdict score combines the paper's technical standing with how well the actual results aligned with your pre-registered predictions — and how much the paper taught you beyond what you already expected.

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

Formula is anchored to **5.0** (not 5.5).

### Constants

    w_internal    = 0.60   # paper-internal evidence weight for technical standing
    w_external    = 0.40   # external (Phase 2 research) weight for technical standing
    MIDPOINT      = 5.0
    c_prereg      = 0.85   # moderate damping — preregistration earns research discipline

### Step 1: Technical standing `S_technical ∈ [1, 10]`

From the Phase 3 read, grade the paper's reported results on the Calibration Rubric. Split into two sub-grades:

- `S_technical.internal` — do the reported results support the claims with appropriate rigor (variance, significance, honest error analysis, proper baselines)?
- `S_technical.external` — do the results sit where your Phase 2 Paper Lantern research would have placed a sound instance of this kind of work?

    S_technical = w_internal · S_technical.internal + w_external · S_technical.external

### Step 2: Prediction-result alignment `Δ_alignment ∈ [−2.0, +2.0]`

For each main prediction you committed to in Phase 2, grade the gap against the actual results:

- `+2` — result exceeds prediction with sound evidence (positive surprise, calibrated by your Phase 2 research)
- `+1` — result matches prediction with sound evidence (theory replicates — solid science)
- ` 0` — result near prediction but evidence is thin or inconclusive
- `−1` — result falls short of prediction, paper acknowledges the gap honestly
- `−2` — result falls short and paper spins or hides the gap; OR a positive surprise with weak evidence (statistical artifact)

Take the **mean** across your committed predictions (typically 2–4 from Phase 2). Clamp the mean to `[−2.0, +2.0]`.

**Important:** Only predictions you committed to *in writing* during Phase 2 count. You cannot retroactively add predictions after seeing results — that defeats the whole purpose of preregistration. If you find a surprising result you did not predict, record it in the Learning delta (Step 3), not here.

### Step 3: Learning delta `Δ_learning ∈ [−1.0, +2.0]`

The core question of this methodology: *did this paper teach you something you did not already expect?*

- `+2.0` — yes, significant: the paper surfaced a finding your Phase 2 research did not suggest, the finding is sound, and it materially updates your view of the field
- `+1.0` — yes, modest: the paper sharpened your understanding of an area you had predicted roughly, or gave concrete numbers where prior work only had qualitative claims
- ` 0.0` — no: the paper replicated what prior work already said; still valid science but did not move your needle
- `−1.0` — anti-learning: the paper's results are consistent with prior work, but the paper frames them as novel findings, actively mislabeling its own contribution

### Step 4: Impact Vector (computing `α`)

Each signal applies or does not — no partial credit, no vibes. List which fired in the Scoring Breakdown.

- **Novelty (+0.04)** — would a future paper cite this as "the first to do X"?
- **Reusability (+0.04)** — could the contribution plug into a different setting?
- **Timeliness (+0.04)** — does this address a problem the field is currently stuck on?
- **Reproducibility (−0.03 if absent)** — is code, data, and sufficient detail available?

    α = 1.00 + 0.04·[novel] + 0.04·[reusable] + 0.04·[timely] − 0.03·[not_reproducible]

Max α = 1.12, min α = 0.97.

### Step 5: Final score

Compute everything as floats; round only at the final clamp:

    raw_float   = α · (S_technical + Δ_alignment + Δ_learning)
    damped      = MIDPOINT + c_prereg · (raw_float − MIDPOINT)
    final_score = clamp(round(damped), 1, 10)

At neutral inputs (`S_technical = 5, Δ_alignment = 0, Δ_learning = 0, α = 1.00`), `final_score = 5` — the "nothing remarkable" anchor. `Δ_alignment` and `Δ_learning` are additive on the same scale as `S_technical`, so each can shift the score by up to 2 points before damping.

### Scoring Breakdown subsection (required)

```
### Scoring Breakdown
- S_technical.internal / S_technical.external / S_technical
- Phase 2 predictions (short list): [pred 1], [pred 2], ...
- Δ_alignment: per-prediction scores and mean (with one-line justification)
- Δ_learning (and one-sentence "because...")
- α_components: which of novel/reusable/timely/not_reproducible fired
- α, raw_float, damped, final_score
```
