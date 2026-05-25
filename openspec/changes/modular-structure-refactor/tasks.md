## 1. 准备（git 回滚点）

- [ ] 1.1 执行 `git add -A && git commit -m "chore: snapshot before modular-structure-refactor"` 保留回滚点

## 2. 后端：各分层目录建 App 空子包

- [ ] 2.1 在 `app/api/endpoints/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `__init__.py`
- [ ] 2.2 在 `app/services/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `__init__.py`
- [ ] 2.3 在 `app/models/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `__init__.py`
- [ ] 2.4 在 `app/schemas/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `__init__.py`
- [ ] 2.5 在 `app/repositories/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `__init__.py`

## 3. 前端：建 App 空子目录占位

- [ ] 3.1 在 `src/views/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `.gitkeep`
- [ ] 3.2 在 `src/components/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `.gitkeep`
- [ ] 3.3 在 `src/services/` 下建 `video/`、`blog/`、`tools/` 目录，各含 `.gitkeep`

## 4. 前端：移动 auth 相关表单组件

- [ ] 4.1 建 `src/components/auth/` 目录
- [ ] 4.2 将 `LoginFormCard.vue` 移动到 `src/components/auth/LoginFormCard.vue`
- [ ] 4.3 将 `RegisterFormCard.vue` 移动到 `src/components/auth/RegisterFormCard.vue`
- [ ] 4.4 将 `ForgotPasswordCard.vue` 移动到 `src/components/auth/ForgotPasswordCard.vue`
- [ ] 4.5 更新 `src/views/LoginView.vue` 中三个组件的 import 路径为 `../components/auth/`

## 5. 前端：更新路由分组注释

- [ ] 5.1 在 `src/router/index.js` 中为共享层和各 App 添加分组注释

## 6. 验证

- [ ] 6.1 执行 `docker compose up -d --build` 确认构建成功
- [ ] 6.2 访问 `localhost:8080` 确认登录页三个面板正常切换
- [ ] 6.3 访问 `GET /api/health` 确认后端正常响应
