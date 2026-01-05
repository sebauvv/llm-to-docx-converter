"""
Tests para el módulo de storage (S3 y mock).

Valida tanto el comportamiento mock como la integración real con S3.
"""

import pytest
from pathlib import Path
from app.storage.s3_client import S3Client, get_s3_client, upload_and_get_url
from app.converter.exceptions import StorageError
from moto import mock_s3
import boto3


class TestS3ClientMock:
    """Tests para el modo mock (desarrollo local)."""
    
    def test_client_initialization_mock(self):
        """Test inicialización en modo mock."""
        client = S3Client(use_mock=True)
        
        assert client.use_mock is True
        assert client.s3 is None  # No debe inicializar boto3
        assert client.mock_dir.exists()
    
    def test_upload_mock_creates_file(self):
        """Test que upload en mock crea archivo local."""
        client = S3Client(use_mock=True)
        
        content = b"Test content"
        url = client.upload_and_get_url(content, "txt")
        
        assert url.startswith("file://")
        
        file_path = Path(url.replace("file://", ""))
        assert file_path.exists()
        
        with open(file_path, "rb") as f:
            assert f.read() == content
    
    def test_upload_mock_generates_unique_names(self):
        """Test que genera nombres únicos."""
        client = S3Client(use_mock=True)
        
        url1 = client.upload_and_get_url(b"content1", "txt")
        url2 = client.upload_and_get_url(b"content2", "txt")
        
        assert url1 != url2
    
    def test_upload_different_extensions(self):
        """Test upload con diferentes extensiones."""
        client = S3Client(use_mock=True)
        
        extensions = ["docx", "html", "pdf", "txt"]
        
        for ext in extensions:
            url = client.upload_and_get_url(b"content", ext)
            assert url.endswith(f".{ext}")
    
    def test_upload_large_file_mock(self):
        """Test upload de archivo grande."""
        client = S3Client(use_mock=True)
        
        large_content = b"x" * (1024 * 1024)
        url = client.upload_and_get_url(large_content, "bin")
        
        file_path = Path(url.replace("file://", ""))
        assert file_path.exists()
        
        assert file_path.stat().st_size == len(large_content)
    
    def test_delete_file_mock(self):
        """Test eliminación de archivo en mock."""
        client = S3Client(use_mock=True)
        
        url = client.upload_and_get_url(b"content", "txt")
        file_path = Path(url.replace("file://", ""))
        assert file_path.exists()
        
        result = client.delete_file(url)
        assert result is True
        assert not file_path.exists()


class TestS3ClientReal:
    """Tests para integración con S3 real (usando moto)."""
    
    @mock_s3
    def test_client_initialization_real(self):
        """Test inicialización con S3 real."""
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        
        client = S3Client(use_mock=False)
        
        assert client.use_mock is False
        assert client.s3 is not None
    
    @mock_s3
    def test_upload_to_s3(self, mock_s3_bucket):
        """Test upload a S3 real."""
        client = S3Client(use_mock=False)
        
        content = b"Test S3 content"
        url = client.upload_and_get_url(content, "txt")
        
        assert "https://" in url or "http://" in url
        assert "test-bucket" in url
    
    @mock_s3
    def test_upload_generates_presigned_url(self, mock_s3_bucket):
        """Test que genera URL presigned correcta."""
        client = S3Client(use_mock=False)
        
        url = client.upload_and_get_url(b"content", "docx")
        
        assert "?" in url  # Query parameters
        assert "Signature" in url or "X-Amz-" in url
    
    @mock_s3
    def test_content_type_docx(self, mock_s3_bucket):
        """Test Content-Type correcto para DOCX."""
        client = S3Client(use_mock=False)
        
        content_type = client._get_content_type("test.docx")
        
        expected = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert content_type == expected
    
    @mock_s3
    def test_content_type_html(self, mock_s3_bucket):
        """Test Content-Type correcto para HTML."""
        client = S3Client(use_mock=False)
        
        content_type = client._get_content_type("test.html")
        assert content_type == "text/html"
    
    @mock_s3
    def test_content_type_unknown(self, mock_s3_bucket):
        """Test Content-Type para extensión desconocida."""
        client = S3Client(use_mock=False)
        
        content_type = client._get_content_type("test.xyz")
        assert content_type == "application/octet-stream"


