from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8000))
    
    # Database Settings
    DB_URL: PostgresDsn = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/crime_db")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", 10))
    
    # Security
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    API_KEY: Optional[str] = os.getenv("API_KEY")
    
    # External Services
    GEOCODING_API_URL: str = os.getenv("GEOCODING_API_URL", "https://nominatim.openstreetmap.org/search")
    GEOCODING_EMAIL: str = os.getenv("GEOCODING_EMAIL", "your@email.com")
    
    # Model Paths
    CLASSIFIER_MODEL_PATH: str = os.getenv("CLASSIFIER_MODEL_PATH", "../ml/models/crime_classifier.h5")
    
    @validator("DB_URL")
    def validate_db_url(cls, v):
        if not str(v).startswith("postgresql://"):
            raise ValueError("Database URL must start with postgresql://")
        return v
    
    @validator("ALLOWED_ORIGINS")
    def validate_origins(cls, v):
        return [origin.strip() for origin in v]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate settings
settings = Settings()

# Export for easy import
__all__ = ["settings"]
