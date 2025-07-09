import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    app_name: str = "Syrup Chat API"
    debug: bool = True
    
    # База данных
    database_url: str = "sqlite:///./database/database.db"
    
    # JWT настройки
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    
    # Cookie настройки
    jwt_access_cookie_name: str = "access_token"
    jwt_refresh_cookie_name: str = "refresh_token"
    
    # CORS настройки
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Сервер настройки
    host: str = "127.0.0.1"
    port: int = 8000
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_prefix": "",
        "extra": "ignore"
    }


# Создаем экземпляр настроек
settings = Settings() 
