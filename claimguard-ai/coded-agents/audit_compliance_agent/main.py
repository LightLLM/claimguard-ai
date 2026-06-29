"""Audit Compliance Agent for ClaimGuard AI."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def generate_audit_summary(
    claim: dict[str, Any],
    policy_verification: dict[str, Any],
    fraud_signal: dict[str, Any],
    human_decision: dict[str, Any],
) -> dict[str, Any]:
    """Create a JSON-serializable final case audit summary."""

    policy_result = policy_verification.get("verification_result", policy_verification)
    exceptions = []
    exceptions.extend(policy_result.get("exceptions", []))
    exceptions.extend(claim.get("intake_summary", {}).get("missing_documents", []))
    exceptions.extend(item.get("rule", "") for item in fraud_signal.get("risk_indicators", []))
    exceptions = [item for item in exceptions if item]

    timeline = [
        {
            "step": "claim_submitted",
            "actor": "Claimant",
            "status": "completed",
            "details": f"Claim {claim['claim_id']} submitted for {claim['claim_amount']} {claim.get('currency', 'USD')}.",
        },
        {
            "step": "claim_intake",
            "actor": "Claim Intake Agent",
            "status": "completed",
            "details": "Required documents and claim fields were checked.",
        },
        {
            "step": "policy_verification",
            "actor": "Policy Verification Agent",
            "status": "completed",
            "details": policy_result.get("recommended_next_step", "policy_checked"),
        },
        {
            "step": "fraud_signal_review",
            "actor": "Fraud Signal Agent",
            "status": "completed",
            "details": f"Risk level {fraud_signal['risk_level']} with score {fraud_signal['risk_score']}.",
        },
        {
            "step": "human_review",
            "actor": human_decision.get("reviewer", "Human Adjuster"),
            "status": human_decision.get("decision", "pending"),
            "details": human_decision.get("reason", "Human review decision recorded."),
        },
    ]

    final_recommendation = human_decision.get("decision", "request_more_documents")
    if final_recommendation == "approve" and fraud_signal.get("risk_level") == "High":
        final_recommendation = "approve_with_siu_monitoring"

    return {
        "agent": "Audit Compliance Agent",
        "audit_id": f"AUD-{claim['claim_id']}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_id": claim["claim_id"],
        "policy_id": claim["policy_id"],
        "timeline": timeline,
        "decisions": {
            "policy_verification": policy_result,
            "fraud_signal": {
                "risk_score": fraud_signal["risk_score"],
                "risk_level": fraud_signal["risk_level"],
                "human_review_required": fraud_signal["human_review_required"],
                "recommended_next_step": fraud_signal["recommended_next_step"],
            },
            "human_decision": human_decision,
        },
        "exceptions": exceptions,
        "human_approvals": [
            {
                "reviewer": human_decision.get("reviewer", "Human Adjuster"),
                "decision": human_decision.get("decision", "pending"),
                "timestamp": human_decision.get("timestamp"),
            }
        ],
        "final_recommendation": final_recommendation,
        "audit_notes": [
            "Every major agent output is preserved in the case summary.",
            "This summary is JSON serializable and ready for UiPath case evidence storage.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ClaimGuard AI Audit Compliance Agent.")
    parser.add_argument("--claim", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--fraud", required=True)
    parser.add_argument("--human-decision", required=True)
    args = parser.parse_args()

    result = generate_audit_summary(
        json.loads(Path(args.claim).read_text(encoding="utf-8")),
        json.loads(Path(args.policy).read_text(encoding="utf-8")),
        json.loads(Path(args.fraud).read_text(encoding="utf-8")),
        json.loads(Path(args.human_decision).read_text(encoding="utf-8")),
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
