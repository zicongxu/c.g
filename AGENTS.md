# AGENTS.md

本文件约束在葱果传媒协作空间内工作的 AI Agent。

## 工作顺序

1. 先读根目录 `README.md` 和 `KNOWLEDGE.md`。
2. 再读目标目录的 `README.md`、项目状态页和关联决策。
3. 先搜索再新建，优先更新权威来源，避免制造重复文档。
4. 修改前确认负责人、状态、保密级别和原始来源。
5. 修改后更新 `updated`，并修复相关索引和链接。

## 行为边界

- 不把未经验证的生成内容标为 `active` 或 `source_of_truth: true`。
- 不读取、复制或提交密钥、个人隐私、客户原始数据。
- 不改写历史 ADR；需要变更时新增 ADR 并标注 `supersedes`。
- 不在仓库中加入大型二进制素材；只维护资产清单与受控链接。
- 不把会议逐字稿直接当作结论；提炼出的结论必须链接原记录。
- 不因“整理”而删除历史内容；移动到 `99-archive/` 并说明原因。

## 推荐产物

- 新项目：使用 `90-templates/project.md`。
- 新决策：使用 `90-templates/decision.md`。
- 新实验：使用 `90-templates/experiment.md`。
- 新会议记录：使用 `90-templates/meeting.md`。
- 新工具或软件条目：使用 `90-templates/tool.md`。
- 新 Skill：使用 `90-templates/skill.md`。

除非任务明确要求，Agent 不应做对外发布、付款、授权变更或删除不可恢复数据。
