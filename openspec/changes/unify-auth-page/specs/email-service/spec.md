## ADDED Requirements

### Requirement: SMTP 邮件发送

EmailService SHALL 通过 SMTP 协议发送邮件，支持 TLS 加密。

#### Scenario: 正常发送邮件
- **WHEN** 调用 `send_email(to, subject, html_body)` 且 SMTP 配置完整
- **THEN** 服务 SHALL 通过配置的 SMTP 服务器发送邮件，返回发送成功

#### Scenario: SMTP 连接失败
- **WHEN** SMTP 服务器无法连接或认证失败
- **THEN** 服务 SHALL 记录错误日志，抛出 EmailSendError 异常

### Requirement: Mock 模式

当 SMTP 未配置时，EmailService SHALL 进入 mock 模式，将邮件内容输出到日志。

#### Scenario: SMTP_HOST 未配置
- **WHEN** 环境变量 `SMTP_HOST` 为空或未设置
- **THEN** 服务 SHALL 进入 mock 模式，调用 `send_email` 时将收件人、主题、正文（含重置链接）打印到 INFO 级别日志，不实际发送

#### Scenario: Mock 模式下重置密码流程
- **WHEN** 在 mock 模式下触发忘记密码流程
- **THEN** 日志中 SHALL 包含完整的重置链接 URL，开发人员可直接复制使用

### Requirement: 重置密码邮件模板

邮件 SHALL 使用 HTML 格式，包含品牌信息和重置链接。

#### Scenario: 邮件内容
- **WHEN** 发送重置密码邮件
- **THEN** 邮件主题为"Serenova - 密码重置"，正文包含：问候语、重置链接按钮、链接有效期说明（30分钟）、如非本人操作的提示

### Requirement: 配置化

邮件服务的所有参数 SHALL 通过环境变量配置。

#### Scenario: 完整配置
- **WHEN** 设置了 `SMTP_HOST`、`SMTP_PORT`、`SMTP_USER`、`SMTP_PASS`、`SMTP_FROM`
- **THEN** 服务 SHALL 使用这些配置连接 SMTP 服务器

#### Scenario: 部分配置
- **WHEN** 仅设置了 `SMTP_HOST` 但缺少认证信息
- **THEN** 服务 SHALL 尝试匿名连接（适用于本地测试 SMTP 服务器）
