# ClaimGuard AI

ClaimGuard AI is a UiPath AgentHack MVP for orchestrating insurance claims with multiple AI agents, human adjuster review, exception handling, and audit-ready case records.

The project is built for **Track 1: UiPath Maestro Case**. UiPath Automation Cloud is the orchestration and governance layer, while the local coded agents demonstrate deterministic agent logic that can be connected into UiPath Agent Builder and Maestro Case.

## Business Problem

Insurance carriers process claims across fragmented systems, emails, invoices, policy records, and adjuster notes. Manual handoffs make it hard to detect missing documents, policy exceptions, fraud signals, and approval history in one auditable place.

ClaimGuard AI coordinates specialized agents so a claim can move from intake to verification, risk review, human decision, and final audit summary with a clear case trail.

## What It Demonstrates

- Multiple specialized agents
- Long-running case workflow
- Failure and exception handling
- Human-in-the-loop review
- Auditability and case timeline
- UiPath Automation Cloud governance model
- UiPath Agent Builder-ready agent definitions
- UiPath Maestro Case-ready workflow documentation
- UiPath CLI / UiPath for Coding Agents usage for hackathon bonus points

## Agent Architecture

1. **Claim Intake Agent** extracts and validates submitted claim data.
2. **Policy Verification Agent** checks active coverage and policy exceptions.
3. **Fraud Signal Agent** scores deterministic risk indicators.
4. **Settlement Recommendation Agent** proposes a next action.
5. **Audit Compliance Agent** generates the final case audit summary.

UiPath Maestro Case owns routing, state, exception queues, human tasks, and governance.

## Local Demo Instructions

From this directory:

```powershell
python scripts/validate_sample_data.py
python scripts/run_local_demo.py
```

Run a specific scenario:

```powershell
python scripts/run_local_demo.py --claim data/sample-claim-high-risk.json
python scripts/run_local_demo.py --claim data/sample-claim-missing-documents.json
```

The demo loads sample claim JSON, runs Fraud Signal Agent logic, runs Audit Compliance Agent logic, and prints a structured final JSON result.

## UiPath CLI Commands

```powershell
npm install -g @uipath/cli
uip --version
uip login
uip skills install --agent cursor --local
```

Native coded-agent publish flow:

```powershell
uv tool install uipath
uip tools install @uipath/codedagent-tool
uip codedagent setup
uip codedagent init
uip codedagent run main --file data/uipath-input-high-risk.json
uip codedagent deploy --my-workspace
```

Quick terminal checklist:

```powershell
node -v
npm -v
npm install -g @uipath/cli
uip --version
uip login
uip skills install --agent cursor --local
```

## How To Connect This To UiPath Automation Cloud

1. Create a UiPath Automation Cloud project for ClaimGuard AI.
2. Register the markdown files in `agents/` as Agent Builder instructions.
3. Wrap the coded agents in `coded-agents/` as callable automations, jobs, or coded workflows.
4. Use the schemas in `schemas/` as input/output contracts for each agent step.
5. Model the case in Maestro using `workflows/maestro-case-flow.md`.
6. Create human tasks for missing documents, policy exceptions, high fraud risk, and final adjuster approval.
7. Store every agent output and human decision as case evidence for audit.

The local coded agents are designed to be connected into UiPath Automation Cloud and orchestrated by UiPath Maestro Case. UiPath remains the orchestration and governance layer.

## Exception Handling

ClaimGuard AI routes these conditions to human review:

- Missing required documents
- Policy inactive, expired, or coverage mismatch
- High fraud risk
- Medium fraud risk with claim amount above 10,000
- Data inconsistencies between claim, policy, invoices, or vendor history

## Human-In-The-Loop Points

Human adjusters can:

- Approve the claim
- Reject the claim
- Request more documents
- Escalate to SIU or compliance
- Override an agent recommendation with a reason

## Demo Video Walkthrough

Recommended recording flow:

1. Show the repo structure and UiPath CLI commands.
2. Run `python scripts/run_local_demo.py`.
3. Switch scenarios to the missing-documents and high-risk samples.
4. Walk through the Maestro case flow in `workflows/maestro-case-flow.md`.
5. Show the final audit summary JSON as the evidence trail.

## Built With

- Python standard library
- JSON Schema-compatible contracts
- UiPath Automation Cloud design
- UiPath Agent Builder-ready prompts
- UiPath Maestro Case workflow model
- UiPath CLI / UiPath coding-agent skills

## License

MIT License. See `LICENSE`.
