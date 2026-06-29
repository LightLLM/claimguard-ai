# UiPath Components

## Automation Cloud

ClaimGuard AI is designed to run under UiPath Automation Cloud so that claim execution, permissions, logs, and governance are centrally managed.

## Maestro Case

Maestro Case is the primary track fit. It should own:

- Claim case creation
- Agent step orchestration
- Exception paths
- Long-running case state
- Human adjuster tasks
- Final case closure
- Audit evidence

## Agent Builder

The markdown files in `agents/` are starter definitions for Agent Builder. Each agent has a clear role, input expectation, instruction set, escalation rule, and output format.

## Coded Agents

The Python agents in `coded-agents/` are local deterministic implementations that can be wrapped as automations or called by UiPath-hosted workflows.

## UiPath CLI

The project includes CLI usage in the README to demonstrate the UiPath for Coding Agents workflow:

```powershell
npm install -g @uipath/cli
uip --version
uip login
uip skills install --agent cursor --local
```
