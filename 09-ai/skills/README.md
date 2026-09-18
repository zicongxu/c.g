# Skills

## Required Location

Every Skill uses this structure:

```text
09-ai/skills/<kebab-case-skill-name>/
├── SKILL.md
├── examples/       # optional
├── evals/          # optional
└── scripts/        # optional
```

Creating or importing a Skill anywhere else is a routing error. Never place a Skill in `00-inbox/`.

## Required Workflow

1. Search `registry.yaml` for the name and aliases.
2. Create or update `skills/<skill-name>/SKILL.md`.
3. Include trigger conditions, non-triggers, input/output contract, permission boundaries, failure behavior, examples, and evaluation criteria.
4. Update `registry.yaml` in the same change.
5. Run `10-tools/scripts/validate-workspace.sh`.

Only an owner-reviewed Skill that meets its evaluation threshold may use `status: active`.
