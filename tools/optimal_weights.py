#!/usr/bin/env python3
"""
Optimal scoring component weights for Day 2 agent configuration.

Derived from Ridge regression of internal scoring components against ICLR 2025
ground truth (avg_score from human reviewers). Only papers with actual review
scores (avg_score > 0) are used — 472 papers with missing reviews are excluded.

Key findings:
  - All agents exhibit severe positive bias (+0.8 to +1.9 points) and score
    compression (agents use 3-point range vs GT's 7-point range).
  - triage-then-deep has the best raw correlation (r=0.711, n=31) despite
    smaller sample size.
  - For consensus, S_consensus is the most informative component (r=0.455),
    and the component regression (R²=0.22) beats simple final_score (R²=0.13).
  - The damping step HELPS but the intercept needs shifting down by ~0.5.
  - For adaptive, final_score is paradoxically more predictive (r=0.58) than
    raw_float (r=0.25), suggesting the rounding captures useful discretization.

Usage:
    from optimal_weights import compute_optimal_score, calibrate_final_score

    # Component-level optimal score (if you have Scoring Breakdown components)
    score = compute_optimal_score({
        "S_consensus": 7.0, "T_breadth": 3, "damped": 6.3
    }, agent_type="consensus")

    # Simple calibration of final integer score
    score = calibrate_final_score(6, agent_type="triage_then_deep")
"""

import numpy as np
from typing import Optional

# ============================================================
# Ground truth statistics (ICLR 2025, non-zero scores only)
# ============================================================
GT_STATS = {
    "n": 690,
    "mean": 5.56,
    "std": 2.03,
    "min": 1.0,
    "max": 10.0,
    "median": 5.75,
    "p25": 3.75,
    "p75": 7.25,
}

# ============================================================
# Component-level regression coefficients
# Learned via Ridge(alpha=1.0) on non-zero GT papers only
# ============================================================

# CONSENSUS (trust-weighted-consensus, actor_id: 4aca4338)
# gt = 0.4411*S_consensus - 0.0787*T_breadth + 0.4920*damped - 0.2636
# R² = 0.2234, r = 0.485, n = 117
# Compared to final_score alone: R² = 0.1264, r = 0.356
CONSENSUS_COMPONENT_WEIGHTS = {
    "S_consensus": 0.4411,
    "T_breadth": -0.0787,
    "damped": 0.4920,
    "intercept": -0.2636,
}

# Simple S_consensus-only model (more robust, nearly as good)
# gt = 0.5876 * S_consensus + 1.4446
# R² = 0.2068, r = 0.455
CONSENSUS_SIMPLE = {
    "S_consensus": 0.5876,
    "intercept": 1.4446,
}

# ADAPTIVE (adaptive-triage-deep, actor_id: 0c0b0abb)
# gt = 1.400 * final_score - 4.054
# R² = 0.335, r = 0.579, n = 23
# Note: raw_float and S_base are NOT predictive (likely because they're
# computed deterministically from alpha * I_base, which compresses range)
ADAPTIVE_WEIGHTS = {
    "final_score": 1.400,
    "intercept": -4.054,
}

# TRIAGE-THEN-DEEP (actor_id: 8fd0f035) — BEST CORRELATOR
# gt = 0.862 * agent_score - 0.391
# R² = 0.505, r = 0.711, n = 31
# Uses wider score range (2-8) than other agents
TRIAGE_THEN_DEEP_WEIGHTS = {
    "final_score": 0.862,
    "intercept": -0.391,
}

# THREE-STAGE-BUDGETED (actor_id: 2af20618)
# Insufficient Scoring Breakdown data matched to GT (n=2).
# Use triage-then-deep calibration as proxy (same scoring formula family).
THREE_STAGE_WEIGHTS = TRIAGE_THEN_DEEP_WEIGHTS

# TRIAGE (actor_id: 6a944e9f)
# gt = 1.023 * agent_score - 0.352
# R² = 0.697, r = 0.835, n = 5 (CAUTION: very small sample)
TRIAGE_WEIGHTS = {
    "final_score": 1.023,
    "intercept": -0.352,
}

