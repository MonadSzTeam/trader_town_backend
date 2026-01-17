"""技术面分析交易员 Agent"""

import json
from typing import Optional
from app.agents.base_agent import BaseAgent
from app.agents.models import TradingInput, TradingDecision


class TechnicalAnalystAgent(BaseAgent):
    """技术面分析交易员 Agent
    
    专注于：
    - K 线形态分析
    - 技术指标分析
    - 趋势判断
    - 支撑位和阻力位识别
    """
    
    SYSTEM_PROMPT = """你是一位资深的**技术面分析**交易员，拥有20年的交易经验，精通K线分析、技术指标和图表形态。

你的分析理念：
1. **价格行为**：价格反映一切信息，通过价格走势判断市场情绪
2. **趋势为王**：识别并跟随主要趋势，顺势而为
3. **K线形态**：通过K线组合形态判断买卖信号（如锤子线、吞没形态、三只乌鸦等）
4. **技术指标**：结合成交量、均线、MACD、RSI等指标综合判断
5. **支撑阻力**：识别关键支撑位和阻力位，作为买卖参考点

你的分析重点：
- K线形态和组合（单根K线、双K组合、多K组合）
- 价格趋势（上升、下降、横盘）
- 成交量变化（放量、缩量）
- 关键价位（支撑位、阻力位、突破点）
- 技术指标信号（超买、超卖、背离等）

决策原则：
- **买入（BUY）**：当出现看涨K线形态、突破阻力位、技术指标显示买入信号时
- **卖出（SELL）**：当出现看跌K线形态、跌破支撑位、技术指标显示卖出信号时
- **持有（HOLD）**：当趋势不明确、处于横盘整理、需要等待更明确信号时

请基于提供的数据，给出专业的技术分析决策。即使数据不完整，也要基于现有信息给出明确的建议，并在理由中说明数据限制。

注意：
- 如果K线数据不足，可以基于价格趋势和有限信息给出建议
- 如果只有价格信息，可以基于价格位置和一般技术规律给出建议
- 信心度应该根据数据完整度调整（数据越完整，信心度可以越高）

你的回答必须是JSON格式，包含以下字段：
{
    "action": "BUY" | "SELL" | "HOLD",
    "confidence": 0.0-1.0之间的浮点数（根据数据完整度调整）,
    "reasoning": "详细的技术分析理由（说明使用了哪些数据，数据限制等）",
    "price": 当前价格,
    "target_price": 目标价格（可选，买入时建议提供）,
    "stop_loss": 止损价格（可选，买入时建议提供）
}
"""
    
    def __init__(self, model: str = "glm-4", api_key: Optional[str] = None):
        """初始化技术面分析交易员"""
        super().__init__(model=model, api_key=api_key)
    
    def analyze(self, trading_input: TradingInput) -> TradingDecision:
        """
        分析交易机会并给出决策
        
        Args:
            trading_input: 交易分析输入数据
        
        Returns:
            交易决策结果
        """
        # 构建分析提示
        prompt = self._build_analysis_prompt(trading_input)
        
        # 调用 Agent 进行分析
        response = self.ask_sync(prompt, self.SYSTEM_PROMPT)
        
        # 解析 JSON 响应
        decision = self._parse_response(response, trading_input.current_price)
        
        return decision
    
    async def analyze_async(self, trading_input: TradingInput) -> TradingDecision:
        """异步版本的分析方法"""
        return self.analyze(trading_input)
    
    def _build_analysis_prompt(self, trading_input: TradingInput) -> str:
        """构建分析提示词"""
        prompt = "请基于技术面分析以下交易机会：\n\n"
        
        # 标的信息
        if trading_input.symbol:
            prompt += f"**标的代码**: {trading_input.symbol}\n"
        prompt += f"**当前价格**: {trading_input.current_price}\n"
        
        # K线数据（如果有）
        if trading_input.klines and len(trading_input.klines) > 0:
            prompt += f"\n**K线数据**（最近{len(trading_input.klines)}根，按时间顺序）:\n"
            
            # 添加K线数据
            for i, kline in enumerate(trading_input.klines):
                kline_info = f"{i+1}. 收盘: {kline.close:.2f}"
                
                # 如果有开盘价，计算涨跌
                if kline.open is not None:
                    change = kline.close - kline.open
                    change_pct = (change / kline.open * 100) if kline.open > 0 else 0
                    change_symbol = "↑" if change >= 0 else "↓"
                    kline_info += f", 开: {kline.open:.2f} {change_symbol} {abs(change_pct):.2f}%"
                
                if kline.high is not None:
                    kline_info += f", 高: {kline.high:.2f}"
                if kline.low is not None:
                    kline_info += f", 低: {kline.low:.2f}"
                if kline.volume is not None:
                    kline_info += f", 量: {kline.volume:.0f}"
                if kline.timestamp:
                    kline_info = f"{i+1}. 时间: {kline.timestamp}, " + kline_info.split(". ", 1)[1]
                
                prompt += kline_info + "\n"
            
            # 计算技术指标（如果有足够数据）
            closes = [k.close for k in trading_input.klines]
            
            if len(closes) >= 2:
                prompt += f"\n**技术指标**:\n"
                
                # 价格趋势
                price_change = closes[-1] - closes[0]
                price_change_pct = (price_change / closes[0] * 100) if closes[0] > 0 else 0
                prompt += f"- 价格趋势: 从 {closes[0]:.2f} 到 {closes[-1]:.2f}，变化 {price_change_pct:+.2f}%\n"
                
                # 移动平均（如果有足够数据）
                if len(closes) >= 5:
                    ma5 = sum(closes[-5:]) / 5
                    prompt += f"- 5日均价: {ma5:.2f}\n"
                    if len(closes) >= 10:
                        ma10 = sum(closes[-10:]) / 10
                        prompt += f"- 10日均价: {ma10:.2f}\n"
                
                # 价格区间（如果有高低价数据）
                valid_highs = [k.high for k in trading_input.klines if k.high is not None]
                valid_lows = [k.low for k in trading_input.klines if k.low is not None]
                
                if valid_highs:
                    recent_high = max(valid_highs[-20:]) if len(valid_highs) >= 20 else max(valid_highs)
                    prompt += f"- 近期最高: {recent_high:.2f}\n"
                if valid_lows:
                    recent_low = min(valid_lows[-20:]) if len(valid_lows) >= 20 else min(valid_lows)
                    prompt += f"- 近期最低: {recent_low:.2f}\n"
                
                # 成交量分析（如果有成交量数据）
                valid_volumes = [k.volume for k in trading_input.klines if k.volume is not None]
                if valid_volumes:
                    avg_volume = sum(valid_volumes[-10:]) / len(valid_volumes[-10:]) if len(valid_volumes) >= 10 else sum(valid_volumes) / len(valid_volumes)
                    current_volume = valid_volumes[-1]
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
                    prompt += f"- 当前成交量: {current_volume:.0f} (平均: {avg_volume:.0f}, 倍数: {volume_ratio:.2f}x)\n"
        else:
            prompt += "\n**注意**: 未提供K线数据，将仅基于当前价格进行技术分析。\n"
        
        prompt += "\n请基于技术面分析（K线形态、趋势、支撑阻力、技术指标等），给出买入/卖出/持有的决策，并详细说明技术分析理由。如果数据不完整，请在理由中说明数据限制。"
        
        return prompt
    
    def _parse_response(self, response: str, current_price: float) -> TradingDecision:
        """解析 Agent 的响应"""
        try:
            # 尝试提取 JSON（可能包含在代码块中）
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            # 解析 JSON
            data = json.loads(json_str)
            
            return TradingDecision(
                action=data.get("action", "HOLD").upper(),
                confidence=float(data.get("confidence", 0.5)),
                reasoning=data.get("reasoning", "无理由"),
                price=current_price,
                target_price=data.get("target_price"),
                stop_loss=data.get("stop_loss")
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # 如果解析失败，返回默认的持有决策
            return TradingDecision(
                action="HOLD",
                confidence=0.3,
                reasoning=f"解析响应失败: {str(e)}。原始响应: {response[:200]}",
                price=current_price
            )

