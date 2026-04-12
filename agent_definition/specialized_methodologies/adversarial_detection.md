# Review Methodology: Adversarial Detection + Score Synthesis

## Phase 1: Tampering Check (~60 seconds)

Read the paper text at `day2_intel/papers/text/<PAPER_ID>.txt` (in the repo root's parent).

Scan for red flags:
1. Read abstract -- note key claims
2. Jump to results/conclusion -- do they support the abstract?
3. Scan for impossible numbers (>100%, negative where impossible)
4. Look for notation/style breaks (different terminology, British/American mixing, transplanted domain references)
5. Check if methodology matches what results evaluate

## Phase 2: Score Decision

**If 2+ red flags**: Score 0-2. Your review should list the specific flags with section/page references.

**If 1 red flag**: Score 2-4. Note the flag but indicate it may be an honest error.

**If 0-1 red flags**: Read other agents' scores from `.other_agent_scores.json`. Compute weighted score:
- triage-then-deep weight: 0.45
- three-stage-budgeted weight: 0.30
- preregistration weight: 0.25
- If an agent has not reviewed this paper, redistribute its weight proportionally to the others

Apply the ICLR ground truth anchors:
- Rejected papers average 2.39
- Accepted orals average 7.82
- Use the full 0-10 range

## Phase 3: Review Assembly

Your review comment should include:

### Tampering Analysis
- Red flags found (or "None found")
- For each flag: what you found, where in the paper, and why it is suspicious

### Score Derivation
- If tampered: which flags fired, severity assessment, final score
- If clean: other agents' scores, weights used, weighted average, any adjustment and why

### Verdict
- Final score with brief justification
- Map to ICLR ground truth anchor: where does this paper sit?

## Methodology-Specific Subsections

```
### Tampering Checklist
- [ ] Abstract-results mismatch
- [ ] Internal contradictions
- [ ] Transplanted text / wrong-domain references
- [ ] Impossible numbers
- [ ] Style/terminology breaks
- [ ] Figure-caption mismatches
- [ ] Unsupporting references

### Tampering Verdict
One of: CLEAN (0 flags) | SUSPICIOUS (1 flag) | TAMPERED (2+ flags)

### Score Derivation
If clean: weighted synthesis from other agents' reviews
If tampered: direct score based on severity

### Final Score
X.X / 10 -- [brief anchor mapping]
```
