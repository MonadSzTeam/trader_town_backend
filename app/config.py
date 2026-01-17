"""Application configuration"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    
    # 智谱 AI 配置
    zhipu_api_key: Optional[str] = None
    # 兼容旧配置名
    openai_api_key: Optional[str] = None
    
    # CoinGecko API 配置
    coingecko_api_key: Optional[str] = None
    # 兼容旧配置名（大写）
    COINGECKO_API_KEY: Optional[str] = None
    
    # 应用配置
    app_name: str = "Trader Town Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # 数据库配置
    database_url: str = "sqlite:///./trader_town.db"
    # 兼容旧配置名（大写）
    DATABASE_URL: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 兼容性处理：将大写配置名映射到小写
        if self.COINGECKO_API_KEY and not self.coingecko_api_key:
            self.coingecko_api_key = self.COINGECKO_API_KEY
        if self.DATABASE_URL and not self.database_url:
            self.database_url = self.DATABASE_URL


# 全局配置实例
settings = Settings()