# PREREGISTRATION (actor_id: 5358e57f)
# gt = 0.686 * agent_score + 0.465
# R² = 0.260, r = 0.510, n = 20
PREREGISTRATION_WEIGHTS = {
    "final_score": 0.686,
    "intercept": 0.465,
}

# ============================================================
# Per-agent final score calibration (updated from non-zero GT)
# Format: gt = coef * agent_score + intercept
# ============================================================
FINAL_SCORE_CALIBRATIONS = {
    "triage_then_deep":     {"coef": 0.862, "intercept": -0.391, "r": 0.711, "n": 31},
    "triage":               {"coef": 1.023, "intercept": -0.352, "r": 0.835, "n": 5},
    "preregistration":      {"coef": 0.686, "intercept":  0.465, "r": 0.510, "n": 20},
    "consensus":            {"coef": 0.950, "intercept": -0.493, "r": 0.392, "n": 163},
    "adaptive":             {"coef": 1.181, "intercept": -3.114, "r": 0.369, "n": 45},
    "three_stage_budgeted": {"coef": 0.862, "intercept": -0.391, "r": 0.711, "n": 31},  # proxy
    "light_triage":         {"coef": 0.702, "intercept":  0.861, "r": 0.365, "n": 21},
}


def compute_optimal_score(components: dict, agent_type: str) -> float:
    """
    Given internal components from an agent's review, compute the
    regression-optimal score.

    Args:
        components: dict of component values. Keys depend on agent_type:
            - consensus: S_consensus, T_breadth, damped (or just S_consensus)
            - adaptive: final_score (or raw_float, I_base, alpha)
            - triage_then_deep/three_stage_budgeted: final_score
              (or S_1_internal, S_1_external, S_2_internal, S_2_external,
               delta_syn, alpha, c)
            - triage: final_score (or I_base, alpha, probe_delta)
        agent_type: one of "consensus", "adaptive", "triage_then_deep",
            "three_stage_budgeted", "triage", "preregistration"

    Returns:
        Calibrated score (float, clamped to 1-10 range)
    """
    if agent_type == "consensus":
        return _compute_consensus(components)
    elif agent_type == "adaptive":
        return _compute_adaptive(components)
    elif agent_type in ("triage_then_deep", "three_stage_budgeted", "three_stage"):
        return _compute_three_stage(components)
    elif agent_type == "triage":
        return _compute_triage(components)
    elif agent_type == "preregistration":
        return _compute_preregistration(components)
    else:
        # Fall back to simple final_score calibration
        if "final_score" in components:
            return calibrate_final_score(components["final_score"], "consensus")
        raise ValueError(f"Unknown agent_type: {agent_type}")


def calibrate_final_score(score: float, agent_type: str) -> float:
    """
    Simple linear calibration of a final integer score.
    Use this when you only have the agent's final score (no component breakdown).

    Args:
        score: the agent's final score (1-10 integer typically)
        agent_type: agent identifier

    Returns:
        Calibrated score (float, clamped to 1-10 range)
    """
    cal = FINAL_SCORE_CALIBRATIONS.get(agent_type)
    if cal is None:
        # Default: use consensus calibration
        cal = FINAL_SCORE_CALIBRATIONS["consensus"]

    result = cal["coef"] * score + cal["intercept"]
    return _clamp(result)


def _compute_consensus(components: dict) -> float:
    """Consensus component regression."""
    if all(k in components for k in ["S_consensus", "T_breadth", "damped"]):
        w = CONSENSUS_COMPONENT_WEIGHTS
        result = (w["S_consensus"] * components["S_consensus"]
                  + w["T_breadth"] * components["T_breadth"]
                  + w["damped"] * components["damped"]
                  + w["intercept"])
    elif "S_consensus" in components:
        w = CONSENSUS_SIMPLE
        result = w["S_consensus"] * components["S_consensus"] + w["intercept"]
    elif "final_score" in components:
        return calibrate_final_score(components["final_score"], "consensus")
    elif "damped" in components:
        # Fallback: damped alone
        result = 1.100 * components["damped"] - 1.139
    else:
        raise ValueError("Consensus needs at least S_consensus, damped, or final_score")
    return _clamp(result)


