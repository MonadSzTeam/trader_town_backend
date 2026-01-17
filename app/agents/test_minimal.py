"""测试最少参数情况下的交易员 Agent"""

import asyncio
from app.agents import (
    ValueInvestorAgent,
    TechnicalAnalystAgent,
    TradingInput,
    KLineData
)


async def test_minimal_params():
    """测试最少参数情况"""
    
    print("=" * 60)
    print("最少参数测试 - 仅提供当前价格")
    print("=" * 60)
    
    # 测试1: 仅提供价格（最少参数）
    minimal_input = TradingInput(
        current_price=100.0
    )
    
    print("\n【测试1: 仅价格】")
    print(f"输入: 价格={minimal_input.current_price}")
    
    value_agent = ValueInvestorAgent()
    tech_agent = TechnicalAnalystAgent()
    
    print("\n价值投资交易员分析:")
    value_decision = value_agent.analyze(minimal_input)
    print(f"  决策: {value_decision.action}")
    print(f"  信心度: {value_decision.confidence:.2%}")
    print(f"  理由: {value_decision.reasoning[:100]}...")
    
    print("\n技术面分析交易员分析:")
    tech_decision = tech_agent.analyze(minimal_input)
    print(f"  决策: {tech_decision.action}")
    print(f"  信心度: {tech_decision.confidence:.2%}")
    print(f"  理由: {tech_decision.reasoning[:100]}...")
    
    # 测试2: 价格 + 少量K线数据（只有收盘价）
    print("\n" + "=" * 60)
    print("【测试2: 价格 + 少量K线（仅收盘价）】")
    print("=" * 60)
    
    simple_klines = [
        KLineData(close=95.0),
        KLineData(close=97.0),
        KLineData(close=98.5),
        KLineData(close=99.0),
        KLineData(close=100.0),  # 当前价格
    ]
    
    simple_input = TradingInput(
        current_price=100.0,
        klines=simple_klines
    )
    
    print(f"输入: 价格={simple_input.current_price}, K线={len(simple_klines)}根（仅收盘价）")
    
    print("\n价值投资交易员分析:")
    value_decision2 = value_agent.analyze(simple_input)
    print(f"  决策: {value_decision2.action}")
    print(f"  信心度: {value_decision2.confidence:.2%}")
    print(f"  理由: {value_decision2.reasoning[:150]}...")
    
    print("\n技术面分析交易员分析:")
    tech_decision2 = tech_agent.analyze(simple_input)
    print(f"  决策: {tech_decision2.action}")
    print(f"  信心度: {tech_decision2.confidence:.2%}")
    print(f"  理由: {tech_decision2.reasoning[:150]}...")
    
    # 测试3: 价格 + 标的信息 + 部分基本面
    print("\n" + "=" * 60)
    print("【测试3: 价格 + 标的信息 + 部分基本面】")
    print("=" * 60)
    
    partial_input = TradingInput(
        symbol="AAPL",
        current_price=150.0,
        pe_ratio=25.0,
        # 没有K线数据，只有部分基本面
    )
    
    print(f"输入: 标的={partial_input.symbol}, 价格={partial_input.current_price}, PE={partial_input.pe_ratio}")
    
    print("\n价值投资交易员分析:")
    value_decision3 = value_agent.analyze(partial_input)
    print(f"  决策: {value_decision3.action}")
    print(f"  信心度: {value_decision3.confidence:.2%}")
    print(f"  理由: {value_decision3.reasoning[:150]}...")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_minimal_params())

