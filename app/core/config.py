from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 🔑 Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_CONFIDENCE_THRESHOLD: float = 0.7
    
    # 🔐 Security
    SECRET_KEY: str = "tu_clave_secreta_muy_segura_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 📁 File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.gif,.webp"
    
    # 🌐 CORS
    CORS_ORIGINS: str = "*"  # Permisivo para aplicaciones móviles
    
    # 📊 APIs externas (opcional)
    NUTRITIONIX_APP_ID: Optional[str] = None
    NUTRITIONIX_API_KEY: Optional[str] = None
    
    # 🛠️ Development
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    
    @property
    def cors_origins_list(self) -> list:
        """Convierte CORS_ORIGINS string a lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_set(self) -> set:
        """Convierte ALLOWED_EXTENSIONS string a set"""
        return {ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")}
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()