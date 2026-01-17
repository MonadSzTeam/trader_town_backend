"""交易 Agent 数据模型"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class KLineData(BaseModel):
    """K 线数据模型"""
    close: float = Field(..., description="收盘价（必需）")
    timestamp: Optional[str] = Field(None, description="时间戳（可选）")
    open: Optional[float] = Field(None, description="开盘价（可选）")
    high: Optional[float] = Field(None, description="最高价（可选）")
    low: Optional[float] = Field(None, description="最低价（可选）")
    volume: Optional[float] = Field(None, description="成交量（可选）")


class TradingDecision(BaseModel):
    """交易决策结果"""
    action: Literal["BUY", "SELL", "HOLD"] = Field(..., description="交易动作：买入/卖出/持有")
    confidence: float = Field(..., ge=0.0, le=1.0, description="信心度，0-1之间")
    reasoning: str = Field(..., description="决策理由")
    price: float = Field(..., description="当前价格")
    target_price: Optional[float] = Field(None, description="目标价格（如果有）")
    stop_loss: Optional[float] = Field(None, description="止损价格（如果有）")


class TradingInput(BaseModel):
    """交易分析输入数据（大部分参数可选，尽量提供更多数据以获得更准确的分析）"""
    # 必需参数：至少需要价格信息
    current_price: float = Field(..., description="当前价格（必需）")
    
    # 可选的基础信息
    symbol: Optional[str] = Field(None, description="股票代码/标的符号（可选）")
    klines: Optional[List[KLineData]] = Field(default_factory=list, description="K 线数据列表（可选，建议提供）")
    
    # 可选的基本面数据（用于价值投资）
    market_cap: Optional[float] = Field(None, description="市值（可选）")
    pe_ratio: Optional[float] = Field(None, description="市盈率（可选）")
    pb_ratio: Optional[float] = Field(None, description="市净率（可选）")
    revenue: Optional[float] = Field(None, description="营收（可选）")
    profit: Optional[float] = Field(None, description="利润（可选）")
    
    # 其他可选信息
    industry: Optional[str] = Field(None, description="行业（可选）")
    company_name: Optional[str] = Field(None, description="公司名称（可选）")

