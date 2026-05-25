## Why

当前认证页面只有登录功能，注册接口虽已存在于后端但前端无入口，忘记密码功能前后端均缺失。用户需要在一个页面内通过流畅的动画切换完成登录、注册和忘记密码操作，同时视觉风格需要升级为 iOS 26 Liquid Glass 设计语言，提升整体体验。

## What Changes

- **前端认证页面重构**：将单一登录卡片改为三面板容器（登录、注册、忘记密码），使用 3D 透视旋转动画进行面板切换
- **注册功能**：前端新增注册表单（用户名、昵称、邮箱、密码、确认密码），对接已有后端注册接口
- **忘记密码流程**：后端新增邮箱验证 + SMTP 发送重置链接，前端新增忘记密码表单和独立重置密码页面
- **User 模型扩展**：新增 `email` 字段（唯一、必填）
- **视觉风格升级**：全局样式从现有 glassmorphism 升级为 iOS 26 Liquid Glass 风格（更高透明度、光线折射、动态边缘光晕）
- **SMTP 邮件服务**：新增可配置的邮件发送能力，开发阶段支持 mock 模式

### 非目标（Non-Goals）

- 不实现邮箱验证（注册后直接激活，不做邮箱确认）
- 不实现 OAuth/第三方登录
- 不实现 refresh token 自动刷新逻辑（已有机制但本次不改动）
- 不实现多因素认证（MFA）
- 移动端响应式适配为次要目标，优先保证桌面端体验

## Capabilities

### New Capabilities

- `auth-frontend-unified`：统一认证页面的三面板布局、3D 透视切换动画、Liquid Glass 视觉风格
- `auth-register`：注册表单及对接后端注册接口的完整流程
- `auth-forgot-password`：忘记密码流程（前端表单 + 后端 token 生成 + SMTP 邮件发送 + 独立重置页面）
- `email-service`：SMTP 邮件发送服务，支持配置化和 mock 模式

### Modified Capabilities

（无已有 spec 需要修改）

## Impact

| 模块 | 影响文件 | 变更类型 |
|------|---------|---------|
| **后端 - 数据模型** | `app/models/user.py` | 新增 email 字段，需数据库迁移 |
| **后端 - Schema** | `app/schemas/auth.py` | 新增请求/响应 schema |
| **后端 - 服务层** | `app/services/auth_service.py` | 新增 forgot_password / reset_password 方法 |
| **后端 - 服务层** | `app/services/email_service.py` | **新建** — SMTP 邮件服务 |
| **后端 - API** | `app/api/endpoints/auth.py` | 新增 2 个端点 |
| **后端 - 仓储层** | `app/repositories/user_repository.py` | 新增 get_by_email 方法 |
| **后端 - 配置** | `app/core/config.py` | 新增 SMTP 配置项 |
| **前端 - 视图** | `src/views/LoginView.vue` | 重写为三面板容器 |
| **前端 - 组件** | `src/components/` | 新增 RegisterFormCard、ForgotPasswordCard，重构 LoginFormCard |
| **前端 - 视图** | `src/views/ResetPasswordView.vue` | **新建** — 独立重置密码页 |
| **前端 - 路由** | `src/router/index.js` | 新增 /reset-password 路由 |
| **前端 - 服务** | `src/services/auth.js` | 新增 register、forgotPassword、resetPassword 方法 |
| **前端 - 样式** | `src/styles.css` | Liquid Glass 样式升级 |
| **依赖** | `backend/pyproject.toml` | 可能新增邮件库依赖 |

### 回滚计划

1. **数据库**：`email` 字段为新增列，回滚时 DROP COLUMN 即可，不影响现有数据
2. **后端 API**：新增端点（`/auth/forgot-password`、`/auth/reset-password`），移除后不影响现有登录/注册
3. **前端**：LoginView.vue 为主要变更文件，git revert 即可恢复原登录页
4. **配置**：SMTP 配置为环境变量，移除后邮件功能降级为 mock 模式
