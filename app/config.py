"""Application configuration"""

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


settings = Settings()
