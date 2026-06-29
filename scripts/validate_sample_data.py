"""Lightweight validation for ClaimGuard AI sample data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLAIM_REQUIRED_FIELDS = {
    "claim_id",
    "policy_id",
    "claimant",
    "incident",
    "claim_amount",
    "currency",
    "documents",
    "claimant_history",
    "vendor_history",
    "intake_summary",
}

POLICY_REQUIRED_FIELDS = {
    "policy_id",
    "status",
    "coverage_types",
    "coverage_limit",
    "deductible",
    "start_date",
    "end_date",
    "verification_result",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate(path: Path, required_fields: set[str]) -> None:
    data = _load(path)
    missing = sorted(required_fields - set(data))
    if missing:
        raise ValueError(f"{path.name} missing required fields: {missing}")


def main() -> None:
    for claim_file in ROOT.glob("data/sample-claim-*.json"):
        _validate(claim_file, CLAIM_REQUIRED_FIELDS)
    for policy_file in ROOT.glob("data/sample-policy-*.json"):
        _validate(policy_file, POLICY_REQUIRED_FIELDS)
    print("Sample data validation passed.")


if __name__ == "__main__":
    main()
