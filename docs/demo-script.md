# 5-Minute Demo Script

## 0:00-0:30 Problem

Insurance claims move across documents, policies, vendors, and adjusters. The risk is not only a wrong decision; it is a decision nobody can explain later. ClaimGuard AI solves this with a UiPath-governed multi-agent case workflow.

## 0:30-1:15 Architecture

Show the repository structure. Explain that UiPath Maestro Case is the orchestration layer, Agent Builder hosts specialized agents, and coded agents provide deterministic fraud and audit logic. Point to `workflows/maestro-case-flow.md`.

## 1:15-2:30 Claim Intake Demo

Open the sample JSON files. Show a complete claim, a missing-document claim, and a high-risk claim. Explain how the Claim Intake Agent checks required documents and flags data inconsistencies.

## 2:30-3:30 Policy And Fraud Agent Demo

Run:

```powershell
python scripts/run_local_demo.py --claim data/sample-claim-high-risk.json
```

Show the fraud score, indicators, human review flag, and recommended next step.

## 3:30-4:15 Human Review Demo

Explain how Maestro routes high risk or missing documents to a human adjuster. Show the mocked human decision in the local demo output and map it to UiPath Action Center or Maestro human task handling.

## 4:15-5:00 Audit Summary And Impact

Show the final audit summary JSON. Highlight the timeline, exceptions, human approval, and final recommendation. Close by explaining that the same structure can be stored as UiPath case evidence for audit and compliance.
