"""
Configuración centralizada de la aplicación.

Todas las variables de entorno y configuraciones
se definen aquí para facilitar mantenimiento y testing.
"""

import os
from typing import Optional


class Config:
    """
    Clase de configuración con valores por defecto.
    """
    
    # AWS S3 Configuration
    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "md-converter-bucket")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # Presigned URL Configuration
    PRESIGNED_URL_EXPIRY: int = int(os.getenv("URL_EXPIRY", "300"))  # 5 minutos
    
    # Conversion Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Supported formats
    SUPPORTED_OUTPUT_FORMATS: list = ["docx", "html"]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    IS_PRODUCTION: bool = ENVIRONMENT == "PROD"
    IS_DEVELOPMENT: bool = ENVIRONMENT == "DEVELOPMENT"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """
        Valida que la configuración sea correcta.
        
        Raises:
            ValueError: Si falta alguna configuración crítica
        """
        if cls.IS_PRODUCTION and cls.BUCKET_NAME == "md-converter-bucket":
            raise ValueError(
                "BUCKET_NAME debe ser configurado en producción"
            )
        
        if cls.PRESIGNED_URL_EXPIRY < 60 or cls.PRESIGNED_URL_EXPIRY > 3600:
            raise ValueError(
                "URL_EXPIRY debe estar entre 60 y 3600 segundos"
            )
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """
        Retorna configuración como diccionario.
        
        Útil para logging o debugging.
        """
        return {
            "bucket_name": cls.BUCKET_NAME,
            "region": cls.AWS_REGION,
            "url_expiry": cls.PRESIGNED_URL_EXPIRY,
            "max_file_size_mb": cls.MAX_FILE_SIZE_MB,
            "environment": cls.ENVIRONMENT,
            "log_level": cls.LOG_LEVEL
        }


config = Config()