class TestSingletonPattern:
    """Tests para el patrón singleton."""
    
    def test_get_s3_client_returns_same_instance(self):
        """Test que get_s3_client retorna misma instancia."""
        import app.storage.s3_client as s3_module
        s3_module._client_instance = None
        
        client1 = get_s3_client(use_mock=True)
        client2 = get_s3_client(use_mock=True)
        
        assert client1 is client2
    
    def test_convenience_function(self):
        """Test función de conveniencia upload_and_get_url."""
        import app.storage.s3_client as s3_module
        s3_module._client_instance = None
        
        url = upload_and_get_url(b"content", "txt")
        
        assert isinstance(url, str)
        assert len(url) > 0


class TestErrorHandling:
    """Tests para manejo de errores."""
    
    def test_upload_empty_content(self):
        """Test upload con contenido vacío."""
        client = S3Client(use_mock=True)
        
        url = client.upload_and_get_url(b"", "txt")
        assert isinstance(url, str)
    
    def test_upload_invalid_extension(self):
        """Test upload con extensión vacía."""
        client = S3Client(use_mock=True)
        
        url = client.upload_and_get_url(b"content", "")
        assert isinstance(url, str)
    
    def test_storage_error_has_context(self):
        """Test que StorageError incluye contexto."""
        error = StorageError(
            "Test error",
            bucket="test-bucket",
            key="test-key"
        )
        
        assert error.bucket == "test-bucket"
        assert error.key == "test-key"
        assert "Test error" in str(error)


class TestCustomExpiry:
    """Tests para configuración de expiración."""
    
    def test_custom_expiry_time(self):
        """Test con tiempo de expiración personalizado."""
        client = S3Client(use_mock=True)
        
        url = client.upload_and_get_url(b"content", "txt", expires_in=600)
        assert isinstance(url, str)
    
    @mock_s3
    def test_expiry_in_presigned_url(self, mock_s3_bucket):
        """Test que expiry se incluye en URL presigned."""
        client = S3Client(use_mock=False)
        
        url = client.upload_and_get_url(b"content", "txt", expires_in=1800)
        
        assert "?" in url


class TestIntegration:
    """Tests de integración completos."""
    
    def test_full_workflow_mock(self):
        """Test workflow completo en modo mock."""
        client = S3Client(use_mock=True)
        
        content = b"Full workflow test content"
        
        url = client.upload_and_get_url(content, "txt")
        
        assert url.startswith("file://")
        file_path = Path(url.replace("file://", ""))
        assert file_path.exists()
        
        with open(file_path, "rb") as f:
            assert f.read() == content
    
    @mock_s3
    def test_full_workflow_s3(self, mock_s3_bucket):
        """Test workflow completo con S3."""
        client = S3Client(use_mock=False)
        
        content = b"S3 workflow test"
        url = client.upload_and_get_url(content, "docx")
        
        assert isinstance(url, str)
        assert len(url) > 0
        
        objects = mock_s3_bucket.list_objects_v2(Bucket="test-bucket")
        assert objects["KeyCount"] > 0


class TestMockDirectory:
    """Tests para el directorio mock."""
    
    def test_mock_directory_created(self):
        """Test que el directorio mock se crea."""
        client = S3Client(use_mock=True)
        
        assert client.mock_dir.exists()
        assert client.mock_dir.is_dir()
    
    def test_multiple_files_in_mock_dir(self):
        """Test múltiples archivos en directorio mock."""
        client = S3Client(use_mock=True)
        
        urls = []
        for i in range(5):
            url = client.upload_and_get_url(f"content{i}".encode(), "txt")
            urls.append(url)
        
        for url in urls:
            file_path = Path(url.replace("file://", ""))
            assert file_path.exists()