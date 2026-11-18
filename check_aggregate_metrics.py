#!/usr/bin/env python3
"""Recalculate allowed aggregate vaccine immunogenicity metrics.

This script accepts aggregate inputs only. It must not be used with subject-level
records. It produces arithmetic checks, not a regulatory or medical conclusion.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    if numerator < 0 or numerator > denominator:
        raise ValueError("numerator must be between 0 and denominator")
    return numerator / denominator


def gmean_from_log(mean_log: float, log_base: str) -> float:
    if log_base == "e":
        return math.exp(mean_log)
    if log_base == "10":
        return 10**mean_log
    raise ValueError("log_base must be 'e' or '10'")


def vaccine_efficacy(vaccine_measure: float, control_measure: float) -> float:
    if vaccine_measure < 0 or control_measure <= 0:
        raise ValueError("measures must be non-negative and control must be positive")
    return 1 - vaccine_measure / control_measure


def calculate(item: dict) -> dict:
    metric = item.get("metric")
    if metric in {"seroprotection_rate", "seropositivity_rate", "seroconversion_rate"}:
        value = rate(int(item["numerator"]), int(item["denominator"]))
        return {"metric": metric, "proportion": value, "percent": 100 * value}
    if metric in {"gmt", "gmc", "gmi", "gmfr"}:
        value = gmean_from_log(float(item["mean_log"]), str(item.get("log_base", "e")))
        return {"metric": metric, "value": value, "log_base": item.get("log_base", "e")}
    if metric == "gmr":
        base = str(item.get("log_base", "e"))
        test = gmean_from_log(float(item["test_mean_log"]), base)
        control = gmean_from_log(float(item["control_mean_log"]), base)
        return {"metric": metric, "value": test / control, "direction": "test/control"}
    if metric == "vaccine_efficacy":
        value = vaccine_efficacy(float(item["vaccine_measure"]), float(item["control_measure"]))
        return {"metric": metric, "proportion": value, "percent": 100 * value}
    raise ValueError(f"unsupported metric: {metric!r}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check aggregate vaccine metrics; subject-level inputs are prohibited."
    )
    parser.add_argument("input", type=Path, help="JSON file containing a list of aggregate metric objects")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("input JSON must be a list")
    print(json.dumps([calculate(item) for item in payload], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
