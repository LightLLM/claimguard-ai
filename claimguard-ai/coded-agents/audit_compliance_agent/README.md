# Audit Compliance Agent

This coded agent creates the final audit-ready case summary from previous agent outputs and a human adjuster decision.

It is intentionally JSON-first so the output can be stored as UiPath case evidence, attached to a Maestro Case, or sent to downstream compliance workflows.

Run through the full demo:

```powershell
python ../../scripts/run_local_demo.py
```
