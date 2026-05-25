## ADDED Requirements

### Requirement: auth 相关表单组件归入 components/auth/ 子目录

`LoginFormCard.vue`、`RegisterFormCard.vue`、`ForgotPasswordCard.vue` SHALL 位于 `src/components/auth/` 目录下，不再存在于 `src/components/` 顶层。

#### Scenario: 组件文件路径正确
- **WHEN** 重构完成后检查目录
- **THEN** `src/components/auth/LoginFormCard.vue` 存在
- **THEN** `src/components/auth/RegisterFormCard.vue` 存在
- **THEN** `src/components/auth/ForgotPasswordCard.vue` 存在
- **THEN** `src/components/LoginFormCard.vue` 不存在

### Requirement: 全局共享组件保留 components/ 顶层

`AppHeader.vue`、`StatusCard.vue` SHALL 保留在 `src/components/` 顶层，不归入任何子目录。

#### Scenario: 全局组件路径不变
- **WHEN** 重构完成后
- **THEN** `src/components/AppHeader.vue` 存在
- **THEN** `src/components/StatusCard.vue` 存在

### Requirement: views/ 顶层保留全局共享页面

`LoginView.vue`、`ResetPasswordView.vue`、`WorkspaceView.vue` SHALL 保留在 `src/views/` 顶层。

#### Scenario: 共享页面路径不变
- **WHEN** 重构完成后
- **THEN** `src/views/LoginView.vue` 存在
- **THEN** `src/views/ResetPasswordView.vue` 存在
- **THEN** `src/views/WorkspaceView.vue` 存在

### Requirement: views/ 下为各 App 建空子目录

`src/views/` 下 SHALL 存在 `video/`、`blog/`、`tools/` 子目录（含 `.gitkeep`），标志未来 App 页面的放置位置。

#### Scenario: App 页面子目录存在
- **WHEN** 重构完成后
- **THEN** `src/views/video/.gitkeep` 存在
- **THEN** `src/views/blog/.gitkeep` 存在
- **THEN** `src/views/tools/.gitkeep` 存在

### Requirement: components/ 下为各 App 建空子目录

`src/components/` 下 SHALL 存在 `video/`、`blog/`、`tools/` 子目录（含 `.gitkeep`）。

#### Scenario: App 组件子目录存在
- **WHEN** 重构完成后
- **THEN** `src/components/video/.gitkeep` 存在
- **THEN** `src/components/blog/.gitkeep` 存在
- **THEN** `src/components/tools/.gitkeep` 存在

### Requirement: LoginView.vue import 路径更新

`views/LoginView.vue` 中三个 Card 组件的 import 路径 SHALL 指向 `../components/auth/`。

#### Scenario: import 路径正确
- **WHEN** 重构完成，执行 vite build
- **THEN** 构建成功无错误
- **THEN** 登录页面三个面板（登录/注册/忘记密码）正常渲染和切换

### Requirement: router/index.js 按 App 分组注释

`router/index.js` SHALL 包含按 App 分组的注释（`// === 共享层 ===`、`// === video App ===` 等），便于后续新增 App 路由时定位。

#### Scenario: 路由注释存在
- **WHEN** 查看 router/index.js
- **THEN** 文件包含共享层分组注释
- **THEN** 文件包含各 App 分组注释占位
- **THEN** 路由功能与重构前完全一致
