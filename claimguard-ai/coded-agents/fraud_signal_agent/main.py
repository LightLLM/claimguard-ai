"""Deterministic Fraud Signal Agent for ClaimGuard AI."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _days_between(start_date: str, incident_date: str) -> int:
    return (_parse_date(incident_date) - _parse_date(start_date)).days


def evaluate_fraud_signal(
    claim_intake_summary: dict[str, Any],
    policy_verification_result: dict[str, Any],
    claimant_history: dict[str, Any],
    vendor_history: dict[str, Any],
) -> dict[str, Any]:
    """Return JSON-serializable fraud risk output using demo-ready rules."""

    score = 0
    indicators: list[dict[str, Any]] = []

    claim_amount = float(claim_intake_summary.get("claim_amount", 0))
    missing_documents = claim_intake_summary.get("missing_documents", [])
    data_inconsistencies = claim_intake_summary.get("data_inconsistencies", [])
    incident_date = claim_intake_summary.get("incident_date")
    policy_start_date = policy_verification_result.get("policy_start_date")

    def add_indicator(rule: str, points: int, detail: str) -> None:
        nonlocal score
        score += points
        indicators.append({"rule": rule, "points": points, "detail": detail})

    if claim_amount > 50000:
        add_indicator("claim_amount_above_50000", 25, f"Claim amount is {claim_amount:.2f}.")

    if incident_date and policy_start_date:
        days_after_start = _days_between(policy_start_date, incident_date)
        if 0 <= days_after_start <= 14:
            add_indicator(
                "incident_within_14_days_of_policy_start",
                20,
                f"Incident occurred {days_after_start} days after policy start.",
            )

    if missing_documents:
        add_indicator("documents_missing", 20, f"Missing: {', '.join(missing_documents)}.")

    if data_inconsistencies:
        add_indicator(
            "data_inconsistencies_present",
            20,
            f"{len(data_inconsistencies)} inconsistency item(s) found.",
        )

    claims_last_12_months = int(claimant_history.get("claims_last_12_months", 0))
    if claims_last_12_months > 2:
        add_indicator(
            "claimant_more_than_two_claims_last_12_months",
            15,
            f"Claimant has {claims_last_12_months} claims in the last 12 months.",
        )

    if bool(vendor_history.get("duplicate_invoice_detected", False)):
        add_indicator("duplicate_invoice_detected", 15, "Vendor invoice matched a prior invoice.")

    if score >= 60:
        risk_level = "High"
    elif score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    human_review_required = risk_level == "High" or (risk_level == "Medium" and claim_amount > 10000)

    if human_review_required and risk_level == "High":
        recommended_next_step = "route_to_human_adjuster_and_siu_review"
    elif human_review_required:
        recommended_next_step = "route_to_human_adjuster_review"
    else:
        recommended_next_step = "continue_to_settlement_recommendation"

    return {
        "agent": "Fraud Signal Agent",
        "risk_score": score,
        "risk_level": risk_level,
        "risk_indicators": indicators,
        "human_review_required": human_review_required,
        "recommended_next_step": recommended_next_step,
        "audit_notes": [
            "Fraud score was calculated using deterministic local rules.",
            "No paid APIs, external data providers, or secrets were used.",
        ],
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _claim_to_inputs(claim: dict[str, Any], policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    intake = claim.get("intake_summary", {})
    return {
        "claim_intake_summary": {
            "claim_id": claim["claim_id"],
            "claim_amount": claim["claim_amount"],
            "incident_date": claim["incident"]["date"],
            "missing_documents": intake.get("missing_documents", []),
            "data_inconsistencies": intake.get("data_inconsistencies", []),
        },
        "policy_verification_result": {
            "policy_id": policy["policy_id"],
            "policy_status": policy["status"],
            "policy_start_date": policy["start_date"],
            "coverage_confirmed": policy["verification_result"]["coverage_confirmed"],
            "exceptions": policy["verification_result"].get("exceptions", []),
        },
        "claimant_history": claim.get("claimant_history", {}),
        "vendor_history": claim.get("vendor_history", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ClaimGuard AI Fraud Signal Agent.")
    parser.add_argument("--claim", required=True, help="Path to a claim JSON file.")
    parser.add_argument("--policy", required=True, help="Path to a policy JSON file.")
    args = parser.parse_args()

    inputs = _claim_to_inputs(_load_json(Path(args.claim)), _load_json(Path(args.policy)))
    result = evaluate_fraud_signal(**inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
