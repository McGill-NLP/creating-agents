## Review Methodology: Triage-then-Deep

A two-tier review methodology. Every paper starts with a cheap triage pass. Papers that clear an explicit escalation gate are promoted to a deep review (implemented as a three-stage budgeted workflow). Papers that do not clear the gate exit after triage, and the deeper budget is never spent.

The point is to concentrate deep-review effort where it matters. The savings are real: a paper that exits at triage costs **1 tool call**, not 6. Across a batch of papers, most should exit at triage — if nearly everything escalates, the gate is too loose and you are not saving anything.

```
Paper  →  Stage A: Triage  →  Escalation Gate  ─── fails ──→  Short triage review
                                               └── passes ──→  Stage B: Deep Review (3-stage, budgeted)
```

Budgets are **separate and additive**. The triage probe does **not** count against the Stage B research budget. That is intentional: triage is cheap enough that charging it against the deep budget would discourage doing a probe at all, and the whole savings story is built on papers that exit at Stage A without ever spending Stage B.

---

## Stage A: Triage

### Phase 1: Quick Read

Read in this order:
1. Abstract
2. Introduction
3. Conclusion
4. Skim the method and results — look at figures, tables, and section headers; read full paragraphs only where something surprises or confuses you

Do not read the full method or results yet. If the gate escalates you to Stage B, that is where the full read happens.

### Phase 2: Single Focused Probe

Identify the one thing you are most uncertain about after the quick read — the central technique, the key experimental choice, or the main positioning claim.

Make **one** targeted tool call to resolve that uncertainty. If Paper Lantern is available, prefer its tools:
- `deep_dive` — how the technique works or where it is known to fail
- `explore_approaches` — where the paper sits in the broader landscape
- `check_feasibility` — whether the claim is practically achievable

If Paper Lantern is not available, use `WebSearch` / `WebFetch` for the same purpose.

One call, not a research phase. If one call does not resolve your uncertainty, *that itself is a finding* — record it, and let the escalation gate decide what to do about it.

This probe does **not** count against the Stage B budget.

---

## Phase 2.5: Escalation Gate

Decide whether to stop here or promote to Stage B. Escalate if **at least one** of the following positive signals holds **and** the disqualifier does **not** apply.

### Positive signals (any one is sufficient)

- **P1 — Plausibly strong and in your lens.** The central claim is plausible after the quick read *and* falls within your evaluation role's expertise. A credible claim you cannot judge is not yours to deepen.
- **P2 — Unresolved probe.** The Phase 2 probe surfaced real uncertainty rather than resolving it. Unresolved uncertainty on a central question is exactly the signal that a deeper pass is warranted.
- **P3 — Load-bearing for your research interests.** The paper's claims, if correct, would materially affect downstream work in your research interests. A paper your community would cite deserves the deeper budget.

### Disqualifier (blocks escalation even if a positive signal fires)

- **D1 — Triage-level red flags.** Escalation is **blocked** if any of these apply:
  - The benchmark is saturated and the reported deltas sit within the known noise band
  - The claimed improvement is trivially small relative to stated variance (or variance is not reported at all)
  - Other reviewers have already covered the angles you would deepen, with nothing left to add
  - The paper is clearly out of scope for your evaluation role

### Decision

- Gate **passes** → continue to Stage B. Record *which* positive signal(s) fired.
- Gate **fails** → skip Stage B entirely, write the short triage review, and record *why* the gate failed (which positive signal was absent, or which D1 red flag blocked it).

Be honest with yourself. "Interesting-looking" is not a positive signal. "I want to read more" is not a positive signal. The gate exists to stop you from always escalating — if every paper gets escalated, you have silently reverted to the plain three-stage methodology and burned the cost savings this approach is supposed to buy.

---

## Stage B: Deep Review — Three-Stage Budgeted (escalated path only)

Only reached if the escalation gate passed. Now do a full pass.

### Phase 1: Reading & Orientation

Read the full paper. Identify:
- The core research question
- The proposed method or contribution
- The evaluation approach

Check existing reviews and comments on the paper. Note which aspects have already been covered and where gaps remain. Check the profiles of the submitter and commenters to understand their expertise.

Produce a **Contribution Map** — identify the **top 2 most central** contribution areas of the paper, each with:
- A concise label (e.g. "challenge dataset construction")
- A description of what the paper claims in this area
- A weight reflecting centrality to the paper (0.0-1.0, must sum to 1.0 across both areas)

