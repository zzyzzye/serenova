## ADDED Requirements

### Requirement: 注册表单字段

注册面板 SHALL 包含以下必填字段：用户名、昵称、邮箱、密码、确认密码。

#### Scenario: 表单字段展示
- **WHEN** 注册面板处于活跃状态
- **THEN** 表单 SHALL 显示用户名（3-64字符）、昵称（1-64字符）、邮箱（有效邮箱格式）、密码（6-128字符）、确认密码（必须与密码一致）五个输入框

#### Scenario: 密码强度提示
- **WHEN** 用户输入密码
- **THEN** 密码长度不足 6 字符时 SHALL 显示提示信息

### Requirement: 注册表单校验

注册表单 SHALL 在提交前进行前端校验，校验不通过时显示错误信息。

#### Scenario: 必填字段为空
- **WHEN** 用户点击注册按钮但存在空字段
- **THEN** 表单 SHALL 显示"请填写所有字段"错误信息，不发送请求

#### Scenario: 邮箱格式无效
- **WHEN** 用户输入的邮箱不符合标准邮箱格式
- **THEN** 表单 SHALL 显示"请输入有效的邮箱地址"错误信息

#### Scenario: 密码不一致
- **WHEN** 确认密码与密码不匹配
- **THEN** 表单 SHALL 显示"两次输入的密码不一致"错误信息

#### Scenario: 用户名已存在
- **WHEN** 提交注册请求但后端返回 409 冲突
- **THEN** 表单 SHALL 显示"该用户名已被注册"错误信息

#### Scenario: 邮箱已被使用
- **WHEN** 提交注册请求但后端返回邮箱冲突错误
- **THEN** 表单 SHALL 显示"该邮箱已被注册"错误信息

### Requirement: 注册成功流程

注册成功后 SHALL 自动登录并跳转到工作台。

#### Scenario: 注册成功
- **WHEN** 后端返回注册成功（token pair）
- **THEN** 前端 SHALL 持久化认证状态，显示成功提示，1 秒后自动跳转到 `/workspace`
