# Human Review Flow

## Human Task Fields

- Claim ID
- Policy ID
- Claim amount
- Exception reason
- Fraud risk level
- Risk indicators
- Recommended next step
- Adjuster decision
- Decision reason
- Attachments requested

## Decision Options

- Approve
- Reject
- Request more documents
- Escalate to SIU
- Escalate to policy specialist

## Required Controls

- Decision reason is mandatory.
- High-risk approvals require a second approval or SIU monitoring note.
- Missing-document cases cannot be approved until the document request is resolved or overridden.

## Audit Handling

The adjuster, decision, timestamp, and reason are passed to the Audit Compliance Agent and included in the final summary.
