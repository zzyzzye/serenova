"""文件职责：作为本地开发启动入口转发 FastAPI 应用，不负责业务装配。"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
