"""Run a local ClaimGuard AI demo without external services."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fraud_agent = _load_module("fraud_signal_agent", ROOT / "coded-agents" / "fraud_signal_agent" / "main.py")
audit_agent = _load_module("audit_compliance_agent", ROOT / "coded-agents" / "audit_compliance_agent" / "main.py")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _select_policy(claim: dict[str, Any]) -> Path:
    if claim["policy_id"] == "POL-99001":
        return ROOT / "data" / "sample-policy-exception.json"
    return ROOT / "data" / "sample-policy-active.json"


def _build_fraud_inputs(claim: dict[str, Any], policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    intake = claim["intake_summary"]
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


def _mock_human_decision(fraud_signal: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    missing_documents = claim.get("intake_summary", {}).get("missing_documents", [])
    if missing_documents:
        decision = "request_more_documents"
        reason = f"Required before settlement: {', '.join(missing_documents)}."
    elif fraud_signal["risk_level"] == "High":
        decision = "escalate_to_siu"
        reason = "High fraud risk requires special investigation review."
    else:
        decision = "approve"
        reason = "Coverage confirmed and fraud risk is acceptable for straight-through settlement."

    return {
        "reviewer": "Demo Adjuster",
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def run_demo(claim_path: Path) -> dict[str, Any]:
    claim = _load_json(claim_path)
    policy = _load_json(_select_policy(claim))
    fraud_signal = fraud_agent.evaluate_fraud_signal(**_build_fraud_inputs(claim, policy))
    human_decision = _mock_human_decision(fraud_signal, claim)
    audit_summary = audit_agent.generate_audit_summary(claim, policy, fraud_signal, human_decision)

    return {
        "scenario": claim_path.name,
        "claim": {
            "claim_id": claim["claim_id"],
            "policy_id": claim["policy_id"],
            "claim_amount": claim["claim_amount"],
        },
        "fraud_signal": fraud_signal,
        "human_decision": human_decision,
        "audit_summary": audit_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ClaimGuard AI local demo.")
    parser.add_argument(
        "--claim",
        default=str(ROOT / "data" / "sample-claim-complete.json"),
        help="Path to a sample claim JSON file.",
    )
    args = parser.parse_args()
    result = run_demo(Path(args.claim).resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
