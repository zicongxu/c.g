# 知识治理规则

## 1. 文档生命周期

```text
capture -> draft -> reviewed -> active -> deprecated -> archived
```

- `capture`：刚进入 `00-inbox/`，尚未归类。
- `draft`：正在整理，不能作为正式依据。
- `reviewed`：已有负责人审阅，等待生效或合并。
- `active`：当前有效，可作为团队与 Agent 的依据。
- `deprecated`：不再推荐，但仍可能被旧项目引用。
- `archived`：只作历史追溯。

## 2. 文档元数据

长期保留的 Markdown 文档应使用以下 YAML 头：

```yaml
---
title: 文档标题
summary: 一句话说明这份文档解决什么问题
status: draft
owner: 姓名或角色
updated: YYYY-MM-DD
review_cycle: monthly | quarterly | yearly | event-driven
source_of_truth: true
confidentiality: public | internal | restricted
tags: [product, video-ai]
related: []
---
```

`updated` 表示内容最后核验时间，不是格式修改时间。没有 `owner` 的文档不应长期处于 `active`。

## 3. 四类知识

| 类型 | 典型内容 | 推荐位置 | 更新方式 |
|---|---|---|---|
| 事实 | 产品定义、组织、指标口径、软件清单 | 对应业务目录 | 原位更新并保留变更记录 |
| 决策 | 架构、模型、供应商、流程选择 | `05-engineering/decisions/` 或对应项目 | 新增 ADR，不删除历史 |
| 方法 | SOP、Runbook、生产流程、Prompt 用法 | `08-knowledge/playbooks/`、`09-ai/` | 经验证后升级为 active |
| 证据 | 访谈、论文、会议、实验数据 | `04-research/`、`08-knowledge/references/` | 保留出处、时间和许可 |

## 4. 写作最小标准

每份知识文档至少回答：

1. 结论是什么？
2. 适用于什么范围，不适用于什么范围？
3. 依据或原始来源在哪里？
4. 谁负责，什么时候复核？
5. 下一步行动或相关文档是什么？

## 5. AI-native 约定

- 给 Agent 的上下文包放 `09-ai/context/`，内容应短、稳定、有边界，并链接权威文档。
- Prompt 放 `09-ai/prompts/`，Skill 放 `09-ai/skills/`；两者都必须有版本、输入输出契约、示例和评测链接。
- 评测集与结果放 `09-ai/evals/`。结论必须记录模型、参数、数据集版本、日期与成本。
- Agent 生成的报告要注明生成方式和人工审阅者；不能把推断写成事实。
- 重要流程应优先固化为可执行 Skill/Workflow，其次才是长篇说明。

## 6. 命名与链接

- 文件和目录：`kebab-case`，日期用 `YYYY-MM-DD`。
- 周期材料：`YYYY-MM-DD-topic.md`。
- 决策：`adr-NNN-short-title.md`。
- 实验：`exp-YYYYMMDD-short-title.md`。
- 项目：每个项目一个目录，目录内保留 `README.md` 作为状态页。
- 使用相对链接连接仓库内文档，避免写死本机路径。

## 7. 不应放入 Git 的内容

- 密钥、Cookie、Token、`.env` 和访问凭证。
- 未脱敏的个人信息、客户数据和受限合同正文。
- 大型视频、音频、模型权重、数据集和可再生成的构建产物。
- 只有聊天上下文才能理解、没有结论和负责人信息的记录。
