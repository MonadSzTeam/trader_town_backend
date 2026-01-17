"""基础智谱 GLM Agent 实现"""

from typing import Optional
from zhipuai import ZhipuAI
from app.config import settings


class BaseAgent:
    """基础 Agent 类，提供问答功能（基于智谱 GLM 模型）"""
    
    def __init__(self, model: str = "glm-4", api_key: Optional[str] = None):
        """
        初始化 Agent
        
        Args:
            model: 使用的智谱 GLM 模型，默认为 glm-4
                可选模型: glm-4, glm-4-plus, glm-4-flash, glm-3-turbo 等
            api_key: 智谱 API 密钥，如果不提供则从配置中读取
        
        Raises:
            ValueError: 如果未提供 API key 且配置中也没有
        """
        self.model = model
        # 优先使用传入的 api_key，其次使用 zhipu_api_key，最后兼容 openai_api_key
        api_key = api_key or settings.zhipu_api_key or settings.openai_api_key
        
        if not api_key:
            raise ValueError(
                "智谱 API key 未设置。请设置环境变量 ZHIPU_API_KEY 或在初始化时提供 api_key 参数"
            )
        
        # 初始化智谱 AI 客户端
        self.client = ZhipuAI(api_key=api_key)
    
    async def ask(self, question: str, system_prompt: Optional[str] = None) -> str:
        """
        向 Agent 提问并获取回答（异步方法）
        
        Args:
            question: 用户的问题
            system_prompt: 可选的系统提示词，用于定义 Agent 的角色和行为
        
        Returns:
            Agent 的回答
        """
        # 智谱 AI 的 API 是同步的，这里直接调用同步方法
        return self.ask_sync(question, system_prompt)
    
    def ask_sync(self, question: str, system_prompt: Optional[str] = None) -> str:
        """
        同步版本的提问方法
        
        Args:
            question: 用户的问题
            system_prompt: 可选的系统提示词
        
        Returns:
            Agent 的回答
        """
        # 构建消息列表
        messages = []
        
        # 添加系统提示词（如果提供）
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加用户问题
        messages.append({
            "role": "user",
            "content": question
        })
        
        # 调用智谱 AI API（使用与 OpenAI 兼容的接口）
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        # 返回回答内容
        return response.choices[0].message.content

