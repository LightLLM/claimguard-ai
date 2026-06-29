# Exception Paths

## Missing Documents

Trigger: Claim Intake Agent reports missing required documents.

Action: Maestro creates a human task to request documents from the claimant. The case waits until documents are received or the adjuster rejects the claim for non-compliance.

## Policy Exception

Trigger: Policy Verification Agent reports inactive policy, coverage mismatch, or claim amount above limit.

Action: Maestro routes to a policy exception review task. Adjuster must approve, reject, or escalate with a reason.

## Fraud Risk Exception

Trigger: Fraud Signal Agent reports high risk, or medium risk with claim amount above 10000.

Action: Maestro routes to human adjuster review. High-risk claims may be escalated to SIU.

## Agent Failure

Trigger: Agent output is malformed, unavailable, or violates schema.

Action: Maestro retries once, then routes to exception queue with raw payload attached as evidence.

## Audit Exception

Trigger: Final summary cannot be generated because a required decision is missing.

Action: Maestro reopens the required human task and prevents case closure until a decision is recorded.
