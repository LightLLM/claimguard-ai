# Fraud Signal Agent

This coded agent evaluates deterministic fraud indicators for a claim. It uses only Python standard library code and is designed to be wrapped by UiPath Automation Cloud as a coded automation, job, or Agent Builder tool.

## Inputs

- Claim intake summary
- Policy verification result
- Claimant history
- Vendor history

## Output

- Fraud risk score
- Risk level
- Risk indicators
- Human review requirement
- Recommended next step
- Audit notes

Run locally:

```powershell
python main.py --claim ../../data/sample-claim-high-risk.json --policy ../../data/sample-policy-exception.json
```
