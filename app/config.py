"""Application configuration"""

<<<<<<< HEAD
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CoinGecko
    COINGECKO_API_KEY: str = "CG-gkYdQjp4Tg3vaUgqkFh1mk2s"
    
    # App
    APP_NAME: str = "Trader Town Backend"
    
    # Database
    DATABASE_URL: str = "sqlite:///./trader_town.db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


=======
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
>>>>>>> c99160f76ba5e32c73b4f75a44bea0ac281e9a90
settings = Settings()
