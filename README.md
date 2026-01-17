# Trader Town Backend

交易员小镇后端服务，基于 FastAPI 构建，提供加密货币数据查询、模拟交易及用户资产管理功能。本项目集成 OpenAI Agent 框架，并使用 SQLAlchemy 进行数据库管理。

## 📚 目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [数据库设计](#数据库设计)
- [API 接口说明](#api-接口说明)
- [项目结构](#项目结构)
- [前后端对接指南](#前后端对接指南)

## 🚀 项目简介

这是一个纯后端 Web API 服务，旨在为前端应用提供数据支持。
主要功能包括：
1.  **市场数据**: 实时获取加密货币价格及 K 线数据 (集成 CoinGecko API)。
2.  **用户系统**: 注册、登录及账户余额管理。
3.  **交易系统**: 买入、卖出挂单及撮合逻辑。
4.  **资产管理**: 用户持仓组合 (Portfolio) 追踪。

## 🛠 技术栈

- **语言**: Python 3.10+
- **Web 框架**: FastAPI (异步高性能)
- **数据库**: SQLite (默认) / MySQL (兼容) + SQLAlchemy (ORM)
- **依赖管理**: uv (相比 pip 更快)
- **外部接口**: CoinGecko API (行情数据)

## ⚡ 快速开始

### 1. 安装依赖

本项目使用 `uv` 进行包管理。如果你还没有安装 `uv`，请先安装它，或者使用标准的 `pip`。

```bash
# 方式 A: 使用 uv (推荐)
uv sync

# 方式 B: 使用 pip
pip install -r requirements.txt  # 如果没有 requirements.txt，使用 pip install fastapi uvicorn sqlalchemy pydantic-settings httpx
```

### 2. 运行服务

```bash
# 使用 uv 启动 (推荐)
uv run uvicorn app.main:app --reload

# 或者直接使用 uvicorn
uvicorn app.main:app --reload
```

服务启动后，默认地址为: `http://localhost:8000`

### 3. 查看文档

启动服务后，访问以下地址查看自动生成的交互式文档：
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## ⚙️ 环境配置

在项目根目录创建 `.env` 文件（或修改 `app/config.py` 默认值）：

```ini
# 数据库连接字符串 (默认使用本地 SQLite)
DATABASE_URL=sqlite:///./trader_town.db

# CoinGecko API Key (可选，免费版可留空或使用 Demo Key)
COINGECKO_API_KEY=CG-gkYdQjp4Tg3vaUgqkFh1mk2s
```

## 🗄 数据库设计

本项目包含以下核心数据表 (详见 `app/db/models.py`):

| 表名 | 描述 | 关键字段 |
| :--- | :--- | :--- |
| **users** | 用户表 | `id`, `username`, `email`, `balance` (余额) |
| **items** | 资产/商品表 | `id`, `symbol` (如 BTC), `name`, `current_price` |
| **orders** | 订单表 | `id`, `user_id`, `type` (BUY/SELL), `price`, `quantity`, `status` |
| **portfolio** | 持仓表 | `id`, `user_id`, `item_id`, `quantity` |

> **注意**: 首次运行时，如果使用 SQLite，数据库文件 `trader_town.db` 会自动生成（需确保有初始化脚本运行或通过 CRUD 触发建表）。

## 🔌 API 接口说明

### 基础路径
所有 API 均以 `/api` 开头。

### 核心端点示例

#### 1. 获取币种行情
- **方法**: `GET`
- **路径**: `/api/coins/{symbol}/overview`
- **参数**: 
    - `symbol`: 币种代码 (如 `btc`, `eth`, `sol`)
    - `vs_currency`: 计价货币 (默认 `usd`)
- **响应**:
  ```json
  {
    "symbol": "btc",
    "coin_id": "bitcoin",
    "current_price": 65000.0,
    "ohlc": [[1678900000, 64000, 65000, 63000, 64500], ...]
  }
  ```

*更多接口（如用户注册、下单）正在开发中，请关注 `app/api/routes/` 目录。*

## 📂 项目结构

```text
trader_town_backend/
├── app/
│   ├── api/
│   │   ├── routes/        # 📍 业务逻辑与路由实现
│   │   │   └── __init__.py # 目前包含行情查询接口
│   │   └── __init__.py    # 路由汇总
│   ├── db/
│   │   ├── connection.py  # 数据库连接配置
│   │   ├── crud.py        # 📍 数据库增删改查操作封装
│   │   ├── doc.sql        # SQL 建表参考
│   │   └── models.py      # ORM 模型定义
│   ├── config.py          # 全局配置
│   └── main.py            # 程序入口
├── pyproject.toml         # 依赖配置文件
└── README.md              # 项目文档
```

## 🤝 前后端对接指南

致前端开发团队：

1.  **接口联调**: 请优先参考 [Swagger UI](http://localhost:8000/docs) 获取最新的参数定义。
2.  **数据格式**: 所有接口默认返回 JSON 格式。
3.  **错误处理**: 
    - `200 OK`: 请求成功。
    - `400 Bad Request`: 参数错误。
    - `404 Not Found`: 资源不存在 (如查询了不存在的币种)。
    - `500 Internal Server Error`: 服务器内部错误。
4.  **Mock 数据**: 如果后端服务不可用，可参考 `app/db/doc.sql` 中的结构 mock 本地数据。
