# Tools

- `cli/`：内部 CLI；每个工具一个目录，包含 README、安装和示例。
- `scripts/`：单一用途的小型自动化脚本。
- `integrations/`：第三方 API、Webhook、机器人和账号关系说明。
- `software/`：团队软件目录、用途、owner、成本、权限与续费时间。

可复用、需要版本与测试的脚本应升级为 CLI 或独立代码仓库。凭证只存密码管理器或密钥系统。