def _compute_adaptive(components: dict) -> float:
    """Adaptive component regression."""
    if "final_score" in components:
        w = ADAPTIVE_WEIGHTS
        result = w["final_score"] * components["final_score"] + w["intercept"]
    elif "raw_float" in components:
        # raw_float is weakly predictive, but available
        result = -0.124 * components["raw_float"] + 5.614
    else:
        raise ValueError("Adaptive needs final_score or raw_float")
    return _clamp(result)


def _compute_three_stage(components: dict) -> float:
    """Three-stage-budgeted / triage-then-deep regression.

    With only 2 GT-matched Scoring Breakdowns, we can't do proper component
    regression. Use final_score calibration instead. If component-level data
    becomes available, the recommended formula based on the scoring structure is:

        optimal = 0.86 * (w1*S_1 + w2*S_2 + delta_syn) - 0.39

    where the 0.86 slope and -0.39 intercept come from the final_score calibration.
    """
    if "final_score" in components:
        return calibrate_final_score(components["final_score"], "triage_then_deep")
    elif "S_areas" in components:
        # Use S_areas + delta_syn as proxy for final_score
        raw = components["S_areas"] + components.get("delta_syn", 0)
        return calibrate_final_score(round(raw), "triage_then_deep")
    elif "damped" in components:
        return calibrate_final_score(round(components["damped"]), "triage_then_deep")
    else:
        raise ValueError("Three-stage needs final_score, S_areas, or damped")


def _compute_triage(components: dict) -> float:
    """Triage reviewer regression."""
    if "final_score" in components:
        return calibrate_final_score(components["final_score"], "triage")
    elif "I_base" in components:
        # Approximate: triage final_score ~ round(I_base + probe_delta)
        raw = components["I_base"] + components.get("probe_delta", 0)
        return calibrate_final_score(round(raw), "triage")
    else:
        raise ValueError("Triage needs final_score or I_base")


def _compute_preregistration(components: dict) -> float:
    """Preregistration reviewer regression."""
    if "final_score" in components:
        return calibrate_final_score(components["final_score"], "preregistration")
    else:
        raise ValueError("Preregistration needs final_score")


def _clamp(score: float, lo: float = 1.0, hi: float = 10.0) -> float:
    """Clamp score to valid range."""
    return round(max(lo, min(hi, score)), 2)


# ============================================================
# Ensemble: combine calibrated scores from multiple agents
# ============================================================

def ensemble_calibrate(agent_scores: dict) -> float:
    """
    Given scores from multiple agents for the same paper, produce
    an ensemble calibrated score.

    Args:
        agent_scores: dict of {agent_type: final_score}
            e.g. {"consensus": 6, "triage_then_deep": 7, "adaptive": 7}

    Returns:
        Ensemble calibrated score (weighted average by correlation strength)
    """
    calibrated = []
    weights = []
    for agent_type, score in agent_scores.items():
        cal = FINAL_SCORE_CALIBRATIONS.get(agent_type)
        if cal is None:
            continue
        cs = calibrate_final_score(score, agent_type)
        calibrated.append(cs)
        # Weight by r² (squared correlation = variance explained)
        weights.append(cal["r"] ** 2)

    if not calibrated:
        raise ValueError("No known agents in input")

    weights = np.array(weights) / sum(weights)
    result = sum(w * s for w, s in zip(weights, calibrated))
    return _clamp(result)


# ============================================================
# Day 2 recommended scoring formulas
# ============================================================

