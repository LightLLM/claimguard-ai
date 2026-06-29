from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any


@dataclass
class ClaimGuardIn:
    scenario: str = "complete"
    claim: dict[str, Any] | None = None
    policy: dict[str, Any] | None = None
    human_decision: dict[str, Any] | None = None


@dataclass
class ClaimGuardOut:
    scenario: str
    claim_id: str
    fraud_signal: dict[str, Any]
    human_decision: dict[str, Any]
    audit_summary: dict[str, Any]


@dataclass
class UnitTestOut:
    passed: bool
    total: int
    failures: list[str]
    results: list[dict[str, Any]]


def _sample_claims() -> dict[str, dict[str, Any]]:
    return {
        "complete": {
            "claim_id": "CLM-2026-0001",
            "policy_id": "POL-77881",
            "claim_amount": 8400,
            "currency": "USD",
            "incident": {"type": "auto_collision", "date": "2026-05-18"},
            "claimant_history": {"claims_last_12_months": 1},
            "vendor_history": {"duplicate_invoice_detected": False},
            "intake_summary": {"missing_documents": [], "data_inconsistencies": []},
        },
        "missing_documents": {
            "claim_id": "CLM-2026-0002",
            "policy_id": "POL-77881",
            "claim_amount": 12600,
            "currency": "USD",
            "incident": {"type": "property_water_damage", "date": "2026-05-25"},
            "claimant_history": {"claims_last_12_months": 1},
            "vendor_history": {"duplicate_invoice_detected": False},
            "intake_summary": {
                "missing_documents": ["proof_of_loss", "repair_estimate"],
                "data_inconsistencies": [],
            },
        },
        "high_risk": {
            "claim_id": "CLM-2026-0003",
            "policy_id": "POL-99001",
            "claim_amount": 87500,
            "currency": "USD",
            "incident": {"type": "commercial_property_fire", "date": "2026-06-10"},
            "claimant_history": {"claims_last_12_months": 4},
            "vendor_history": {"duplicate_invoice_detected": True},
            "intake_summary": {
                "missing_documents": ["fire_department_report", "proof_of_loss"],
                "data_inconsistencies": [
                    "Vendor invoice total does not match claimed loss amount.",
                    "Incident location differs from primary insured address.",
                ],
            },
        },
    }


def _sample_policy(claim: dict[str, Any]) -> dict[str, Any]:
    if claim["policy_id"] == "POL-99001":
        return {
            "policy_id": "POL-99001",
            "status": "active",
            "coverage_limit": 75000,
            "start_date": "2026-06-01",
            "verification_result": {
                "coverage_confirmed": False,
                "exceptions": [
                    "Claim amount exceeds coverage limit.",
                    "Incident occurred within 14 days of policy start date.",
                ],
                "recommended_next_step": "route_to_human_adjuster_for_policy_exception",
            },
        }
    return {
        "policy_id": "POL-77881",
        "status": "active",
        "coverage_limit": 100000,
        "start_date": "2025-11-01",
        "verification_result": {
            "coverage_confirmed": True,
            "exceptions": [],
            "recommended_next_step": "continue_to_fraud_signal_review",
        },
    }


def _days_between(start_date: str, incident_date: str) -> int:
    return (date.fromisoformat(incident_date) - date.fromisoformat(start_date)).days


