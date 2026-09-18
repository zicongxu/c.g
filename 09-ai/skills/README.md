# Skills

每个 Skill 使用独立目录：

```text
skill-name/
├── SKILL.md
├── examples/
├── evals/
└── scripts/        # 如需要
```

Skill 必须包含明确触发条件、输入输出契约、权限边界、失败行为和评测。只有达到发布门槛且经 owner 审阅后，状态才能改为 `active`。
