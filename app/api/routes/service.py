"""CoinGecko API Service 层"""

from typing import Any, Dict
import asyncio

import httpx
from fastapi import HTTPException

from app.config import settings


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


def resolve_coin_id(symbol_or_id: str) -> str:
    """
    将输入的符号（如 btc）转换为 CoinGecko ID（如 bitcoin）。
    如果未在映射中找到，则假设输入本身就是 ID。
    
    Args:
        symbol_or_id: 币种符号或 CoinGecko ID
    
    Returns:
        CoinGecko ID
    """
    return SYMBOL_TO_ID.get(symbol_or_id.lower(), symbol_or_id.lower())


class CoinGeckoService:
    """CoinGecko API 服务类"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    TIMEOUT = 10.0
    
    def __init__(self):
        """初始化服务"""
        self.api_key = settings.coingecko_api_key or settings.COINGECKO_API_KEY
    
    def _get_api_key_params(self) -> Dict[str, str]:
        """获取 API Key 参数（CoinGecko 使用查询参数而非请求头）"""
        if self.api_key:
            return {"x_cg_demo_api_key": self.api_key}
        return {}
    
    async def get_coin_price(
        self, 
        coin_id: str, 
        vs_currency: str = "usd"
    ) -> Dict[str, Any]:
        """
        获取币种实时价格
        
        Args:
            coin_id: CoinGecko 币种 ID
            vs_currency: 计价货币，默认为 usd
        
        Returns:
            价格信息字典
        
        Raises:
            HTTPException: 当 API 调用失败或币种不存在时
        """
        params = {
            "ids": coin_id,
            "vs_currencies": vs_currency,
            "include_24hr_change": "true"
        }
        params.update(self._get_api_key_params())
        
        async with httpx.AsyncClient(
            base_url=self.BASE_URL, 
            timeout=self.TIMEOUT
        ) as client:
            try:
                response = await client.get(
                    "/simple/price",
                    params=params
                )
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=502, 
                    detail=f"Failed to reach CoinGecko: {exc}"
                ) from exc
        
        if response.status_code != 200:
            error_detail = f"CoinGecko API error: {response.status_code}"
            if response.status_code == 429:
                error_detail = "CoinGecko API rate limit exceeded. Please try again later."
            elif response.status_code == 502:
                error_detail = "CoinGecko API service unavailable. Please check your network connection."
            try:
                error_body = response.json()
                if isinstance(error_body, dict) and 'error' in error_body:
                    error_detail = f"CoinGecko API error: {error_body.get('error', error_detail)}"
            except:
                pass
            raise HTTPException(
                status_code=response.status_code, 
                detail=error_detail
            )
        
        data = response.json()
        if coin_id not in data:
            raise HTTPException(
                status_code=404, 
                detail="Coin not found"
            )
        
        return data[coin_id]
    
    async def get_coin_ohlc(
        self,
        coin_id: str,
        vs_currency: str = "usd",
        days: int = 1
    ) -> list:
        """
        获取币种 OHLC 数据
        
        Args:
            coin_id: CoinGecko 币种 ID
            vs_currency: 计价货币，默认为 usd
            days: 天数，默认为 1
        
        Returns:
            OHLC 数据列表
        
        Raises:
            HTTPException: 当 API 调用失败时
        """
        url = f"/coins/{coin_id}/ohlc"
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        params.update(self._get_api_key_params())
        
        async with httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=self.TIMEOUT
        ) as client:
            try:
                response = await client.get(
                    url,
                    params=params
                )
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to reach CoinGecko: {exc}"
                ) from exc
        
        if response.status_code != 200:
            error_detail = f"CoinGecko API error: {response.status_code}"
            if response.status_code == 429:
                error_detail = "CoinGecko API rate limit exceeded. Please try again later."
            elif response.status_code == 502:
                error_detail = "CoinGecko API service unavailable. Please check your network connection."
            try:
                error_body = response.json()
                if isinstance(error_body, dict) and 'error' in error_body:
                    error_detail = f"CoinGecko API error: {error_body.get('error', error_detail)}"
            except:
                pass
            raise HTTPException(
                status_code=response.status_code,
                detail=error_detail,
            )
        
        return response.json()
    
    async def get_coin_overview(
        self,
        coin_id: str,
        vs_currency: str = "usd"
    ) -> Dict[str, Any]:
        """
        获取币种概览：包括实时价格和过去 24 小时的 OHLC 数据
        
        Args:
            coin_id: CoinGecko 币种 ID
            vs_currency: 计价货币，默认为 usd
        
        Returns:
            包含价格和 OHLC 数据的字典
        
        Raises:
            HTTPException: 当 API 调用失败或币种不存在时
        """
        # 并发请求价格和 OHLC 数据
        async with httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=self.TIMEOUT
        ) as client:
            try:
                # 1. 获取实时价格
                price_params = {
                    "ids": coin_id,
                    "vs_currencies": vs_currency,
                    "include_24hr_change": "true",
                    "include_last_updated_at": "true",
                }
                price_params.update(self._get_api_key_params())
                
                price_req = client.get(
                    "/simple/price",
                    params=price_params
                )
                
                # 2. 获取 24 小时 OHLC 数据
                ohlc_params = {
                    "vs_currency": vs_currency,
                    "days": 1
                }
                ohlc_params.update(self._get_api_key_params())
                
                ohlc_req = client.get(
                    f"/coins/{coin_id}/ohlc",
                    params=ohlc_params
                )
                
                # 等待所有请求完成
                price_resp, ohlc_resp = await asyncio.gather(price_req, ohlc_req)
                
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to reach CoinGecko: {exc}"
                ) from exc
        
        # 处理价格响应
        if price_resp.status_code != 200:
            raise HTTPException(
                status_code=price_resp.status_code,
                detail="Failed to fetch price data"
            )
        
        price_data = price_resp.json()
        if coin_id not in price_data:
            raise HTTPException(
                status_code=404,
                detail=f"Coin '{coin_id}' not found"
            )
        
        current_info = price_data[coin_id]
        
        # 处理 OHLC 响应
        ohlc_data = []
        if ohlc_resp.status_code == 200:
            ohlc_data = ohlc_resp.json()
        
        return {
            "coin_id": coin_id,
            "currency": vs_currency,
            "current_price": current_info.get(vs_currency),
            "change_24h": current_info.get(f"{vs_currency}_24h_change"),
            "last_updated": current_info.get("last_updated_at"),
            "ohlc_24h": ohlc_data,  # [timestamp, open, high, low, close]
        }

