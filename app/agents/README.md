# Agent 模块使用说明

## 概述

`agents` 模块提供了基于**智谱 GLM 模型**的基础 Agent 功能，可以实现基本的提问回答功能。

## 快速开始

### 1. 配置环境变量

确保 `.env` 文件中包含智谱 API Key：

```env
ZHIPU_API_KEY=your_api_key_here
```

或者使用兼容的旧配置名：

```env
OPENAI_API_KEY=your_api_key_here
```

### 2. 基本使用

#### 异步方式

```python
from app.agents import BaseAgent
import asyncio

async def main():
    agent = BaseAgent(model="glm-4")
    answer = await agent.ask("你好，请介绍一下你自己")
    print(answer)

asyncio.run(main())
```

#### 同步方式

```python
from app.agents import BaseAgent

agent = BaseAgent(model="glm-4")
answer = agent.ask_sync("Python 是什么？")
print(answer)
```

### 3. 使用自定义系统提示词

```python
agent = BaseAgent(model="glm-4")
system_prompt = "你是一个专业的交易助手，擅长分析市场趋势。"
answer = await agent.ask("今天股市怎么样？", system_prompt=system_prompt)
```

## API 说明

### BaseAgent

#### 初始化参数

- `model` (str): 使用的智谱 GLM 模型，默认为 `"glm-4"`
- `api_key` (Optional[str]): 智谱 API 密钥，如果不提供则从配置中读取

#### 方法

##### `ask(question: str, system_prompt: Optional[str] = None) -> str`

异步方法，向 Agent 提问并获取回答（内部调用同步方法）。

- `question`: 用户的问题
- `system_prompt`: 可选的系统提示词，用于定义 Agent 的角色和行为
- 返回: Agent 的回答

##### `ask_sync(question: str, system_prompt: Optional[str] = None) -> str`

同步方法，功能与 `ask` 相同，但使用同步调用。

## 支持的模型

- `glm-4` (默认) - 智谱 GLM-4 模型
- `glm-4-plus` - GLM-4 Plus 增强版
- `glm-4-flash` - GLM-4 Flash 快速版
- `glm-3-turbo` - GLM-3 Turbo 模型
- 其他智谱 AI 支持的模型

## 测试

运行测试脚本：

```bash
uv run python app/agents/test_agent.py
```

