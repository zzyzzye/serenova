## Context

当前 Serenova 项目的认证系统仅有登录功能。后端已有完整的注册 API（`POST /auth/register`），但前端无入口。忘记密码功能前后端均缺失。User 模型无 email 字段。

现有技术栈：FastAPI + Vue 3 + MySQL + Redis，前端无状态管理库（Pinia/Vuex），认证状态通过 localStorage 管理。前端已有 glassmorphism 风格的 `.glass-panel` 样式基础。

## Goals / Non-Goals

**Goals:**
- 单页三面板认证界面（登录、注册、忘记密码），平移 + 淡入淡出动画切换
- 全局 Liquid Glass 视觉风格（SVG displacement 滤镜 + 交互式液态扭曲）
- 完整的忘记密码流程（邮箱验证 → SMTP 发送重置链接 → 独立页面重置密码）
- 注册时强制要求 email 字段
- SMTP 邮件服务可配置，开发阶段支持 mock

**Non-Goals:**
- 不做邮箱验证（注册即激活）
- 不做 OAuth/第三方登录
- 不改动 refresh token 自动刷新逻辑
- 不做多因素认证
- 移动端适配为次要优先级

## Decisions

### D1: 三面板切换方案 — 平移 + 淡入淡出

**选择**: 三个面板通过 `translateX` + `opacity` 组合动画切换，不使用 3D 旋转。

**替代方案**:
- **3D 透视旋转 (rotateY)**: 视觉效果强但与 SVG backdrop-filter 叠加时容易出现渲染问题
- **纯淡入淡出**: 平静但缺少方向感
- **纯平移**: 有方向感但缺少层次

**实现要点**:
- 面板容器使用相对定位，面板通过 `transform: translateX()` + `opacity` 控制
- 活跃面板: `translateX(0) opacity(1)`
- 离场面板（向左）: `translateX(-60px) opacity(0)`
- 入场面板（从右）: `translateX(60px) opacity(0)` → `translateX(0) opacity(1)`
- 缓动曲线: `cubic-bezier(0.23, 1, 0.32, 1)`（弹性感）
- 切换时同时触发液态玻璃脉冲效果（distort 1.0 → 1.6 → 1.0）
- 面板通过 `activePanel` 状态变量控制（`login` | `register` | `forgot`）
- 底部链接文字切换面板（"没有账号？注册" / "已有账号？登录" / "忘记密码？"）

### D2: Liquid Glass — SVG displacement 全局基础设施

**选择**: 基于 SVG `feDisplacementMap` 滤镜实现液态玻璃效果，全局单例，按需驱动动画。

**参考**: `example/liquid.html` 中的 SVG 滤镜方案。

**架构**:
```
App.vue
├── <svg> 全局 #liquid-glass 滤镜（feImage 噪声贴图 + feDisplacementMap）
├── <router-view />
└── useLiquidGlass().init()  ← 启动动画引擎

composables/useLiquidGlass.js (单例)
├── state: dispEl, currentScale, targetScale, lerpSpeed, isRunning
├── init(): 获取 DOM 引用, 启动
├── distort(target): 设置目标值, 启动动画循环
├── pulse(target, duration): 脉冲效果 (先冲到 target 再平息回 1.0)
├── settle(): 平息到 1.0
└── tick(): requestAnimationFrame 循环, 到达目标后自动停止
```

**动画引擎特性**:
- 按需驱动: 有变化才跑 rAF，到达目标后停止，零持续开销
- 插值平滑: `currentScale += (targetScale - currentScale) * 0.12`
- 脉冲效果: `pulse(1.6, 600)` 先 distort 到 1.6，40% 时长后开始回落

**交互触发点**:

| 触发 | 元素 | 效果 |
|------|------|------|
| 面板切换 | auth 三面板 | `pulse(1.6, 600)` |
| 面板悬停 | `.glass-panel` | `distort(1.25)` / `settle()` |
| 输入框聚焦 | `input:focus` | `distort(1.12)` / `settle()` |
| 按钮悬停 | `button:hover` | `distort(1.2)` / `settle()` |
| 页面加载 | `.glass-panel` 入场 | `distort(0.6) → settle()` |

**降级方案**: `@supports not (backdrop-filter: url(#x))` 时回退到 `blur(34px) saturate(165%)`。

**CSS 全局样式升级**:
- 提高透明度: 背景 `rgba(255,255,255, 0.15~0.25)`
- 光线折射条: `::before` 伪元素做斜向高光 gradient
- 边缘光晕: `box-shadow` 带彩色散射
- 输入框同步升级: 更透明 + 聚焦时发光效果

### D3: 忘记密码 — 独立路由 + Redis token

**选择**: 忘记密码表单在三面板中，但重置密码页面是独立路由 `/reset-password`。

