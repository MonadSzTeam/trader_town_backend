"""API 路由定义"""

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.api.routes.service import CoinGeckoService, resolve_coin_id


router = APIRouter()


@router.get("/coins/{symbol}/overview")
async def get_coin_overview(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
) -> Any:
    """
    获取币种概览：包括实时价格和过去 24 小时的 OHLC 数据（用于绘制 K 线）。
    支持使用符号（如 btc, eth, mon）或 CoinGecko ID 查询。
    """
    coin_id = resolve_coin_id(symbol)
    service = CoinGeckoService()
    
    try:
        result = await service.get_coin_overview(coin_id, vs_currency)
        # 添加原始 symbol 到响应中
        result["symbol"] = symbol
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e


@router.get("/coins/{symbol}/price")
async def get_coin_price(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
) -> Any:
    """
    仅获取实时价格。
    """
    coin_id = resolve_coin_id(symbol)
    service = CoinGeckoService()
    
    try:
        price_info = await service.get_coin_price(coin_id, vs_currency)
        return {
            "symbol": symbol,
            "coin_id": coin_id,
            "price_info": price_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e


@router.get("/coins/{coin_id}/ohlc")
async def get_coin_ohlc(
    coin_id: str,
    vs_currency: str = Query("usd", min_length=1),
    days: int = Query(1, ge=1),
) -> Any:
    """
    获取币种 OHLC 数据。
    支持使用符号（如 btc）或 CoinGecko ID 查询。
    """
    resolved_id = resolve_coin_id(coin_id)
    service = CoinGeckoService()
    
    try:
        ohlc_data = await service.get_coin_ohlc(resolved_id, vs_currency, days)
        return {
            "coin_id": coin_id,
            "vs_currency": vs_currency,
            "days": days,
            "ohlc": ohlc_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e
