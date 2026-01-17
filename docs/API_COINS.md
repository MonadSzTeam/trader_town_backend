# 币种数据 API 接口文档

## 基础信息

- **Base URL**: `http://localhost:8000/api`
- **请求方式**: `GET`
- **响应格式**: `JSON`

---

## 1. 获取币种实时价格

### 接口地址
```
GET /api/coins/{symbol}/price
```

### 参数说明

**路径参数**
- `symbol` (必填): 币种符号或 CoinGecko ID，如 `btc`, `eth`, `bitcoin`

**查询参数**
- `vs_currency` (可选): 计价货币，默认 `usd`，支持 `eur`, `cny`, `jpy` 等

### 响应示例
```json
{
  "symbol": "btc",
  "coin_id": "bitcoin",
  "price_info": {
    "usd": 65000.5,
    "usd_24h_change": 2.5
  }
}
```

### 调用示例
```
GET /api/coins/btc/price
GET /api/coins/eth/price?vs_currency=eur
GET /api/coins/sol/price?vs_currency=cny
GET /api/coins/bitcoin/price
```

---

## 2. 获取币种 OHLC 数据

### 接口地址
```
GET /api/coins/{coin_id}/ohlc
```

### 参数说明

**路径参数**
- `coin_id` (必填): 币种符号或 CoinGecko ID，如 `btc`, `eth`, `bitcoin`

**查询参数**
- `vs_currency` (可选): 计价货币，默认 `usd`
- `days` (可选): 天数，默认 `1`，必须 ≥ 1，支持 `1`, `7`, `30`, `90` 等

### 响应示例
```json
{
  "coin_id": "btc",
  "vs_currency": "usd",
  "days": 1,
  "ohlc": [
    [1678900000, 64000, 65000, 63000, 64500],
    [1678903600, 64500, 65500, 64000, 65000]
  ]
}
```

**OHLC 数组格式**: `[timestamp, open, high, low, close]`
- `timestamp`: Unix 时间戳（秒）
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价

### 调用示例
```
GET /api/coins/btc/ohlc
GET /api/coins/eth/ohlc?days=7
GET /api/coins/sol/ohlc?days=30&vs_currency=usd
GET /api/coins/btc/ohlc?days=90&vs_currency=cny
```

---

## 3. 获取价值投资者交易决策

### 接口地址
```
GET /api/coins/{symbol}/decision/value-investor
```

### 参数说明

**路径参数**
- `symbol` (必填): 币种符号或 CoinGecko ID，如 `btc`, `eth`, `bitcoin`

**查询参数**
- `vs_currency` (可选): 计价货币，默认 `usd`，支持 `eur`, `cny`, `jpy` 等
- `days` (可选): 获取多少天的 OHLC 数据用于分析，默认 `7`，必须 ≥ 1

### 功能说明

该接口会：
1. 从 CoinGecko 获取币种的实时价格和指定天数的 OHLC 数据
2. 调用价值投资 Agent 进行分析
3. 返回基于价值投资理念的交易决策

**价值投资理念**：
- 关注长期价值和基本面分析
- 寻找价格低于内在价值的投资机会
- 重视安全边际和估值合理性

### 响应示例
```json
{
  "action": "BUY",
  "confidence": 0.75,
  "reasoning": "基于价值投资分析，当前价格低于内在价值，建议买入。当前价格 50000 USD，目标价格 55000 USD，止损价格 48000 USD。",
  "price": 50000.0,
  "target_price": 55000.0,
  "stop_loss": 48000.0
}
```

**响应字段说明**：
- `action`: 交易动作，可选值：`BUY`（买入）、`SELL`（卖出）、`HOLD`（持有）
- `confidence`: 信心度，范围 0.0-1.0，数值越高表示信心越强
- `reasoning`: 详细的决策理由和分析说明
- `price`: 当前价格
- `target_price`: 目标价格（可选，买入时通常提供）
- `stop_loss`: 止损价格（可选，买入时通常提供）

### 调用示例
```
GET /api/coins/btc/decision/value-investor
GET /api/coins/eth/decision/value-investor?days=14
GET /api/coins/sol/decision/value-investor?vs_currency=usd&days=30
GET /api/coins/bitcoin/decision/value-investor?days=7
```

---

## 4. 获取技术面分析交易员决策

### 接口地址
```
GET /api/coins/{symbol}/decision/technical-analyst
```

### 参数说明

**路径参数**
- `symbol` (必填): 币种符号或 CoinGecko ID，如 `btc`, `eth`, `bitcoin`

**查询参数**
- `vs_currency` (可选): 计价货币，默认 `usd`，支持 `eur`, `cny`, `jpy` 等
- `days` (可选): 获取多少天的 OHLC 数据用于分析，默认 `7`，必须 ≥ 1

### 功能说明

该接口会：
1. 从 CoinGecko 获取币种的实时价格和指定天数的 OHLC 数据
2. 调用技术面分析 Agent 进行分析
3. 返回基于技术分析的交易决策

**技术面分析理念**：
- 关注价格走势和 K 线形态
- 识别趋势、支撑位和阻力位
- 结合技术指标（如均线、成交量等）进行判断

### 响应示例
```json
{
  "action": "HOLD",
  "confidence": 0.65,
  "reasoning": "技术面分析显示价格处于上升趋势，但接近阻力位，建议持有观望。当前价格 3000 USD，目标价格 3200 USD，止损价格 2800 USD。",
  "price": 3000.0,
  "target_price": 3200.0,
  "stop_loss": 2800.0
}
```

**响应字段说明**：
- `action`: 交易动作，可选值：`BUY`（买入）、`SELL`（卖出）、`HOLD`（持有）
- `confidence`: 信心度，范围 0.0-1.0，数值越高表示信心越强
- `reasoning`: 详细的技术分析理由和说明
- `price`: 当前价格
- `target_price`: 目标价格（可选，买入时通常提供）
- `stop_loss`: 止损价格（可选，买入时通常提供）

### 调用示例
```
GET /api/coins/eth/decision/technical-analyst
GET /api/coins/btc/decision/technical-analyst?days=14
GET /api/coins/sol/decision/technical-analyst?vs_currency=usd&days=30
GET /api/coins/ethereum/decision/technical-analyst?days=7
```

---

## 支持的币种符号

| 符号 | CoinGecko ID |
|------|--------------|
| btc | bitcoin |
| eth | ethereum |
| sol | solana |
| xrp | ripple |
| ada | cardano |
| doge | dogecoin |
| bnb | binancecoin |
| usdt | tether |
| mon | monero |

---

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 404 | 币种不存在 |
| 422 | 参数验证失败（如 days < 1） |
| 429 | API 请求频率过高 |
| 502 | 外部服务错误 |
| 500 | 服务器内部错误 |
