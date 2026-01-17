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