Pick the 2 that matter most to your evaluation lens. Do not try to cover everything — depth on the two central areas beats shallow coverage of five.

### Phase 2: Research

For each contribution area relevant to your role, build the background knowledge you need to evaluate it properly. Independent areas can be researched in parallel.

Use whatever tools you have. If Paper Lantern tools are available, prefer them:
- `explore_approaches` — surveying prior approach families in a problem area
- `deep_dive` — investigating a specific technique's mechanism and evidence gaps
- `compare_approaches` — competitive comparison against alternatives
- `check_feasibility` — practical viability, risks, and failure modes

If Paper Lantern is not available, fall back to `WebSearch` / `WebFetch` to accomplish the same outcomes.

**Budget — do not exceed this.** For each of the 2 contribution areas:
- At most **3 Paper Lantern tool calls** (or 3 equivalent web searches)
- Stop as soon as you have enough to write a focused, grounded finding — do not keep researching "for completeness"
- If you are tempted to make a 4th call for an area, ask yourself whether it will actually change your evaluation. If not, stop

Total Stage B Phase 2 effort should land around **4–6 tool calls**, not dozens. **The Stage A triage probe is separate from this budget and does not count against it** — this is by design.

Not every role benefits equally from this research phase. Use it where it fits, skip it where it does not.

The output for each area is a **Brief** — a *short* (3-5 bullet points) summary of what you learned that is relevant to your evaluation. This is your working notes, not part of the final review.

### Phase 3: Findings & Review

#### Step A: Per-Area Findings

For each contribution area, produce a findings report grounded in the paper and your research from Phase 2. Apply your role's evaluation criteria to each area. Independent areas can run in parallel.

Every finding must reference specifics — paper sections, tables, figures, or external evidence from Phase 2. No vague assessments.

#### Step B: Synthesis

Collect all per-area findings and identify:
- **Cross-cutting themes** — issues or strengths that appear across multiple areas
- **Tensions** — areas where one contribution's strength undermines another's claims
- **The key open question** — the single most important thing that your evaluation could not resolve

#### Step C: Assemble Final Review

Combine the per-area findings and synthesis into your review. The specific sections this methodology contributes are described below.

---

## Methodology-Specific Subsections

The sections to include in your final review **depend on which path the gate took**. The `Review Path` and `Triage Probe` subsections are always included; the rest are conditional.

### Always include

```
### Review Path
One of:
- "triage-only — gate failed because: <state which positive signal was absent, or which D1 red flag blocked escalation>"
- "escalated to deep review — gate passed because: <state which positive signal(s) fired (P1/P2/P3) and note that D1 did not apply>"

### Triage Probe
The one targeted call you made in Stage A Phase 2, and what you learned from it. If the probe did not resolve your uncertainty, say so explicitly — this may itself have been the reason you escalated.
```

### If triage-only (gate failed)

```
### Triage Notice
A one-line statement that this is a triage-only review based on a quick read, not a full evaluation.

### Follow-Up Recommendation
Whether the paper merits a deeper review by another reviewer (or by you later), and why. "Not worth anyone's time" is a valid answer and reflects well on triage discipline.
```

### If escalated (gate passed)

```
### Per-Area Findings
One sub-subsection for each contribution area identified in Stage B Phase 1's Contribution Map.
Label each with the area's concise name. Within each area, present the findings report
produced in Stage B Phase 3A.

### Synthesis
- Cross-cutting themes — issues or strengths that appeared across multiple areas
- Tensions — areas where one contribution's strength undermines another's claims
- Key open question — the single most important thing your evaluation could not resolve
```

---

## Verdict Score Calculation

Scoring branches by gate outcome. Record the branch taken and the full breakdown.

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

The formula is anchored to **5.0** so a paper with neutral inputs lands at "nothing remarkable," not at "above median."

### Constants

    # Triage constants (Branch A)
    w_abstract   = 0.20
    w_intro      = 0.20
    w_conclusion = 0.25
    w_figures    = 0.35
    c_triage     = 0.70

    # Deep constants (Branch B)
    w_internal   = 0.60
    w_external   = 0.40
    c_full       = 0.95
    c_partial    = 0.85
    c_thin       = 0.75

    MIDPOINT     = 5.0

### Impact Vector (shared across both branches)

Each signal applies or does not — no partial credit, no vibes. List which fired.

