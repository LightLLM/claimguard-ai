# Devpost Submission Draft

## Inspiration

Insurance claim teams need faster decisions, but they also need decisions they can defend. We built ClaimGuard AI to show how multiple AI agents can collaborate inside a governed UiPath Maestro Case workflow.

## What It Does

ClaimGuard AI processes an insurance claim from intake through policy verification, fraud signal review, human adjuster decision, and final audit summary. It flags missing documents, policy exceptions, risk indicators, and human review requirements.

## How We Built It

We modeled the workflow around UiPath Automation Cloud and Maestro Case. We created Agent Builder-ready prompt files, JSON schemas for agent contracts, sample claim and policy data, and local Python coded agents for fraud scoring and audit summary generation.

## Challenges We Ran Into

The main challenge was designing an MVP that demonstrates real case orchestration without relying on paid external APIs or private insurance systems. We solved this with realistic mock data and transparent deterministic rules.

## Accomplishments

- Built a complete multi-agent claim orchestration repo.
- Created three claim scenarios for judges to test.
- Implemented deterministic fraud scoring.
- Implemented JSON-serializable audit summaries.
- Documented Maestro case routing and human review paths.

## What We Learned

Agentic systems are strongest when they are paired with workflow governance. The agents produce recommendations, but UiPath Maestro Case controls state, routing, accountability, and auditability.

## What Is Next

- Connect the coded agents to UiPath Automation Cloud.
- Build the Maestro Case in UiPath.
- Add UiPath Action Center forms for adjuster decisions.
- Add document extraction for uploaded claim evidence.
- Add dashboard reporting for fraud trends and claim cycle time.

## Built With

- UiPath Automation Cloud
- UiPath Maestro Case design
- UiPath Agent Builder-ready prompts
- UiPath CLI / coding-agent skills
- Python standard library
- JSON schemas

## Testing Instructions For Judges

1. Clone the repository.
2. From `claimguard-ai`, run `python scripts/validate_sample_data.py`.
3. Run `python scripts/run_local_demo.py`.
4. Run `python scripts/run_local_demo.py --claim data/sample-claim-high-risk.json`.
5. Inspect the printed fraud signal and audit summary JSON.
