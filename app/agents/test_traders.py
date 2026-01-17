"""测试交易员 Agent 功能"""

import asyncio
from app.agents import (
    ValueInvestorAgent,
    TechnicalAnalystAgent,
    TradingInput,
    KLineData
)


def create_sample_klines() -> list[KLineData]:
    """创建示例K线数据（模拟上涨趋势）"""
    klines = []
    base_price = 100.0
    
    # 生成20根K线，模拟一个上涨趋势
    for i in range(20):
        open_price = base_price + i * 0.5 + (i % 3) * 0.3
        close_price = open_price + 1.0 + (i % 2) * 0.5
        high_price = close_price + 0.5
        low_price = open_price - 0.3
        volume = 1000000 + i * 50000
        
        klines.append(KLineData(
            timestamp=f"2024-01-{15+i:02d} 09:30:00",
            open=round(open_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2),
            close=round(close_price, 2),
            volume=volume
        ))
        base_price = close_price
    
    return klines


async def test_traders():
    """测试两个交易员 Agent"""
    
    # 创建示例数据
    klines = create_sample_klines()
    current_price = klines[-1].close
    
    trading_input = TradingInput(
        symbol="AAPL",
        current_price=current_price,
        klines=klines,
        # 添加一些基本面数据（用于价值投资分析）
        market_cap=3000000000000,  # 3万亿
        pe_ratio=28.5,
        pb_ratio=45.2,
        revenue=394328000000,  # 3943亿
        profit=99803000000  # 998亿
    )
    
    print("=" * 60)
    print("交易员 Agent 测试")
    print("=" * 60)
    print(f"\n标的: {trading_input.symbol}")
    print(f"当前价格: {current_price:.2f}")
    print(f"K线数据: {len(klines)}根")
    print(f"最近5根K线收盘价: {[k.close for k in klines[-5:]]}")
    print("\n" + "=" * 60)
    
    # 测试价值投资交易员
    print("\n【价值投资交易员分析】")
    print("-" * 60)
    value_agent = ValueInvestorAgent()
    value_decision = value_agent.analyze(trading_input)
    
    print(f"决策: {value_decision.action}")
    print(f"信心度: {value_decision.confidence:.2%}")
    print(f"理由: {value_decision.reasoning}")
    if value_decision.target_price:
        print(f"目标价格: {value_decision.target_price:.2f}")
    if value_decision.stop_loss:
        print(f"止损价格: {value_decision.stop_loss:.2f}")
    
    # 测试技术面分析交易员
    print("\n【技术面分析交易员分析】")
    print("-" * 60)
    tech_agent = TechnicalAnalystAgent()
    tech_decision = tech_agent.analyze(trading_input)
    
    print(f"决策: {tech_decision.action}")
    print(f"信心度: {tech_decision.confidence:.2%}")
    print(f"理由: {tech_decision.reasoning}")
    if tech_decision.target_price:
        print(f"目标价格: {tech_decision.target_price:.2f}")
    if tech_decision.stop_loss:
        print(f"止损价格: {tech_decision.stop_loss:.2f}")
    
    # 对比分析
    print("\n" + "=" * 60)
    print("【对比分析】")
    print("-" * 60)
    if value_decision.action == tech_decision.action:
        print(f"✅ 两位交易员意见一致: {value_decision.action}")
    else:
        print(f"⚠️  两位交易员意见分歧:")
        print(f"   价值投资交易员: {value_decision.action} (信心度: {value_decision.confidence:.2%})")
        print(f"   技术面分析交易员: {tech_decision.action} (信心度: {tech_decision.confidence:.2%})")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_traders())

