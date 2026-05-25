## ADDED Requirements

### Requirement: 忘记密码表单

忘记密码面板 SHALL 包含邮箱输入框和发送按钮。

#### Scenario: 表单展示
- **WHEN** 忘记密码面板处于活跃状态
- **THEN** 表单 SHALL 显示邮箱输入框和"发送重置链接"按钮，并附说明文字"请输入注册时使用的邮箱"

#### Scenario: 邮箱格式校验
- **WHEN** 用户输入的邮箱格式无效
- **THEN** 表单 SHALL 显示"请输入有效的邮箱地址"错误信息

### Requirement: 发送重置邮件

后端 SHALL 验证邮箱存在性，生成重置 token，通过 SMTP 发送重置链接。

#### Scenario: 邮箱存在 — 发送成功
- **WHEN** 用户提交已注册的邮箱地址
- **THEN** 后端 SHALL 生成 UUID reset token，存入 Redis（TTL 30分钟），通过 SMTP 发送包含重置链接的邮件，前端显示"重置链接已发送到您的邮箱"

#### Scenario: 邮箱不存在 — 静默成功
- **WHEN** 用户提交未注册的邮箱地址
- **THEN** 后端 SHALL 返回相同成功响应（不暴露邮箱是否存在），不发送邮件

#### Scenario: 重复发送
- **WHEN** 用户在 1 分钟内多次提交同一邮箱
- **THEN** 后端 SHALL 返回成功但不重复发送邮件（使用 Redis 标记冷却期）

### Requirement: 重置密码页面

独立路由 `/reset-password` SHALL 提供密码重置表单。

#### Scenario: 有效 token 访问
- **WHEN** 用户通过邮件链接访问 `/reset-password?token=xxx` 且 token 有效
- **THEN** 页面 SHALL 显示新密码输入框、确认密码输入框和"重置密码"按钮

#### Scenario: 无效/过期 token
- **WHEN** 用户访问 `/reset-password?token=xxx` 但 token 无效或已过期
- **THEN** 页面 SHALL 显示"链接已过期或无效，请重新申请"提示，并提供返回登录的链接

#### Scenario: 缺少 token 参数
- **WHEN** 用户直接访问 `/reset-password` 不带 token 参数
- **THEN** 页面 SHALL 重定向到登录页面

### Requirement: 执行密码重置

后端 SHALL 验证 token 并更新密码。

#### Scenario: 密码重置成功
- **WHEN** 用户提交新密码且 token 有效
- **THEN** 后端 SHALL 更新密码哈希、清除 Redis 中的 reset token、撤销该用户所有现有 session，前端显示"密码重置成功，请重新登录"并跳转到登录页

#### Scenario: 密码不一致
- **WHEN** 确认密码与新密码不匹配
- **THEN** 前端 SHALL 显示"两次输入的密码不一致"错误信息

#### Scenario: token 已被使用
- **WHEN** 用户使用已被消耗的 token 尝试重置
- **THEN** 后端 SHALL 返回 400 错误，前端显示"链接已失效"
