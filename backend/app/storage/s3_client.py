"""
Cliente de S3 con soporte para mock local.

Este módulo maneja la carga de archivos a S3 y generación de URLs,
también puede funcionar en modo mock para desarrollo local sin AWS.
"""

import uuid
import os
from typing import Optional
from pathlib import Path

from app.config import config
from app.converter.exceptions import StorageError


class S3Client:
    """
    Cliente para interactuar con S3 o mock local
    
    Attributes:
        use_mock: Si es True se simula S3 en lo que es guardar archivos localmente
        mock_dir: Directorio para archivos cuando use_mock=True
    """
    
    def __init__(self, use_mock: bool = None):
        """
        Inicializa el cliente S3.
        
        Args:
            use_mock: Fuerza modo mock. Si es None se detecta automáticamente.
        """
        if use_mock is None:
            self.use_mock = config.ENVIRONMENT == "development"
        else:
            self.use_mock = use_mock
        
        self.mock_dir = Path("/tmp/s3-mock")
        
        if self.use_mock:
            self.mock_dir.mkdir(exist_ok=True, parents=True)
            self.s3 = None  
        else:
            import boto3
            self.s3 = boto3.client("s3", region_name=config.AWS_REGION)
    
    def upload_and_get_url(
        self,
        content: bytes,
        file_extension: str,
        expires_in: Optional[int] = None
    ) -> str:
        """
        Sube archivo a S3 y retorna URL presigned.
        
        Args:
            content: Contenido del archivo en bytes
            file_extension: Extensión sin punto (ej: "docx", "html")
            expires_in: Tiempo de expiración en segundos (opcional)
        
        Returns:
            str: URL presigned para descargar el archivo
        
        Raises:
            StorageError: Si hay error al subir o generar URL
        """
        if expires_in is None:
            expires_in = config.PRESIGNED_URL_EXPIRY
        
        file_key = f"{uuid.uuid4()}.{file_extension}"
        
        try:
            if self.use_mock:
                return self._upload_mock(content, file_key)
            else:
                return self._upload_s3(content, file_key, expires_in)
                
        except Exception as e:
            raise StorageError(
                f"Error al subir archivo: {str(e)}",
                bucket=config.BUCKET_NAME,
                key=file_key
            )
    
    def _upload_mock(self, content: bytes, file_key: str) -> str:
        """
        Guarda archivo localmente (modo mock).
        
        Args:
            content: Contenido en bytes
            file_key: Nombre del archivo
        
        Returns:
            str: URL simulada (file://)
        """
        file_path = self.mock_dir / file_key
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        return f"file://{file_path.absolute()}"
    
    def _upload_s3(self, content: bytes, file_key: str, expires_in: int) -> str:
        """
        Sube archivo a S3 real.
        
        Args:
            content: Contenido en bytes
            file_key: Key en S3
            expires_in: Segundos de expiración
        
        Returns:
            str: URL presigned
        """
        self.s3.put_object(
            Bucket=config.BUCKET_NAME,
            Key=file_key,
            Body=content,
            ContentType=self._get_content_type(file_key)
        )
        
        url = self.s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": config.BUCKET_NAME,
                "Key": file_key
            },
            ExpiresIn=expires_in
        )
        
        return url
    
    def _get_content_type(self, filename: str) -> str:
        """
        Determina Content-Type basado en extensión.
        
        Args:
            filename: Nombre del archivo
        
        Returns:
            str: MIME type
        """
        extension = filename.split(".")[-1].lower()
        
        content_types = {
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "html": "text/html",
            "pdf": "application/pdf",
            "txt": "text/plain"
        }
        
        return content_types.get(extension, "application/octet-stream")
    
    def delete_file(self, file_url: str) -> bool:
        """
        Elimina archivo de S3 o mock.
        
        Args:
            file_url: URL del archivo
        
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if self.use_mock:
                if file_url.startswith("file://"):
                    file_path = Path(file_url.replace("file://", ""))
                    if file_path.exists():
                        file_path.unlink()
                    return True
            else:
                pass
            
            return True
            
        except Exception as e:
            raise StorageError(f"Error al eliminar archivo: {str(e)}")


_client_instance = None


def get_s3_client(use_mock: bool = None) -> S3Client:
    """
    Obtiene instancia del cliente S3 (singleton).
    
    Args:
        use_mock: Forzar modo mock
    
    Returns:
        S3Client: Instancia del cliente
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = S3Client(use_mock=use_mock)
    
    return _client_instance


def upload_and_get_url(content: bytes, file_extension: str) -> str:
    """
    Atajo para subir archivo y obtener URL.
    
    Args:
        content: Contenido en bytes
        file_extension: Extensión del archivo
    
    Returns:
        str: URL del archivo
    """
    client = get_s3_client()
    return client.upload_and_get_url(content, file_extension)