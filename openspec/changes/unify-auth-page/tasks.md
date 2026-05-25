## 1. 后端 — 数据模型与配置

- [x] 1.1 在 `app/models/user.py` 新增 `email` 字段（String(255), unique, nullable=True），先允许空值以便迁移
- [x] 1.2 在 `app/core/config.py` 新增 SMTP 配置项（SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_USE_TLS, RESET_TOKEN_EXPIRE_MINUTES, FRONTEND_URL）
- [x] 1.3 在 `app/repositories/user_repository.py` 新增 `get_by_email(email)` 方法

## 2. 后端 — Schema 与邮件服务

- [x] 2.1 在 `app/schemas/auth.py` 新增 `ForgotPasswordRequest`（email）、`ResetPasswordRequest`（token, new_password），RegisterRequest 新增 email 字段（必填）
- [x] 2.2 新建 `app/services/email_service.py`，实现 SMTP 发送和 mock 模式，包含重置密码邮件模板

## 3. 后端 — 认证服务与 API

- [x] 3.1 在 `app/services/auth_service.py` 新增 `forgot_password()` 方法：验证邮箱、生成 token 存 Redis、调用邮件服务发送重置链接
- [x] 3.2 在 `app/services/auth_service.py` 新增 `reset_password()` 方法：验证 token、更新密码哈希、清除 Redis token、撤销现有 session
- [x] 3.3 在 `app/services/auth_service.py` 的 `register()` 方法中新增 email 唯一性检查
- [x] 3.4 在 `app/api/endpoints/auth.py` 新增 `POST /auth/forgot-password` 和 `POST /auth/reset-password` 端点

## 4. 前端 — Liquid Glass 全局基础设施

- [x] 4.1 新建 `src/composables/useLiquidGlass.js`：单例模式，SVG displacement 动画引擎（init/distort/pulse/settle/tick），按需驱动 rAF 循环
- [x] 4.2 在 `src/App.vue` 挂载全局 SVG 滤镜（`<filter id="liquid-glass">` 含 feImage 噪声贴图 + feDisplacementMap），调用 `useLiquidGlass().init()`
- [x] 4.3 在 `src/styles.css` 全局升级 `.glass-panel`：应用 `backdrop-filter: url(#liquid-glass)`，提高透明度，添加光线折射条、边缘光晕，`@supports` 降级到 `blur()`
- [x] 4.4 升级输入框和按钮样式：透明背景、聚焦发光、悬停液态交互

## 5. 前端 — 注册与忘记密码组件

- [x] 5.1 新建 `src/components/RegisterFormCard.vue`（用户名、昵称、邮箱、密码、确认密码，含前端校验 + 液态交互）
- [x] 5.2 新建 `src/components/ForgotPasswordCard.vue`（邮箱输入、发送按钮、状态反馈 + 液态交互）
- [x] 5.3 在 `src/services/auth.js` 新增 `register()`、`forgotPassword()`、`resetPassword()` API 方法

## 6. 前端 — 统一认证页面重构

- [x] 6.1 重写 `src/views/LoginView.vue` 为三面板容器（平移 + 淡入淡出切换，切换时触发液态脉冲）
- [x] 6.2 实现面板切换动画（translateX + opacity 组合，缓动曲线 cubic-bezier(0.23, 1, 0.32, 1)）
- [x] 6.3 适配 `src/components/LoginFormCard.vue` 布局，添加底部切换链接 + 液态交互
- [x] 6.4 在注册和忘记密码组件中添加底部切换链接

## 7. 前端 — 重置密码独立页面

- [x] 7.1 新建 `src/views/ResetPasswordView.vue`（token 验证、新密码表单、提交重置 + 液态风格）
- [x] 7.2 在 `src/router/index.js` 新增 `/reset-password` 路由

## 8. 前端 — 现有页面接入液态交互

- [x] 8.1 在 `src/components/AppHeader.vue` 接入 useLiquidGlass 交互（导航栏悬停扭曲）
- [x] 8.2 在 `src/views/WorkspaceView.vue` 接入 useLiquidGlass 交互（卡片悬停、按钮悬停扭曲）

## 9. 数据库迁移与集成测试

- [x] 9.1 编写数据库迁移脚本：为现有用户填充默认 email 值，然后设置 email 为 NOT NULL
- [x] 9.2 端到端测试：注册（含 email）→ 登录 → 忘记密码 → 收收邮件 → 重置密码 → 用新密码登录
