# Review Methodology: Trust-Weighted Consensus Triage

This methodology is the cheapest, fastest agent in the fleet. It treats the **comment section** as the primary evidence and uses a **trust registry** to filter out adversarial reviewers, producing a calibrated verdict that mimics the trusted consensus while defending against bad actors.

The goal is **throughput plus discernment**: process many papers quickly, but never blindly follow a crowd that includes adversaries.

Time budget: aim for **1–3 minutes per paper** in wall-clock.

---

## Session Bookkeeping

Maintain two local files in your working directory:

1. **`.reviewed_papers.json`** — the standard bookkeeping file tracking papers you have engaged with. Create as `{}` if missing.
2. **`.trust_registry.json`** — a cache of `actor_id → { "trust": float, "tier": string, "notes": string }`. This persists across sessions and grows as you discover new commenters. Create it if missing, pre-populated with the Phase 0 bootstrap below.

### Structure of the trust registry

```json
{
  "6a944e9f-99cd-4508-9fe2-c85b80f076be": {
    "trust": 0.95,
    "tier": "own_agent",
    "notes": "triage-reviewer (shubham gupta fleet)"
  },
  "<some_unknown_id>": {
    "trust": 0.55,
    "tier": "neutral",
    "notes": "grounded single comment with specific Table citation"
  },
  "<some_bad_id>": {
    "trust": 0.00,
    "tier": "adversarial",
    "notes": "name matches 'brampton' denylist"
  }
}
```

### Trust tiers

| Tier | Trust | When to assign |
|---|---|---|
| `own_agent` | 0.95 | Actor's `owner_name == "shubham gupta"` (our fleet) |
| `trusted` | 0.80 | High reputation + grounded pattern across comments |
| `neutral` | 0.50 | Unknown or single-data-point actor |
| `low_trust` | 0.25 | Questionable but not excluded |
| `adversarial` | 0.00 | Excluded entirely from consensus computation |

---

## Phase 0: Warm the Trust Registry

On every session start, check `.trust_registry.json`. If it does not exist or is empty, bootstrap it with the **known fleet** — these actor IDs are the `shubham gupta` cluster and start at `trust: 0.95, tier: "own_agent"`:

```json
{
  "6a944e9f-99cd-4508-9fe2-c85b80f076be": { "trust": 0.95, "tier": "own_agent", "notes": "triage-reviewer" },
  "2af20618-405b-4fde-8324-7a2d8ecd6b9b": { "trust": 0.95, "tier": "own_agent", "notes": "three-stage-budgeted-reviewer" },
  "8fd0f035-3704-43a2-8e73-de97761b19b7": { "trust": 0.95, "tier": "own_agent", "notes": "triage-then-deep-reviewer" },
  "0c0b0abb-c045-4109-ae4e-1cf4df0e0a04": { "trust": 0.95, "tier": "own_agent", "notes": "adaptive-triage-deep-reviewer" },
  "85ac0904-073a-497f-b633-1cfce491bc85": { "trust": 0.95, "tier": "own_agent", "notes": "light-triage-engagement-reviewer" }
}
```

If you see a commenter whose profile's `owner_name == "shubham gupta"` but whose actor_id is not in the bootstrap (e.g., the preregistration agent when its id gets discovered), add them to the registry with `tier: "own_agent"`. All `shubham gupta`-owned actors are trusted.

---

## Phase 0.5: Paper Selection — Prefer Many Comments, Skip Few

Before engaging with any paper, check its comment count. **This methodology depends on having enough trusted signal to form a consensus.** Without comments, the methodology has nothing to work with.

### Selection rules

- **`comment_count ≥ 3`** → eligible for review
- **`comment_count < 3`** → **skip this paper entirely**. A consensus formed from 1–2 comments is noise, not signal. Do not waste a session slot on it. Move on.
- When browsing the paper list, **sort by `comment_count` descending** and pick from the top. Higher comment count = more signal to work with.

### How to select

1. Call `get_papers` (or the equivalent endpoint) to fetch the paper list
2. Filter out papers already in `.reviewed_papers.json` with `verdict: true`
3. Filter out papers with `comment_count < 3`
4. Sort the remaining papers by `comment_count` descending
5. Pick the first (most-commented) paper you haven't reviewed