DAY2_RECOMMENDATIONS = """
DAY 2 SCORING RECOMMENDATIONS
==============================

1. CONSENSUS AGENT (best volume, r=0.39 -> component r=0.49):
   Replace: final_score = round(damped)
   With:    final_score = round(0.44*S_consensus - 0.08*T_breadth + 0.49*damped - 0.26)
   Or simpler: final_score = round(0.59*S_consensus + 1.44)

   Key insight: S_consensus alone is a better predictor than the full
   damped -> rounded pipeline. The damping OVER-corrects toward 5.0.
   Reduce damping coefficient from current level, or remove it entirely
   and use S_consensus directly.

2. TRIAGE-THEN-DEEP (best correlation, r=0.71):
   Current formula works well! Just apply linear recalibration:
   calibrated = 0.86 * final_score - 0.39

   Key insight: This agent uses the widest score range (2-8), which
   is why it correlates best. Encourage WIDER score spread in other agents.

3. ADAPTIVE AGENT (r=0.37 -> r=0.58 with calibration):
   Apply: calibrated = 1.18 * final_score - 3.11

   Problem: 60% of scores are exactly 7, 38% are exactly 6.
   Score range is only 5-8. Need to REDUCE positive bias and
   INCREASE score spread. Suggested: lower the damping anchor from 5.0
   to 4.5, and reduce alpha multiplier range.

4. UNIVERSAL FIX - REDUCE POSITIVE BIAS:
   All agents are biased +0.8 to +1.9 points above GT.
   The damping formula "5.0 + c*(raw - 5.0)" anchors scores toward 5.0,
   but GT mean is 5.56 with many papers at 3-4.

   Recommended: Change damping anchor to 4.5 or remove damping entirely
   for the deep review agents.

5. UNIVERSAL FIX - INCREASE SCORE SPREAD:
   Agent std is 0.5-0.7 vs GT std of 2.03.
   Most agents cluster in a 3-point range (5-7).

   Recommended: After computing raw_float, apply a spread correction:
   adjusted = GT_MEAN + (raw_float - agent_mean) * (GT_STD / agent_std)
   This maps the agent's distribution to match GT spread.
"""


def apply_spread_correction(score: float, agent_type: str) -> float:
    """
    Apply distribution-matching spread correction.
    Maps agent scores to have GT-like mean and spread.
    """
    # Agent statistics (from Day 1 reviewed_papers.json)
    AGENT_STATS = {
        "consensus":            {"mean": 5.56, "std": 0.68},
        "triage_then_deep":     {"mean": 6.22, "std": 1.06},
        "adaptive":             {"mean": 6.61, "std": 0.53},
        "three_stage_budgeted": {"mean": 5.86, "std": 1.00},
        "preregistration":      {"mean": 7.14, "std": 0.90},
        "light_triage":         {"mean": 5.80, "std": 0.90},
        "triage":               {"mean": 5.75, "std": 1.50},
    }

    stats = AGENT_STATS.get(agent_type)
    if stats is None:
        return score

    # Z-score transform then map to GT distribution
    z = (score - stats["mean"]) / max(stats["std"], 0.1)
    adjusted = GT_STATS["mean"] + z * GT_STATS["std"]
    return _clamp(adjusted)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Compute optimal calibrated review scores")
    parser.add_argument("--components", type=str,
                        help='JSON dict of component values')
    parser.add_argument("--agent-type", type=str, required=True,
                        help="Agent type (consensus, adaptive, triage_then_deep, etc.)")
    parser.add_argument("--score", type=float,
                        help="Simple final score to calibrate")
    parser.add_argument("--spread-correct", action="store_true",
                        help="Apply spread correction to match GT distribution")
    parser.add_argument("--recommendations", action="store_true",
                        help="Print Day 2 recommendations")

    args = parser.parse_args()

    if args.recommendations:
        print(DAY2_RECOMMENDATIONS)
    elif args.components:
        components = json.loads(args.components)
        score = compute_optimal_score(components, args.agent_type)
        if args.spread_correct:
            score = apply_spread_correction(score, args.agent_type)
        print(f"{score:.2f}")
    elif args.score is not None:
        score = calibrate_final_score(args.score, args.agent_type)
        if args.spread_correct:
            score = apply_spread_correction(score, args.agent_type)
        print(f"{score:.2f}")
    else:
        parser.print_help()
