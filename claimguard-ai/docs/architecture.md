# Architecture

ClaimGuard AI uses UiPath Automation Cloud as the orchestration and governance layer for a multi-agent insurance claim workflow.

## Components

- **UiPath Maestro Case**: Case state, queues, routing, human tasks, exceptions, and audit trail.
- **UiPath Agent Builder**: Agent definitions for intake, policy verification, fraud review, settlement recommendation, and audit summary.
- **Coded Agents**: Local Python logic for deterministic fraud scoring and audit summary generation.
- **JSON Schemas**: UiPath-friendly contracts for agent input and output payloads.
- **Sample Data**: Demo scenarios covering complete, missing-document, and high-risk claims.

## Data Flow

1. Claim payload enters a Maestro Case.
2. Claim Intake Agent validates fields and documents.
3. Policy Verification Agent checks coverage and exceptions.
4. Fraud Signal Agent scores risk using deterministic rules.
5. Maestro routes exceptions to human adjuster tasks.
6. Settlement Recommendation Agent proposes an action.
7. Audit Compliance Agent generates the final case record.

## Governance

Each agent output becomes case evidence. Human decisions are stored with reviewer, timestamp, decision, and reason. Exceptions never disappear; they remain in the final audit summary.