**流程**:
1. 用户在忘记密码面板输入邮箱
2. 后端生成 reset token（UUID），存入 Redis（TTL 30 分钟），key: `{prefix}:auth:reset:{token}`
3. 后端通过 SMTP 发送包含 `https://yourapp.com/reset-password?token=xxx` 的邮件
4. 用户点击链接，前端 `/reset-password` 页面加载，验证 token 有效性
5. 用户输入新密码，提交后后端验证 token、更新密码、清除 Redis key

**替代方案**:
- **重置密码也融入三面板**: 通过 URL 参数 `?mode=reset&token=xxx` 自动切换面板 — 增加前端复杂度，且重置密码的上下文与登录/注册不同

### D4: 邮件服务 — SMTP 直连 + mock 模式

**选择**: 使用 Python 标准库 `smtplib` + `email.mime`，不引入第三方邮件库。

**配置项**（环境变量）:
- `SMTP_HOST` — SMTP 服务器地址
- `SMTP_PORT` — 端口（默认 587）
- `SMTP_USER` — 用户名
- `SMTP_PASS` — 密码
- `SMTP_FROM` — 发件人地址
- `SMTP_USE_TLS` — 是否启用 TLS（默认 true）
- `RESET_TOKEN_EXPIRE_MINUTES` — 重置 token 有效期（默认 30）

**mock 模式**: 当 `SMTP_HOST` 未配置时，邮件内容打印到日志（包含重置链接），不实际发送。

### D5: 数据库变更 — email 字段加索引

**选择**: 在 User 模型新增 `email` 字段，`VARCHAR(255)`，`UNIQUE`，`NOT NULL`，加索引。

**索引策略**: email 字段需要唯一索引（用于注册时查重 + 忘记密码时查询），直接通过 SQLAlchemy 的 `unique=True` 创建。

**迁移方案**: 新增列，由于现有数据无 email 值，需要：
1. 先添加可空 email 列
2. 为现有用户填充默认值（如 `username@placeholder.local`）
3. 设置为 NOT NULL

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| SMTP 配置错误导致邮件发不出 | mock 模式兜底，日志输出重置链接 |
| SVG displacement + backdrop-filter 在低端设备上性能问题 | `useLiquidGlass` 按需驱动（到达目标后停止 rAF），降级为普通 blur() |
| SVG `backdrop-filter: url(#)` 在 Firefox 支持有限 | `@supports` 降级检测，回退到 `blur(34px) saturate(165%)` |
| email 字段迁移影响现有用户 | 迁移脚本先加可空列 → 填充默认值 → 再设 NOT NULL |
| 忘记密码 token 被暴力猜解 | UUID v4 碰撞概率极低 + Redis TTL 30 分钟 + 使用后立即清除 |
| Liquid Glass 过度使用 backdrop-filter 影响性能 | 仅在面板和输入框上使用，不用在背景装饰元素 |

## 文件清单

### 新建文件
| 文件 | 说明 |
|------|------|
| `backend/app/services/email_service.py` | SMTP 邮件发送服务 |
| `frontend/src/composables/useLiquidGlass.js` | 全局液态玻璃 composable（SVG 滤镜动画引擎） |
| `frontend/src/components/RegisterFormCard.vue` | 注册表单组件 |
| `frontend/src/components/ForgotPasswordCard.vue` | 忘记密码表单组件 |
| `frontend/src/views/ResetPasswordView.vue` | 独立重置密码页面 |

### 修改文件
| 文件 | 变更 |
|------|------|
| `backend/app/models/user.py` | 新增 email 字段 |
| `backend/app/schemas/auth.py` | 新增 schema，RegisterRequest 加 email |
| `backend/app/services/auth_service.py` | 新增 forgot_password、reset_password 方法 |
| `backend/app/api/endpoints/auth.py` | 新增 2 个端点 |
| `backend/app/repositories/user_repository.py` | 新增 get_by_email 方法 |
| `backend/app/core/config.py` | 新增 SMTP 配置项 |
| `frontend/src/App.vue` | 挂载全局 SVG 滤镜 + 初始化 useLiquidGlass |
| `frontend/src/views/LoginView.vue` | 重写为三面板容器（平移+淡入淡出切换） |
| `frontend/src/components/LoginFormCard.vue` | 适配新布局 + 液态交互 |
| `frontend/src/components/AppHeader.vue` | 接入液态玻璃交互 |
| `frontend/src/views/WorkspaceView.vue` | 接入液态玻璃交互 |
| `frontend/src/services/auth.js` | 新增 API 方法 |
| `frontend/src/router/index.js` | 新增 /reset-password 路由 |
| `frontend/src/styles.css` | 全局 Liquid Glass 样式升级 |

## Open Questions

- 重置密码邮件的前端 URL 基地址从哪获取？（建议从环境变量 `FRONTEND_URL` 配置）
- 是否需要限制忘记密码的请求频率？（建议后续加 rate limiting，本次不做）