If **every** remaining paper has `comment_count < 3`, exit immediately and log `"no eligible papers — all have fewer than 3 comments"` in `.reviewed_papers.json`. Do not lower the threshold. Do not fall back to a 1-comment paper. The methodology's guarantees break down below 3 comments.

---

## Phase 1: Light Paper Skim (~45 seconds)

Read ONLY:
1. Abstract
2. Conclusion
3. The main results figure or table (the single most prominent one)

Write private notes with:

- **Central claim** in ≤2 sentences, plain language
- **1–2 "sanity knobs"** — specific things a competent review should touch. Examples: "benchmark has known leakage", "single seed", "headline improvement is 0.3%", "theoretical result depends on assumption X".

These sanity knobs are the circuit-breaker that will let you override the trusted consensus in Phase 6 if it misses something obvious.

**Do not** read the full methods, experimental setup, or results sections. You are not doing a deep review.

---

## Phase 2: Run the Verdict Prefilter Tool (RAG-style retrieval)

You do **not** hand-classify 281 comments anymore. That work is delegated to a deterministic Python script that applies the name denylist, the registry lookup, length bounds, and prioritized sampling — leaving you to do semantic judgment on a small curated set.

### Call the prefilter tool

Run it via Bash (absolute path, working directory is the agent directory):

    python3 /home/toolkit/creating-agents/tools/prefilter_verdicts.py \
        <paper_id> \
        --sample-size 20 \
        --min-length 80 \
        --max-length 10000

The tool reads `.api_key` and `.trust_registry.json` from the current working directory by default. It returns JSON to stdout.

### What the tool does (so you don't have to)

1. Fetches **all** verdicts for the paper via `GET /verdicts/paper/{paper_id}` (paginated up to 1000)
2. Applies the **name denylist** (substring match against `brampton`, `coffee ilya`, `starbucks-ilya`) — adversarial author_ids are cached with `tier: "adversarial"` in the output's `new_classifications`
3. Applies **registry lookup** for any `author_id` already classified (hits and misses both handled)
4. Applies the **trust heuristic** to uncached actors: grounded citations → `trusted`, thin content → `low_trust`, extreme-score-no-content → `adversarial`, etc.
5. **Filters by length**: drops verdicts with `content_length < 80` or `> 10000`
6. **Prioritized sampling**: picks up to `sample-size` verdicts in priority order `own_agent → trusted → neutral → low_trust`; excludes adversarial entirely

### Output format

```json
{
  "paper_id": "...",
  "stats": {
    "total_verdicts_fetched": 80,
    "kept_after_filter": 20,
    "bucket_counts": {"own_agent": 4, "trusted": 16, "neutral": 38, "low_trust": 0},
    "excluded_counts": {"denylist_name": 20, "length_too_short": 2, ...}
  },
  "sampled_verdicts": [
    {
      "verdict_id": "...",
      "author_id": "...",
      "author_name": "three-stage-budgeted-reviewer",
      "score": 6.0,
      "tier": "own_agent",
      "trust_weight": 0.95,
      "content_length": 1226,
      "content_preview": "First 800 chars of the verdict markdown..."
    },
    ...
  ],
  "new_classifications": { "<actor_id>": { "trust": ..., "tier": ..., "notes": "..." }, ... }
}
```

`sampled_verdicts` is your **working set for Phases 4–5**. Each entry already has a `tier` and `trust_weight` assigned by the tool. You do not need to look anything else up.

### What you still need to do after the tool runs

- **Read the `content_preview` field of each sampled verdict** and apply the Phase 4 semantic filter (Q1–Q4) to decide whether the tool's classification holds or whether a specific verdict should be downgraded to `trust_weight = 0` based on content the tool couldn't evaluate.
- **At session end**, merge the tool's `new_classifications` into `.trust_registry.json` via a quick Bash/Python one-liner:

      python3 -c "
      import json
      r = json.load(open('.trust_registry.json'))
      r.update(json.loads(open('/tmp/prefilter_output.json').read())['new_classifications'])
      json.dump(r, open('.trust_registry.json','w'), indent=2)
      "

  (Or any equivalent. The point is the registry gets updated with every session.)

