"""价值投资交易员 Agent"""

import json
from typing import Optional
from app.agents.base_agent import BaseAgent
from app.agents.models import TradingInput, TradingDecision


class ValueInvestorAgent(BaseAgent):
    """价值投资理念的交易员 Agent
    
    专注于：
    - 公司基本面分析
    - 财务指标评估
    - 长期价值判断
    - 估值合理性分析
    """
    
    SYSTEM_PROMPT = """你是一位资深的**价值投资**交易员，拥有20年的投资经验，深受巴菲特、格雷厄姆等价值投资大师的影响。

你的投资理念：
1. **长期持有**：关注公司的长期价值，而非短期波动
2. **基本面分析**：深入研究公司的财务状况、盈利能力、行业地位
3. **安全边际**：只在价格低于内在价值时买入，留有足够的安全边际
4. **护城河**：重视公司的竞争优势和护城河
5. **估值合理**：关注PE、PB等估值指标，寻找被低估的优质公司

你的分析重点：
- 财务健康度（营收、利润、现金流）
- 估值水平（PE、PB是否合理）
- 行业前景和公司竞争力
- 管理层质量和公司治理

决策原则：
- **买入（BUY）**：当公司基本面优秀，当前价格明显低于内在价值，且估值合理时
- **卖出（SELL）**：当公司基本面恶化，或价格严重高估，远超内在价值时
- **持有（HOLD）**：当公司基本面良好但价格接近合理估值，或需要更多信息时

请基于提供的信息，给出专业的投资决策。即使数据不完整，也要基于现有信息给出明确的建议，并在理由中说明数据限制。

注意：
- 如果基本面数据不足，可以基于价格趋势和有限信息给出建议
- 如果只有价格信息，可以基于价格位置和一般市场规律给出建议
- 信心度应该根据数据完整度调整（数据越完整，信心度可以越高）

你的回答必须是JSON格式，包含以下字段：
{
    "action": "BUY" | "SELL" | "HOLD",
    "confidence": 0.0-1.0之间的浮点数（根据数据完整度调整）,
    "reasoning": "详细的决策理由（说明使用了哪些数据，数据限制等）",
    "price": 当前价格,
    "target_price": 目标价格（可选，买入时建议提供）,
    "stop_loss": 止损价格（可选，买入时建议提供）
}
"""
    
    def __init__(self, model: str = "glm-4", api_key: Optional[str] = None):
        """初始化价值投资交易员"""
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
        prompt = "请分析以下投资机会：\n\n"
        
        # 标的信息
        if trading_input.symbol:
            prompt += f"**标的代码**: {trading_input.symbol}\n"
        if trading_input.company_name:
            prompt += f"**公司名称**: {trading_input.company_name}\n"
        if trading_input.industry:
            prompt += f"**行业**: {trading_input.industry}\n"
        
        prompt += f"**当前价格**: {trading_input.current_price}\n"
        
        # K线数据（如果有）
        if trading_input.klines and len(trading_input.klines) > 0:
            prompt += f"\n**K线数据**（最近{len(trading_input.klines)}根）:\n"
            recent_klines = trading_input.klines[-20:] if len(trading_input.klines) > 20 else trading_input.klines
            for kline in recent_klines:
                kline_info = f"- 收盘: {kline.close}"
                if kline.timestamp:
                    kline_info = f"- 时间: {kline.timestamp}, " + kline_info
                if kline.open is not None:
                    kline_info += f", 开: {kline.open}"
                if kline.high is not None:
                    kline_info += f", 高: {kline.high}"
                if kline.low is not None:
                    kline_info += f", 低: {kline.low}"
                if kline.volume is not None:
                    kline_info += f", 量: {kline.volume}"
                prompt += kline_info + "\n"
            
            # 计算价格趋势（如果有足够数据）
            if len(trading_input.klines) >= 2:
                closes = [k.close for k in trading_input.klines]
                price_change = closes[-1] - closes[0]
                price_change_pct = (price_change / closes[0] * 100) if closes[0] > 0 else 0
                prompt += f"\n价格趋势: 从 {closes[0]:.2f} 到 {closes[-1]:.2f}，变化 {price_change_pct:+.2f}%\n"
        else:
            prompt += "\n**注意**: 未提供K线数据，将仅基于当前价格和基本面进行分析。\n"
        
        # 基本面数据（如果有）
        has_fundamental = any([
            trading_input.market_cap, trading_input.pe_ratio, trading_input.pb_ratio,
            trading_input.revenue, trading_input.profit
        ])
        
        if has_fundamental:
            prompt += "\n**基本面数据**:\n"
            if trading_input.market_cap:
                prompt += f"- 市值: {trading_input.market_cap:,.0f}\n"
            if trading_input.pe_ratio:
                prompt += f"- 市盈率(PE): {trading_input.pe_ratio}\n"
            if trading_input.pb_ratio:
                prompt += f"- 市净率(PB): {trading_input.pb_ratio}\n"
            if trading_input.revenue:
                prompt += f"- 营收: {trading_input.revenue:,.0f}\n"
            if trading_input.profit:
                prompt += f"- 利润: {trading_input.profit:,.0f}\n"
        else:
            prompt += "\n**注意**: 未提供基本面数据，将基于价格趋势和一般市场规律进行分析。\n"
        
        prompt += "\n请基于价值投资理念，给出买入/卖出/持有的决策，并说明理由。如果数据不完整，请在理由中说明数据限制。"
        
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

