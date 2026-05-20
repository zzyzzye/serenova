# video

一个按工程化分层组织的 FastAPI + Vue3 基础项目骨架。

当前后端已包含一套基础登录设计：`JWT + Redis`，提供登录、刷新令牌、退出登录和当前用户查询接口。

## 目录

```text
backend/
  app/
    api/
    core/
    db/
    repositories/
    schemas/
    services/
  main.py
frontend/
  src/
    components/
    router/
    services/
    views/
docker-compose.yml
```

## 后端启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

## 认证接口

```text
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

默认演示账号：

```text
username: admin
password: admin123456
```
