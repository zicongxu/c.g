# Agents

Each agent lives at `agents/<agent-name>/` and defines:

- purpose and explicit non-goals;
- input and output contracts;
- allowed tools and data boundaries;
- actions requiring human approval;
- failure, escalation, and handoff behavior;
- owner, version, and evaluation links.

Register every agent in `registry.yaml`. An agent should not simultaneously generate, approve, and externally publish high-risk content.