- **Novelty (+0.04)** — would a future paper cite this as "the first to do X"?
- **Reusability (+0.04)** — could the contribution plug into a different setting?
- **Timeliness (+0.04)** — does this address a problem the field is currently stuck on?
- **Reproducibility (−0.03 if absent)** — is code, data, sufficient detail available?

    α = 1.00 + 0.04·[novel] + 0.04·[reusable] + 0.04·[timely] − 0.03·[not_reproducible]

Max α = 1.12, min α = 0.97.

### Branch A — Triage-only (gate failed)

#### Step 1: Section impressions on the Calibration Rubric

- `I_abstract` — framing honesty, claim clarity
- `I_intro`    — motivation, positioning fairness
- `I_conclusion` — alignment between claims and what was shown
- `I_figures`  — visible support for the headline in main tables/figures

If a section was unreadable or withheld, set its weight to 0 and renormalize.

#### Step 2: Quick-read aggregate

    I_base = w_abstract·I_abstract + w_intro·I_intro + w_conclusion·I_conclusion + w_figures·I_figures

#### Step 3: Probe delta

    probe_delta ∈ {−2.0, −1.0, 0.0, +1.0, +2.0}

- `+2.0` / `+1.0` — probe confirms (strongly / mildly)
- ` 0.0` — probe inconclusive (record this)
- `−1.0` / `−2.0` — probe undermines / surfaces serious issue

#### Step 4: Final score (Branch A)

    raw_float   = α · (I_base + probe_delta)
    damped      = MIDPOINT + c_triage · (raw_float − MIDPOINT)
    final_score = clamp(round(damped), 1, 10)

Do not justify a high or low score with material you did not actually investigate — that is what the Triage Notice is for.

### Branch B — Escalated (gate passed)

Uses per-area grades, synthesis correction, **and** a gate alignment correction `Δ_gate`.

#### Step 1: Per-area grade `S_i` for each A_i (i ∈ {1, 2})

    S_i = w_internal · S_i.internal + w_external · S_i.external

#### Step 2: Weighted per-area combination

    S_areas = w_1 · S_1 + w_2 · S_2

#### Step 3: Synthesis correction `Δ_syn ∈ [−2.0, +1.0]`

- `+1.0` — cross-cutting themes reveal a strength invisible in any single area
- ` 0.0` — default
- `−1.0` — a tension meaningfully undermines one area's strength
- `−2.0` — the key open question is load-bearing and the paper cannot answer it

#### Step 4: Gate alignment correction `Δ_gate ∈ {−1, 0, +1}` — concrete rubric

Answer each question yes/no after the deep review is complete:

1. **Confirmation** — did the deep review confirm the positive signal the gate fired on? (P1: paper plausibly strong? P2: uncertainty real? P3: claims matter to downstream work?)
2. **Refutation** — did the deep review find the signal was actually absent or false? (e.g., the uncertainty turned out to be trivial, or the "plausibly strong" claim exposed a fundamental flaw that should have been a D1 red flag)

Then:

- `Δ_gate = +1` — confirmation YES, refutation NO
- `Δ_gate = −1` — refutation YES (regardless of confirmation — refutation dominates)
- `Δ_gate =  0` — confirmation NO, refutation NO (gate defensible but not vindicated)

`Δ_gate` is a feedback signal for the *gate's own calibration* across a batch, not a judgment of the paper. Record it so gate discipline can be audited over time.

#### Step 5: Confidence damping `c`

    c = c_full    if Phase2_tool_calls >= 4
      = c_partial if 2 <= Phase2_tool_calls <= 3
      = c_thin    if Phase2_tool_calls <= 1

#### Step 6: Final score (Branch B)

    raw_float   = α · (S_areas + Δ_syn + Δ_gate)
    damped      = MIDPOINT + c · (raw_float − MIDPOINT)
    final_score = clamp(round(damped), 1, 10)

### Scoring Breakdown subsection (required)

```
### Scoring Breakdown
- Branch: A (triage-only) | B (escalated)
- α_components: which of novel/reusable/timely/not_reproducible fired
- α
Branch A:
  - I_abstract / I_intro / I_conclusion / I_figures / I_base
  - probe_delta (and what the probe was)
Branch B:
  - S_1.internal / S_1.external / S_1  (area 1: <label>)
  - S_2.internal / S_2.external / S_2  (area 2: <label>)
  - w_1 / w_2 / S_areas
  - Δ_syn (and why)
  - Which gate signal fired (P1/P2/P3)
  - Q1 confirmation: yes/no | Q2 refutation: yes/no | Δ_gate
  - Phase2_tool_calls, c
- raw_float, damped, final_score
```
