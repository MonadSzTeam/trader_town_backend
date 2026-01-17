"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 智谱 AI 配置
    zhipu_api_key: Optional[str] = None
    # 兼容旧配置名
    openai_api_key: Optional[str] = None
    
    # 应用配置
    app_name: str = "Trader Town Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
settings = Settings()
