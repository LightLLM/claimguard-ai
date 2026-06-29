# Maestro Case Flow

## Case Name

ClaimGuard AI Insurance Claim Review

## Case Stages

1. **New Claim Submitted**
   - Create case.
   - Attach submitted claim JSON and document metadata.

2. **Claim Intake**
   - Run Claim Intake Agent.
   - If required documents are missing, create human task: Request Missing Documents.

3. **Policy Verification**
   - Run Policy Verification Agent.
   - If policy is inactive, coverage is not confirmed, or claim exceeds coverage limit, create human task: Policy Exception Review.

4. **Fraud Signal Review**
   - Run Fraud Signal Agent.
   - If risk is high, create human task: SIU / Adjuster Review.
   - If risk is medium and claim amount is above 10000, create human task: Adjuster Review.

5. **Human Adjuster Decision**
   - Adjuster chooses approve, reject, request more documents, or escalate.
   - Decision reason is required.

6. **Settlement Recommendation**
   - Run Settlement Recommendation Agent.
   - Preserve human overrides and exception reasons.

7. **Audit Summary**
   - Run Audit Compliance Agent.
   - Attach final JSON summary to the case.
   - Close case or route to follow-up queue.

## Case Evidence

- Original claim
- Policy verification output
- Fraud signal output
- Human decision
- Final audit summary
