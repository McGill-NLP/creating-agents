## Review Methodology: Three-Stage Review

A three-phase process for producing thorough, well-informed paper reviews.

```
Paper  →  Phase 1: Reading & Orientation  →  Phase 2: Research  →  Phase 3: Findings & Review
```

---

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

---

### Phase 2: Research

For each contribution area relevant to your role, build the background knowledge you need to evaluate it properly. Independent areas can be researched in parallel.

What "research" means depends on your evaluation role. Examples:
- Surveying prior approaches and competing methods
- Understanding the technical details of a specific technique
- Investigating reproducibility norms for the domain
- Checking ethical precedents or known harms in the application area

Use whatever tools you have to accomplish these research goals. If Paper Lantern tools are available, prefer them — they are purpose-built for this kind of research:
- `explore_approaches` — for surveying prior approach families in a problem area
- `deep_dive` — for investigating a specific technique's mechanism and evidence gaps
- `compare_approaches` — for competitive comparison against alternatives
- `check_feasibility` — for assessing practical viability, risks, and failure modes

If Paper Lantern is not available, fall back to web search tools (e.g. `WebSearch`, `WebFetch`) to accomplish the same outcomes.

**Budget — do not exceed this.** For each of the 2 contribution areas:
- At most **3 Paper Lantern tool calls** (or 3 equivalent web searches if Paper Lantern is unavailable)
- Stop as soon as you have enough to write a focused, grounded finding — do not keep researching "for completeness"
- If you are tempted to make a 4th call for an area, ask yourself whether it will actually change your evaluation. If not, stop

Total Phase 2 effort across both areas should land around **4–6 tool calls**, not dozens. A good Phase 2 is focused and returns quickly; an exhaustive Phase 2 leaves no time for Phase 3 (the actual review).

Not every role benefits equally from this research phase. Use it where it fits, skip it where it doesn't.

The output for each area is a **Brief** — a *short* (3-5 bullet points) summary of what you learned that is relevant to your evaluation. This is your working notes, not part of the final review.

---

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

Also include the following sections in your final review:

```
### Per-Area Findings

One sub-subsection for each contribution area identified in Phase 1's Contribution Map.
Label each with the area's concise name. Within each area, present the findings report
produced in Phase 3A.

### Synthesis

- Cross-cutting themes — issues or strengths that appeared across multiple areas
- Tensions — areas where one contribution's strength undermines another's claims
- Key open question — the single most important thing your evaluation could not resolve
```

---

## Verdict Score Calculation

The three-stage methodology already evaluates two contribution areas with explicit weights. The verdict is a weighted combination of per-area grades, a synthesis correction, and an impact factor — all derived from work you already did.

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

The formula is anchored to **5.0** (not 5.5) so that a paper with neutral inputs lands at "nothing remarkable," not at "above median."

### Constants

    w_internal    = 0.60   # paper-internal evidence weight per area
    w_external    = 0.40   # external-context weight per area
    # Contribution Map weights (w_1, w_2) are set per-paper in Phase 1, sum = 1.0
    MIDPOINT      = 5.0
    c_full        = 0.95   # ≥ 4 Phase 2 tool calls
    c_partial     = 0.85   # 2–3 calls
    c_thin        = 0.75   # ≤ 1 call — flag explicitly; you are barely above triage

### Step 1: Per-area grade `S_i` for each contribution area A_i (i ∈ {1, 2})

For each area, split the grade into two sub-grades on the Calibration Rubric:

- `S_i.internal` — grade from paper-internal evidence (Sections, Tables, Figures you cited in Phase 3A). [1, 10]
- `S_i.external` — grade from your Phase 2 Brief (prior work, competing methods, feasibility). [1, 10]

    S_i = w_internal · S_i.internal + w_external · S_i.external

Internal evidence weighs more — the paper is ultimately judged on what it shows, not on how it sits in the landscape.

### Step 2: Weighted per-area combination

Using the Contribution Map weights `w_1`, `w_2` from Phase 1:

    S_areas = w_1 · S_1 + w_2 · S_2

### Step 3: Synthesis correction `Δ_syn ∈ [−2.0, +1.0]`

Asymmetric ceiling — synthesis should rarely promote a paper, but may catch tensions that demote it:

- `+1.0` — cross-cutting themes reveal a strength invisible in any single area
- ` 0.0` — default
- `−1.0` — a tension meaningfully undermines one area's strength
- `−2.0` — the key open question is load-bearing and the paper cannot answer it

### Step 4: Impact Vector (computing `α`)

Each signal applies or does not — no partial credit, no vibes. List which fired in the Scoring Breakdown.

- **Novelty (+0.04)** — would a future paper cite this as "the first to do X"?
- **Reusability (+0.04)** — could the contribution be plugged into a different setting (different domain, different model scale, different task)?
- **Timeliness (+0.04)** — does this address a problem the field is currently stuck on?
- **Reproducibility (−0.03 if absent)** — is code, data, and sufficient detail available to reproduce?

Formula (max α = 1.12, min α = 0.97):

    α = 1.00 + 0.04·[novel] + 0.04·[reusable] + 0.04·[timely] − 0.03·[not_reproducible]

### Step 5: Confidence damping `c`

Select based on how much Phase 2 research budget you actually used across both areas:

    c = c_full    if Phase2_tool_calls >= 4
      = c_partial if 2 <= Phase2_tool_calls <= 3
      = c_thin    if Phase2_tool_calls <= 1

### Step 6: Final score

Compute everything as floats; round only at the final clamp:

    raw_float   = α · (S_areas + Δ_syn)
    damped      = MIDPOINT + c · (raw_float − MIDPOINT)
    final_score = clamp(round(damped), 1, 10)

### Scoring Breakdown subsection (required)

```
### Scoring Breakdown
- S_1.internal / S_1.external / S_1  (area 1: <label>)
- S_2.internal / S_2.external / S_2  (area 2: <label>)
- w_1 / w_2 / S_areas
- Δ_syn (and why)
- α_components: which of novel/reusable/timely/not_reproducible fired
- α, Phase2_tool_calls, c
- raw_float, damped, final_score
```
