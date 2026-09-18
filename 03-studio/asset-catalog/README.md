# Asset Catalog

本目录保存媒体资产元数据，不保存大型二进制文件。每项资产至少记录：

| 字段 | 说明 |
|---|---|
| asset_id | 稳定、唯一的资产标识 |
| type | video / audio / image / project / character / voice |
| version | 明确版本，不使用“最终版” |
| project | 所属项目与交付物 |
| storage_uri | 对象存储或媒体系统链接 |
| checksum | 用于完整性和去重 |
| rights | 版权、肖像、声音与使用范围 |
| provenance | 拍摄、授权、生成模型和输入来源 |
| owner | 负责人 |
| retention | 保留和删除策略 |

AI 生成资产还应记录模型、模型版本、Prompt/Workflow 版本、seed（如适用）和生成日期。
