## ADDED Requirements

### Requirement: 后端各分层目录按 App 建空子包

后端的 `api/endpoints/`、`services/`、`models/`、`schemas/`、`repositories/` 目录下，SHALL 各自存在以 App 名命名的子目录（video、blog、tools），每个子目录包含 `__init__.py`，标志为合法 Python 包。

#### Scenario: 新建空子包存在
- **WHEN** 重构完成后检查目录结构
- **THEN** `app/api/endpoints/video/__init__.py` 存在
- **THEN** `app/api/endpoints/blog/__init__.py` 存在
- **THEN** `app/api/endpoints/tools/__init__.py` 存在
- **THEN** 同样结构在 services/models/schemas/repositories 下各自存在

### Requirement: 共享层代码原地保留不移动

auth、health、user 相关的共享代码（`endpoints/auth.py`、`endpoints/health.py`、`services/auth_service.py`、`services/email_service.py`、`services/health_service.py`、`models/user.py`、`schemas/auth.py`、`repositories/user_repository.py`、`repositories/auth_session_repository.py`）SHALL 保留在各分层顶层，不归入任何 App 子目录。

#### Scenario: 共享文件路径不变
- **WHEN** 重构完成后
- **THEN** `app/api/endpoints/auth.py` 仍在原路径
- **THEN** `app/services/auth_service.py` 仍在原路径
- **THEN** 后端服务正常启动，所有 API 路由可访问

### Requirement: 后端服务重构后保持可运行

重构后执行 `docker compose up -d --build`，后端容器 SHALL 正常启动，`/api/health` 接口返回 200。

#### Scenario: 构建和启动成功
- **WHEN** 执行 docker compose 构建
- **THEN** 构建无错误退出
- **THEN** `GET /api/health` 返回 200
