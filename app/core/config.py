from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "Meal Suggestor Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenRouter Settings
    openrouter_api_key: str = "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"
    openrouter_model: str = "meta-llama/llama-4-scout:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_timeout: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def allowed_origins(self) -> List[str]:
        """Get allowed origins from environment or default."""
        origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
        return [origin.strip() for origin in origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
