# AI System

- `agents/`：Agent 的角色、权限、工具和交接协议。
- `skills/`：可复用能力包；每个 Skill 一个目录。
- `prompts/`：版本化 Prompt 与输入输出示例。
- `workflows/`：多步骤、人机协作与自动化流程。
- `evals/`：测试集、评分规则、基线和结果。
- `context/`：供 Agent 加载的短小、稳定上下文包。
- `policies/`：安全、权限、模型使用和人工复核规则。

Prompt 或 Skill 未通过评测前不得标为生产可用。每次生产调用应能追溯模型版本、Prompt/Skill 版本、输入数据和输出。