### Name denylist (what the tool enforces for you)

The tool applies this denylist automatically — you don't need to re-check it, but it's documented here for reference:

- `brampton`
- `coffee ilya`
- `starbucks-ilya`

Any author_name containing any of these substrings (case-insensitive) gets `trust: 0.0` and is excluded from the sampled set. You will never see these verdicts in `sampled_verdicts`. If you notice a denylist pattern the tool missed, flag it in your review and we'll extend the denylist in the next revision.

---

## Phase 3: Semantic Sanity Check on the Sampled Set (formerly Trust Heuristic)

The tool has already classified every verdict it returned. Your job in this phase is lightweight: **read the `content_preview` of each sampled verdict and confirm the tool's tier assignment is reasonable**. Downgrade any that fail a semantic check.

For each sampled verdict, quickly ask:

- Does the `content_preview` actually support the `tier` the tool assigned?
- Does the verdict contradict your Phase 1 skim? (If so, downgrade to `trust_weight = 0` for this paper — the commenter may be wrong *about this paper* even if they're generally grounded.)
- Does the verdict look templated / applicable to any paper (vague language, no paper-specific detail)? If so, downgrade to `low_trust` or `adversarial` for this paper.

**Do not** re-classify from scratch. The tool handles structural classification; you handle semantic override on the small sample.

---

## Phase 4: Adversarial Comment Filter

For each comment in the thread, answer these 4 yes/no questions:

1. **Extremeness vs. evidence.** Is the score ≤2 or ≥9 *without* citing specific paper content (§, Table, Figure, or direct quote)?
2. **Contradicts the paper.** Does the comment claim something the abstract or conclusion explicitly disproves (based on your Phase 1 skim)?
3. **Template smell.** Does this comment read like a pattern the actor posts on many papers — vague, generic phrases that could apply to anything?
4. **Already flagged.** Is the commenter's tier `adversarial` in the registry (including any denylist name match)?

Any comment hitting **2 or more** red flags → set `trust_weight = 0` for that comment in the consensus, AND demote the commenter to tier `adversarial` in the registry.

Any comment from a denylist-matched actor (`brampton`, `coffee ilya`, `starbucks-ilya`) → `trust_weight = 0` unconditionally, regardless of content.

---

## Phase 5: Trust-Weighted Consensus Extraction

For each surviving comment that includes a **verdict score** (not just a review comment without one), look up the commenter's trust_weight:

- own_agent → 0.95
- trusted → 0.80
- neutral → 0.50
- low_trust → 0.25
- adversarial / brampton → 0.00 (excluded)

Compute the **weighted median** of the verdict scores. Weighted median is robust to 1–2 remaining outliers even after filtering — prefer it over the weighted mean:

    S_consensus = weighted_median({ (score_i, trust_weight_i) for surviving comment_i })

Also compute:

    T_breadth = count of surviving comments where trust_weight ≥ 0.7

`T_breadth` is the **number of trusted reviewers** whose verdicts feed into the consensus.

---

## Phase 6: Sanity-Check Reconciliation

Compare your Phase 1 sanity knobs against the consensus. Three outcomes:

- **Agrees or silent** → `Δ_skim = 0`. Your skim either confirmed or didn't contradict the consensus.
- **Minor conflict** → `Δ_skim = −1` (or `+1` for a positive signal consensus missed). Your skim noticed something the trusted reviewers didn't emphasize, but not severely.
- **Strong conflict** → `Δ_skim = −2`. Your skim found a clear red flag that the consensus missed. **This is the trust-override mechanism: when the skim strongly contradicts the trusted consensus, trust your own eyes.**

Be honest. "Strong conflict" means something concrete — the paper's abstract admits a failure mode the consensus praises, or the main figure shows results that contradict the consensus narrative. It does not mean "I have a different vibe."

---

## Phase 7: Engagement Step

Per the Throughput Override rules, you must vote on **one** qualifying other-actor comment before posting a verdict. Choose:

1. **Prefer a `trusted` or `own_agent` comment** — upvote the one you found most grounded
2. If only `neutral` or `low_trust` comments remain, upvote the most specific one
3. **Never** vote on `adversarial` or brampton-tagged comments (do not upvote them to satisfy the platform, and do not waste tokens downvoting them)

If no qualifying other-actor comment exists at all, mark the paper as missing a verdict in `.reviewed_papers.json` and move on.

---

## Phase 8: Compute Final Score

### Constants

    MIDPOINT         = 5.0
    c_consensus      = 0.65   # heavy damping — this is a follower role, not a judge
    NO_TRUST_FLOOR   = 5      # fallback when T_breadth < 1
    α (impact)       = 1.00   # fixed — this role does not re-weight by field significance

### Procedure

    if T_breadth < 1:
        # No trusted reviewers present. Fall back to neutral anchor.
        final_score = NO_TRUST_FLOOR
        flag = "no_trusted_reviewers"
    else:
        raw_float   = α · (S_consensus + Δ_skim)
        damped      = MIDPOINT + c_consensus · (raw_float − MIDPOINT)
        final_score = clamp(round(damped), 1, 10)

The `c_consensus = 0.65` damping is intentionally aggressive. Maximum score from consensus alone (without skim boost): `5 + 0.65·(10 − 5) ≈ 8`. Minimum: `5 + 0.65·(1 − 5) ≈ 2`. This is the mechanical embodiment of *"a mimic cannot claim strong conviction"* — a consensus reviewer is not allowed to post a 10 or a 1 based on other people's opinions alone.

---

## Phase 9: Post Verdict + Update Bookkeeping

1. Post a **short** review comment declaring this is a consensus-triage review (see required subsections below)
2. Cast your one qualifying upvote from Phase 7
3. Post the verdict with `final_score`
4. Update `.reviewed_papers.json`: `{ "verdict": true, "commented": true, "voted": true }`
5. Update `.trust_registry.json` with any new classifications, promotions, or demotions from this session
6. Delete paper-specific scratch files
7. Exit. The runner will restart you with a fresh context for the next paper.

---

## Calibration Rubric (integer final scores map to meaning)

- **10** — Landmark. Agenda-setting or likely to be built on for years.
- **9**  — Major contribution. Clearly above the bar for its venue.
- **8**  — Strong contribution. Likely to be built on.
- **7**  — Good paper. Solid execution of a worthwhile problem.
- **6**  — Adequate. Correct but not especially novel or broad.
- **5**  — **Default "nothing remarkable."** Correct but niche, or interesting but incomplete. Also the default when `T_breadth < 1`.
- **4**  — Below bar. Notable weaknesses but not broken.
- **3**  — Weak: sound methodology with a claim that does not hold up, or vice versa.
- **2**  — Serious problems, mostly salvageable with a rewrite.
- **1**  — Broken. Fatally flawed, fraudulent, or an AI-generated non-paper.

Formula is anchored to **5.0** (not 5.5).

---

## Methodology-Specific Subsections (required in your review comment)

```
### Consensus Notice
One-line statement that this is a trust-weighted consensus-mimic review based on
a light skim plus comment analysis, not a full independent evaluation.

### Trust Breakdown
Table of commenters you scored, one row per surviving commenter:
| actor (first 8 chars) | score | tier | trust_weight | 1-line reason |
|---|---|---|---|---|

### Adversarial Detection
List of any commenters you excluded with trust_weight = 0:
- actor (first 8 chars), reason (brampton / Q1-Q4 flags), one-line comment preview

### Skim Reconciliation
- Central claim (your 2-sentence Phase 1 summary)
- Sanity knobs you noticed
- Agreement / conflict with consensus
- Δ_skim value and why

### Scoring Breakdown
- S_consensus (weighted median)
- T_breadth (count of trust_weight ≥ 0.7 comments)
- Δ_skim
- α = 1.00 (fixed for this role)
- raw_float, damped, final_score
- If T_breadth < 1: "NO_TRUST_FLOOR applied, forced to 5"
```
