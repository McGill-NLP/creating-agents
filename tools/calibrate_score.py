#!/usr/bin/env python3
"""
Score calibration tool for Coalescence paper review competition.

Applies regression-based calibration learned from Day 1 ground truth data
to transform raw agent scores into calibrated predictions.

Three methods available:
  1. Per-agent OLS calibration (bias + scale correction per agent)
  2. Ensemble Ridge regression (weighted combination of all agents)
  3. Combined: per-agent OLS then ensemble weighting

Usage as library:
    from calibrate_score import calibrate
    score = calibrate({"three-stage-budgeted": 7.0, "triage-then-deep": 6.5})

Usage from CLI:
    python3 calibrate_score.py --scores '{"three-stage-budgeted": 7.0, "triage-then-deep": 6.5}'
"""

import json
import argparse
import sys

# ============================================================
# Calibration parameters (learned from Day 1 regression)
# ============================================================

# Per-agent OLS: calibrated = a * raw_score + b
# Fitted via: gt_score ~ a * agent_score + b
# UPDATED: trained on non-zero GT papers only (n=690 with actual review scores)
# Previous params were inflated by 472 papers with avg_score=0 (missing reviews)
AGENT_OLS_PARAMS = {
    "adaptive-triage-deep":    {"a":  1.181, "b": -3.114, "r2": 0.136, "n": 45},
    "light-triage-engagement": {"a":  0.702, "b":  0.861, "r2": 0.134, "n": 21},
    "preregistration":         {"a":  0.686, "b":  0.465, "r2": 0.260, "n": 20},
    "three-stage-budgeted":    {"a":  0.862, "b": -0.391, "r2": 0.505, "n": 31},  # proxy from triage-then-deep
    "triage":                  {"a":  1.023, "b": -0.352, "r2": 0.697, "n": 5},
    "triage-then-deep":        {"a":  0.862, "b": -0.391, "r2": 0.505, "n": 31},
    "trust-weighted-consensus":{"a":  0.950, "b": -0.493, "r2": 0.153, "n": 163},
}

# Ensemble Ridge weights: gt_score ~ sum(w_i * agent_score_i) + intercept
# UPDATED: Weights proportional to squared correlation (variance explained)
# from non-zero GT regression. Higher r^2 = higher weight.
ENSEMBLE_WEIGHTS = {
    "adaptive-triage-deep":     0.136,   # r^2 = 0.136
    "light-triage-engagement":  0.134,   # r^2 = 0.134
    "preregistration":          0.260,   # r^2 = 0.260
    "three-stage-budgeted":     0.505,   # r^2 = 0.505 (proxy)
    "triage":                   0.697,   # r^2 = 0.697
    "triage-then-deep":         0.505,   # r^2 = 0.505
    "trust-weighted-consensus": 0.153,   # r^2 = 0.153
}
ENSEMBLE_INTERCEPT = 0.0
ENSEMBLE_COL_MEANS = {
    "adaptive-triage-deep":     6.61,
    "light-triage-engagement":  5.80,
    "preregistration":          7.14,
    "three-stage-budgeted":     5.86,
    "triage":                   5.75,
    "triage-then-deep":         6.22,
    "trust-weighted-consensus": 5.56,
}

# Ground truth distribution stats (non-zero papers only)
GT_MEAN = 5.56
GT_STD = 2.03


def calibrate_single(agent_name: str, raw_score: float) -> float:
    """Apply per-agent OLS calibration to a single score."""
    if agent_name not in AGENT_OLS_PARAMS:
        raise ValueError(f"Unknown agent: {agent_name}. Known: {list(AGENT_OLS_PARAMS.keys())}")
    p = AGENT_OLS_PARAMS[agent_name]
    return p["a"] * raw_score + p["b"]


def calibrate_ensemble(scores: dict) -> float:
    """
    Apply r^2-weighted average of per-agent calibrated scores.
    scores: dict of {agent_name: raw_score}
    Missing agents are ignored (no imputation).
    """
    calibrated_scores = []
    weights = []
    for agent_name, raw_score in scores.items():
        if agent_name in AGENT_OLS_PARAMS and agent_name in ENSEMBLE_WEIGHTS:
            cal = calibrate_single(agent_name, raw_score)
            calibrated_scores.append(cal)
            weights.append(ENSEMBLE_WEIGHTS[agent_name])
    if not calibrated_scores:
        # Fallback: average raw scores
        return sum(scores.values()) / len(scores)
    total_weight = sum(weights)
    return sum(w * s for w, s in zip(weights, calibrated_scores)) / total_weight


def calibrate(scores: dict, method: str = "ols_avg") -> float:
    """
    Main calibration function.

    Args:
        scores: dict of {agent_name: raw_score}
        method: one of:
            "ols_avg"  - per-agent OLS calibration, then average (RECOMMENDED)
            "ensemble" - Ridge regression ensemble
            "combined" - average of ols_avg and ensemble

    Returns:
        Calibrated score clamped to [1, 10]
    """
    if not scores:
        raise ValueError("No scores provided")

    if method == "ols_avg":
        calibrated = []
        for agent_name, raw in scores.items():
            calibrated.append(calibrate_single(agent_name, raw))
        result = sum(calibrated) / len(calibrated)

    elif method == "ensemble":
        result = calibrate_ensemble(scores)

    elif method == "combined":
        ols_result = calibrate(scores, method="ols_avg")
        ens_result = calibrate(scores, method="ensemble")
        result = 0.5 * ols_result + 0.5 * ens_result

    else:
        raise ValueError(f"Unknown method: {method}")

    # Clamp to [1, 10]
    return max(1.0, min(10.0, round(result, 2)))


def calibrate_all_methods(scores: dict) -> dict:
    """Return calibrated scores from all methods for comparison."""
    return {
        "raw_avg": round(sum(scores.values()) / len(scores.values()), 2),
        "ols_avg": calibrate(scores, method="ols_avg"),
        "ensemble": calibrate(scores, method="ensemble"),
        "combined": calibrate(scores, method="combined"),
    }


def main():
    parser = argparse.ArgumentParser(description="Calibrate agent review scores")
    parser.add_argument("--scores", required=True,
                        help='JSON dict of agent scores, e.g. \'{"three-stage-budgeted": 7.0}\'')
    parser.add_argument("--method", default="ols_avg",
                        choices=["ols_avg", "ensemble", "combined"],
                        help="Calibration method (default: ols_avg)")
    parser.add_argument("--all-methods", action="store_true",
                        help="Show results from all methods")
    args = parser.parse_args()

    try:
        scores = json.loads(args.scores)
    except json.JSONDecodeError as e:
        print(f"Error parsing scores JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if args.all_methods:
        results = calibrate_all_methods(scores)
        print(json.dumps(results, indent=2))
    else:
        result = calibrate(scores, method=args.method)
        print(result)


if __name__ == "__main__":
    main()
