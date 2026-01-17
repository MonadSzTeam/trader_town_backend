from typing import Any
import asyncio

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.config import settings


router = APIRouter()

# 常用币种符号到 CoinGecko ID 的映射
SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "mon": "monero",  # 假设用户指代 Monero (XMR)
    "usdt": "tether",
    "bnb": "binancecoin",
    "sol": "solana",
    "xrp": "ripple",
    "ada": "cardano",
    "doge": "dogecoin",
}


def _resolve_coin_id(symbol_or_id: str) -> str:
    """
    将输入的符号（如 btc）转换为 CoinGecko ID（如 bitcoin）。
    如果未在映射中找到，则假设输入本身就是 ID。
    """
    return SYMBOL_TO_ID.get(symbol_or_id.lower(), symbol_or_id.lower())


@router.get("/coins/{symbol}/overview")
async def get_coin_overview(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
) -> Any:
    """
    获取币种概览：包括实时价格和过去 24 小时的 OHLC 数据（用于绘制 K 线）。
    支持使用符号（如 btc, eth, mon）或 CoinGecko ID 查询。
    """
    coin_id = _resolve_coin_id(symbol)
    
    # 并发请求 CoinGecko 的 price 和 ohlc 接口
    async with httpx.AsyncClient(base_url="https://api.coingecko.com/api/v3", timeout=10.0) as client:
        try:
            # 1. 获取实时价格
            # API: /simple/price?ids={id}&vs_currencies={currency}&include_24hr_change=true
            price_params = {
                "ids": coin_id,
                "vs_currencies": vs_currency,
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            }
            if settings.COINGECKO_API_KEY:
                price_params["x_cg_demo_api_key"] = settings.COINGECKO_API_KEY

            price_req = client.get(
                "/simple/price",
                params=price_params
            )
            
            # 2. 获取 24 小时 OHLC 数据 (days=1)
            # API: /coins/{id}/ohlc?vs_currency={currency}&days=1
            ohlc_params = {"vs_currency": vs_currency, "days": 1}
            if settings.COINGECKO_API_KEY:
                ohlc_params["x_cg_demo_api_key"] = settings.COINGECKO_API_KEY

            ohlc_req = client.get(
                f"/coins/{coin_id}/ohlc",
                params=ohlc_params
            )
            
            # 等待所有请求完成
            price_resp, ohlc_resp = await asyncio.gather(price_req, ohlc_req)
            
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Failed to reach CoinGecko: {exc}") from exc

    # 处理价格响应
    if price_resp.status_code != 200:
        # 实时价格查询失败通常不应阻塞整个流程，但如果是 429 或关键错误则需处理
        # 这里简单起见，如果查不到价格，返回空对象或抛出错误
        pass
    
    price_data = price_resp.json()
    if coin_id not in price_data:
         raise HTTPException(status_code=404, detail=f"Coin '{symbol}' (mapped to '{coin_id}') not found")

    current_info = price_data[coin_id]

    # 处理 OHLC 响应
    ohlc_data = []
    if ohlc_resp.status_code == 200:
        ohlc_data = ohlc_resp.json()
    
    return {
        "symbol": symbol,
        "coin_id": coin_id,
        "currency": vs_currency,
        "current_price": current_info.get(vs_currency),
        "change_24h": current_info.get(f"{vs_currency}_24h_change"),
        "last_updated": current_info.get("last_updated_at"),
        "ohlc_24h": ohlc_data,  # [timestamp, open, high, low, close]
    }


@router.get("/coins/{symbol}/price")
async def get_coin_price(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
) -> Any:
    """
    仅获取实时价格。
    """
    coin_id = _resolve_coin_id(symbol)
    
    async with httpx.AsyncClient(base_url="https://api.coingecko.com/api/v3", timeout=10.0) as client:
        try:
            params = {
                "ids": coin_id, 
                "vs_currencies": vs_currency,
                "include_24hr_change": "true"
            }
            if settings.COINGECKO_API_KEY:
                params["x_cg_demo_api_key"] = settings.COINGECKO_API_KEY

            response = await client.get(
                "/simple/price",
                params=params
            )
        except httpx.RequestError as exc:
             raise HTTPException(status_code=502, detail=f"Failed to reach CoinGecko: {exc}") from exc
             
    if response.status_code != 200:
         raise HTTPException(status_code=response.status_code, detail="CoinGecko API error")
         
    data = response.json()
    if coin_id not in data:
        raise HTTPException(status_code=404, detail="Coin not found")
        
    return {
        "symbol": symbol,
        "coin_id": coin_id,
        "price_info": data[coin_id]
    }


@router.get("/coins/{coin_id}/ohlc")
async def get_coin_ohlc(
    coin_id: str,
    vs_currency: str = Query("usd", min_length=1),
    days: int = Query(1, ge=1),
) -> Any:
    # 尝试解析 ID，如果用户在这个接口也传了 btc，我们也兼容一下
    resolved_id = _resolve_coin_id(coin_id)
    url = f"/coins/{resolved_id}/ohlc"
    params = {"vs_currency": vs_currency, "days": days}
    if settings.COINGECKO_API_KEY:
        params["x_cg_demo_api_key"] = settings.COINGECKO_API_KEY

    async with httpx.AsyncClient(base_url="https://api.coingecko.com/api/v3", timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Failed to reach CoinGecko: {exc}") from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail={"message": "CoinGecko API error", "body": response.text},
        )

    data = response.json()

    return {
        "coin_id": coin_id,
        "vs_currency": vs_currency,
        "days": days,
        "ohlc": data,
    }

