import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PantryPilot API"
    app_version: str = "1.0.0"
    demo_mode: bool = True
    
    # Google Cloud & Vertex AI
    google_cloud_project: str = "pantrypilot-hackathon-2026"
    google_cloud_location: str = "us-central1"
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_pro_model: str = "gemini-2.5-pro"
    vertex_ai_api_key: str = ""
    
    # Server & Security
    backend_host: str = "0.0.0.0"
    backend_port: int = 8008
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    rate_limit_per_minute: int = 60
    secret_key: str = "dev-secret-key-pantrypilot-2026"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
# Check environment override
if os.getenv("DEMO_MODE", "").lower() in ("true", "1", "yes"):
    settings.demo_mode = True
