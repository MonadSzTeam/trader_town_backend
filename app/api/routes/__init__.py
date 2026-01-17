"""API 路由定义"""

from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.api.routes.service import CoinGeckoService, resolve_coin_id
from app.agents import ValueInvestorAgent, TechnicalAnalystAgent, TradingInput, KLineData, TradingDecision


router = APIRouter()


def convert_ohlc_to_klines(ohlc_data: list, vs_currency: str = "usd") -> List[KLineData]:
    """
    将 CoinGecko OHLC 数据转换为 KLineData 列表
    
    Args:
        ohlc_data: CoinGecko OHLC 数据，格式为 [[timestamp, open, high, low, close], ...]
        vs_currency: 计价货币
    
    Returns:
        KLineData 列表
    """
    klines = []
    for item in ohlc_data:
        if len(item) >= 5:
            timestamp_ms = item[0]  # Unix 时间戳（毫秒）
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
            klines.append(KLineData(
                timestamp=timestamp,
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
            ))
    return klines


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


@router.get("/coins/{symbol}/decision/value-investor")
async def get_value_investor_decision(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
    days: int = Query(7, ge=1),
) -> TradingDecision:
    """
    获取价值投资者的交易决策。
    
    支持使用符号（如 btc, eth）或 CoinGecko ID 查询。
    该接口会获取币种的价格和 OHLC 数据，然后调用价值投资 Agent 进行分析。
    
    Args:
        symbol: 币种符号或 CoinGecko ID
        vs_currency: 计价货币，默认为 usd
        days: 获取多少天的 OHLC 数据，默认为 7 天
    
    Returns:
        价值投资者的交易决策（TradingDecision）
    """
    coin_id = resolve_coin_id(symbol)
    service = CoinGeckoService()
    
    try:
        # 获取币种价格和 OHLC 数据
        price_info = await service.get_coin_price(coin_id, vs_currency)
        ohlc_data = await service.get_coin_ohlc(coin_id, vs_currency, days)
        
        # 转换为 KLineData
        klines = convert_ohlc_to_klines(ohlc_data, vs_currency)
        
        # 获取当前价格
        current_price = price_info.get(vs_currency, 0.0)
        if not current_price and klines:
            # 如果没有价格，使用最新 K 线的收盘价
            current_price = klines[-1].close
        
        # 构建 TradingInput
        trading_input = TradingInput(
            symbol=symbol,
            current_price=current_price,
            klines=klines,
        )
        
        # 调用价值投资 Agent
        agent = ValueInvestorAgent()
        decision = await agent.analyze_async(trading_input)
        
        return decision
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e


@router.get("/coins/{symbol}/decision/technical-analyst")
async def get_technical_analyst_decision(
    symbol: str,
    vs_currency: str = Query("usd", min_length=1),
    days: int = Query(7, ge=1),
) -> TradingDecision:
    """
    获取技术面分析交易员（高频投资者）的交易决策。
    
    支持使用符号（如 btc, eth）或 CoinGecko ID 查询。
    该接口会获取币种的价格和 OHLC 数据，然后调用技术面分析 Agent 进行分析。
    
    Args:
        symbol: 币种符号或 CoinGecko ID
        vs_currency: 计价货币，默认为 usd
        days: 获取多少天的 OHLC 数据，默认为 7 天
    
    Returns:
        技术面分析交易员的交易决策（TradingDecision）
    """
    coin_id = resolve_coin_id(symbol)
    service = CoinGeckoService()
    
    try:
        # 获取币种价格和 OHLC 数据
        price_info = await service.get_coin_price(coin_id, vs_currency)
        ohlc_data = await service.get_coin_ohlc(coin_id, vs_currency, days)
        
        # 转换为 KLineData
        klines = convert_ohlc_to_klines(ohlc_data, vs_currency)
        
        # 获取当前价格
        current_price = price_info.get(vs_currency, 0.0)
        if not current_price and klines:
            # 如果没有价格，使用最新 K 线的收盘价
            current_price = klines[-1].close
        
        # 构建 TradingInput
        trading_input = TradingInput(
            symbol=symbol,
            current_price=current_price,
            klines=klines,
        )
        
        # 调用技术面分析 Agent
        agent = TechnicalAnalystAgent()
        decision = await agent.analyze_async(trading_input)
        
        return decision
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e
