## Why

当前前后端代码均平铺在单层目录下，所有页面、组件、接口、服务混在一起，没有按 App 划分子模块。项目计划容纳多个业务系统（video、blog、tools 等），现有结构无法扩展，必须在规模扩大前完成模块化重构，建立可持续的分层边界。

## What Changes

- **后端**：在 `api/endpoints/`、`services/`、`models/`、`schemas/`、`repositories/` 下为每个 App 创建以 App 名命名的子目录；共享层（auth、health、user 模型）保留在顶层，不做行为变动
- **前端**：在 `views/` 和 `components/` 下按 App 名建子目录；全局共享页面（LoginView、ResetPasswordView、WorkspaceView）移入规范位置；全局共享组件（AppHeader、StatusCard）保留顶层；auth 相关表单组件归入 `components/auth/`；路由在 `router/index.js` 中按 App 分组注释
- **非破坏性**：本次重构只移动文件和调整 import 路径，不改变任何 API 接口、业务逻辑、数据库结构或 UI 行为

### 非目标（Non-Goals）

- 不新增任何业务功能
- 不修改 API 路由路径
- 不改动数据库模型字段
- 不引入新的 App（video、blog 等目录此次只建空架子）
- 不改变 Docker 构建流程

## Capabilities

### New Capabilities

- `modular-backend-layout`：后端按 App 划分目录层次，共享层与 App 层边界清晰
- `modular-frontend-layout`：前端 views/components/services 按 App 划分子目录，路由分组

### Modified Capabilities

（无 spec 级行为变更，所有 API 契约和 UI 行为保持不变）

## Impact

- **后端**：`app/api/endpoints/`、`app/services/`、`app/models/`、`app/schemas/`、`app/repositories/` 目录结构变更；所有文件内的相对 import 路径需同步更新
- **前端**：`src/views/`、`src/components/`、`src/services/` 目录结构变更；`router/index.js` import 路径更新
- **回滚计划**：重构前通过 git 提交当前状态，若出现问题直接 `git revert` 回滚，无数据库迁移风险
