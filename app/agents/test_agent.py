"""测试 Agent 功能的脚本"""

import asyncio
from app.agents import BaseAgent


async def test_agent():
    """测试 Agent 的基本问答功能"""
    # 创建 Agent 实例（使用智谱 GLM 模型）
    agent = BaseAgent(model="glm-4")
    
    # 测试问题
    question = "你好，请简单介绍一下你自己"
    
    print(f"问题: {question}")
    print("正在获取回答...")
    
    # 获取回答
    answer = await agent.ask(question)
    
    print(f"回答: {answer}")
    
    # 测试同步方法
    print("\n--- 测试同步方法 ---")
    question2 = "Python 是什么？"
    print(f"问题: {question2}")
    answer2 = agent.ask_sync(question2)
    print(f"回答: {answer2}")


if __name__ == "__main__":
    asyncio.run(test_agent())

