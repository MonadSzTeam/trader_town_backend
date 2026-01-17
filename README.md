# trader_town_backend
交易员小镇后端

## 项目简介

基于 Python 的 **纯后端 Web API 服务**，通过 RESTful API 接口为前端应用提供数据和服务。集成 OpenAI Agent 框架，具备完整的数据库操作能力。

**注意**：本项目仅包含后端代码，不包含任何前端内容。

## 技术栈

- **Python**: >= 3.10
- **依赖管理**: uv
- **Web 框架**: FastAPI
- **数据库**: SQLAlchemy
- **AI 框架**: 智谱 GLM (ZhipuAI)

## 项目结构

```
trader_town_backend/
├── pyproject.toml          # uv 项目配置文件
├── README.md               # 项目说明文档
├── .gitignore              # Git 忽略文件
├── app/                    # 主应用目录
│   ├── __init__.py
│   ├── main.py            # FastAPI 应用入口
│   ├── config.py          # 配置管理
│   ├── api/               # API 路由模块
│   │   ├── __init__.py
│   │   └── routes/        # 路由定义
│   │       └── __init__.py
│   ├── agents/            # 智谱 GLM Agent 功能模块
│   │   └── __init__.py
│   └── db/                # 数据库模块
│       ├── __init__.py
│       ├── connection.py  # 数据库连接管理
│       └── models.py      # 数据库模型定义
└── tests/                 # 测试目录
    └── __init__.py
```

## 快速开始

### 安装依赖

```bash
# 使用 uv 安装依赖
uv sync
```

### 运行项目

```bash
# 启动开发服务器（使用 uv 运行）
uv run uvicorn app.main:app --reload

# 或者直接使用 uvicorn
uvicorn app.main:app --reload
```

服务器默认运行在 `http://localhost:8000`

### API 文档

启动服务后，可以访问：
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 开发说明

### 核心模块

- `app/main.py`: FastAPI 应用主入口，定义 API 服务启动逻辑
- `app/config.py`: 环境变量和配置管理（数据库连接、API 密钥等）
- `app/api/routes/`: API 路由定义，提供 RESTful 接口给前端调用
- `app/agents/`: 智谱 GLM Agent 功能封装，实现 AI 代理能力
- `app/db/`: 数据库连接和模型定义，使用 SQLAlchemy ORM

### 项目特点

- ✅ 纯后端服务，仅提供 API 接口
- ✅ 使用 FastAPI 构建高性能异步 API
- ✅ 集成智谱 GLM Agent 框架
- ✅ 完整的数据库操作支持（SQLAlchemy）
- ✅ 使用 uv 进行依赖管理
