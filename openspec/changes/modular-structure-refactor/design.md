## Context

当前前后端代码均为"单层平铺"结构：后端所有接口在 `endpoints/` 顶层，前端所有页面在 `views/` 顶层、所有组件在 `components/` 顶层。随着业务增长（video、blog、tools 等 App 陆续接入），这种结构会导致命名冲突、职责混乱和边界破坏。必须在规模扩大前完成目录分层，为后续多 App 并存打好基础。

## Goals / Non-Goals

**Goals:**
- 后端各分层目录按 App 名建子包，共享层与 App 层边界物理隔离
- 前端 views/components/services 按 App 名建子目录，路由分组注释
- 所有 import 路径随目录变动同步更新，项目保持可运行状态
- auth 相关表单组件归入 `components/auth/` 子目录

**Non-Goals:**
- 不新增任何业务功能
- 不修改 API 路由路径或接口契约
- 不改动数据库表结构
- 不新建 video/blog/tools 等 App 的实际业务代码（只建目录占位 `__init__.py` / `.gitkeep`）

## Decisions

### 决策 1：后端只建 auth 子包，其他 App 建空目录

当前后端只有 auth/health 共享层，没有任何具体 App 代码。因此本次只需：
1. 将现有共享代码原地保留（不移动）
2. 为未来 App（video、blog、tools）在各分层下建空子目录 + `__init__.py`

**理由**：现有代码全部属于共享层，强行归入某个 App 目录反而错误；空目录让新成员知道该往哪里放代码。

### 决策 2：前端 auth 相关组件归入 `components/auth/`

LoginFormCard、RegisterFormCard、ForgotPasswordCard 三个组件专属于认证流程，不跨 App 复用。将其归入 `components/auth/` 子目录。AppHeader、StatusCard 属于全局共享，保留顶层。

**理由**：auth 相关组件既不是全局复用组件，也不属于某个业务 App，独立子目录语义最清晰。

### 决策 3：前端共享页面保留 views/ 顶层，不建 auth/ 子目录

LoginView、ResetPasswordView、WorkspaceView 是全局共享的路由级页面，按规范放顶层。

**理由**：规范明确"全局共享的页面（登录、导航门户）放顶层"。

### 决策 4：路由文件只更新 import 路径，不改变路由结构

`router/index.js` 中按 App 分组添加注释，但路由定义本身不变。

## 文件变动清单

### 后端新建目录（空占位）

```
app/api/endpoints/video/__init__.py
app/api/endpoints/blog/__init__.py
app/api/endpoints/tools/__init__.py
app/services/video/__init__.py
app/services/blog/__init__.py
app/services/tools/__init__.py
app/models/video/__init__.py
app/models/blog/__init__.py
app/models/tools/__init__.py
app/schemas/video/__init__.py
app/schemas/blog/__init__.py
app/schemas/tools/__init__.py
app/repositories/video/__init__.py
app/repositories/blog/__init__.py
app/repositories/tools/__init__.py
```

### 前端移动文件

| 原路径 | 新路径 |
|--------|--------|
| `components/LoginFormCard.vue` | `components/auth/LoginFormCard.vue` |
| `components/RegisterFormCard.vue` | `components/auth/RegisterFormCard.vue` |
| `components/ForgotPasswordCard.vue` | `components/auth/ForgotPasswordCard.vue` |

### 前端 import 路径更新

- `views/LoginView.vue`：三个 Card 组件 import 路径更新为 `../components/auth/`
- `router/index.js`：添加分组注释

## Risks / Trade-offs

- **[风险] import 路径遗漏** → 通过 `vite build` 编译验证，构建失败即捕获
- **[风险] 后端空 `__init__.py` 影响模块发现** → Python 包导入不受影响，只是新增空包
- **[取舍] 只移动前端组件不移动页面** → 保持与规范一致，共享页面在顶层符合架构约定

## Migration Plan

1. git commit 当前状态（保留回滚点）
2. 后端：各分层目录下建 video/blog/tools 空子包
3. 前端：建 `components/auth/` 目录，移动三个 Card 组件
4. 前端：更新 `views/LoginView.vue` 中的 import 路径
5. 前端：更新 `router/index.js` 分组注释
6. 执行 `docker compose up -d --build` 验证构建通过

## Open Questions

无。