def _fraud_signal(claim: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    score = 0
    indicators: list[dict[str, Any]] = []
    intake = claim.get("intake_summary", {})

    def add_indicator(rule: str, points: int, detail: str) -> None:
        nonlocal score
        score += points
        indicators.append({"rule": rule, "points": points, "detail": detail})

    claim_amount = float(claim.get("claim_amount", 0))
    if claim_amount > 50000:
        add_indicator("claim_amount_above_50000", 25, f"Claim amount is {claim_amount:.2f}.")

    days_after_start = _days_between(policy["start_date"], claim["incident"]["date"])
    if 0 <= days_after_start <= 14:
        add_indicator(
            "incident_within_14_days_of_policy_start",
            20,
            f"Incident occurred {days_after_start} days after policy start.",
        )

    missing_documents = intake.get("missing_documents", [])
    if missing_documents:
        add_indicator("documents_missing", 20, f"Missing: {', '.join(missing_documents)}.")

    data_inconsistencies = intake.get("data_inconsistencies", [])
    if data_inconsistencies:
        add_indicator("data_inconsistencies_present", 20, f"{len(data_inconsistencies)} item(s) found.")

    claims_last_12_months = int(claim.get("claimant_history", {}).get("claims_last_12_months", 0))
    if claims_last_12_months > 2:
        add_indicator(
            "claimant_more_than_two_claims_last_12_months",
            15,
            f"Claimant has {claims_last_12_months} claims in the last 12 months.",
        )

    if bool(claim.get("vendor_history", {}).get("duplicate_invoice_detected", False)):
        add_indicator("duplicate_invoice_detected", 15, "Vendor invoice matched a prior invoice.")

    risk_level = "High" if score >= 60 else "Medium" if score >= 25 else "Low"
    human_review_required = risk_level == "High" or (risk_level == "Medium" and claim_amount > 10000)

    if human_review_required and risk_level == "High":
        next_step = "route_to_human_adjuster_and_siu_review"
    elif human_review_required:
        next_step = "route_to_human_adjuster_review"
    else:
        next_step = "continue_to_settlement_recommendation"

    return {
        "agent": "Fraud Signal Agent",
        "risk_score": score,
        "risk_level": risk_level,
        "risk_indicators": indicators,
        "human_review_required": human_review_required,
        "recommended_next_step": next_step,
        "audit_notes": ["Deterministic local rules; no paid APIs or secrets used."],
    }


def _human_decision(claim: dict[str, Any], fraud_signal: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    if override:
        return override

    missing_documents = claim.get("intake_summary", {}).get("missing_documents", [])
    if missing_documents:
        decision = "request_more_documents"
        reason = f"Required before settlement: {', '.join(missing_documents)}."
    elif fraud_signal["risk_level"] == "High":
        decision = "escalate_to_siu"
        reason = "High fraud risk requires special investigation review."
    else:
        decision = "approve"
        reason = "Coverage confirmed and fraud risk is acceptable."

    return {
        "reviewer": "UiPath Demo Adjuster",
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _audit_summary(
    claim: dict[str, Any],
    policy: dict[str, Any],
    fraud_signal: dict[str, Any],
    human_decision: dict[str, Any],
) -> dict[str, Any]:
    policy_result = policy["verification_result"]
    exceptions = [
        *policy_result.get("exceptions", []),
        *claim.get("intake_summary", {}).get("missing_documents", []),
        *[item["rule"] for item in fraud_signal.get("risk_indicators", [])],
    ]

    return {
        "agent": "Audit Compliance Agent",
        "audit_id": f"AUD-{claim['claim_id']}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_id": claim["claim_id"],
        "policy_id": claim["policy_id"],
        "timeline": [
            {"step": "claim_submitted", "actor": "Claimant", "status": "completed"},
            {"step": "claim_intake", "actor": "Claim Intake Agent", "status": "completed"},
            {"step": "policy_verification", "actor": "Policy Verification Agent", "status": "completed"},
            {"step": "fraud_signal_review", "actor": "Fraud Signal Agent", "status": "completed"},
            {"step": "human_review", "actor": human_decision.get("reviewer"), "status": human_decision.get("decision")},
        ],
        "decisions": {
            "policy_verification": policy_result,
            "fraud_signal": fraud_signal,
            "human_decision": human_decision,
        },
        "exceptions": exceptions,
        "human_approvals": [human_decision],
        "final_recommendation": human_decision.get("decision", "request_more_documents"),
        "audit_notes": ["Ready for UiPath Maestro Case evidence storage."],
    }


def _run_claim_guard(
    scenario: str,
    claim_override: dict[str, Any] | None = None,
    policy_override: dict[str, Any] | None = None,
    human_decision_override: dict[str, Any] | None = None,
) -> ClaimGuardOut:
    claim = claim_override or _sample_claims().get(scenario, _sample_claims()["complete"])
    policy = policy_override or _sample_policy(claim)
    fraud_signal = _fraud_signal(claim, policy)
    human_decision = _human_decision(claim, fraud_signal, human_decision_override)
    audit_summary = _audit_summary(claim, policy, fraud_signal, human_decision)

    return ClaimGuardOut(
        scenario=scenario,
        claim_id=claim["claim_id"],
        fraud_signal=fraud_signal,
        human_decision=human_decision,
        audit_summary=audit_summary,
    )


def main(input: ClaimGuardIn) -> ClaimGuardOut:
    return _run_claim_guard(input.scenario, input.claim, input.policy, input.human_decision)


def unit_tests() -> UnitTestOut:
    expectations = {
        "complete": {"risk_score": 0, "risk_level": "Low", "human_review_required": False, "decision": "approve"},
        "missing_documents": {
            "risk_score": 20,
            "risk_level": "Low",
            "human_review_required": False,
            "decision": "request_more_documents",
        },
        "high_risk": {
            "risk_score": 115,
            "risk_level": "High",
            "human_review_required": True,
            "decision": "request_more_documents",
        },
    }
    failures: list[str] = []
    results: list[dict[str, Any]] = []

    for scenario, expected in expectations.items():
        output = _run_claim_guard(scenario)
        fraud_signal = output.fraud_signal
        actual = {
            "scenario": scenario,
            "claim_id": output.claim_id,
            "risk_score": fraud_signal["risk_score"],
            "risk_level": fraud_signal["risk_level"],
            "human_review_required": fraud_signal["human_review_required"],
            "decision": output.human_decision["decision"],
            "final_recommendation": output.audit_summary["final_recommendation"],
            "exception_count": len(output.audit_summary["exceptions"]),
        }
        results.append(actual)

        for key, expected_value in expected.items():
            if actual[key] != expected_value:
                failures.append(f"{scenario}.{key}: expected {expected_value!r}, got {actual[key]!r}")

    return UnitTestOut(
        passed=not failures,
        total=len(expectations),
        failures=failures,
        results=results,
    )
