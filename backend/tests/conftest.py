"""
Configuración global de pytest y fixtures compartidas.

Este archivo contiene fixtures que pueden ser usadas en todos los tests.
"""

import pytest
import os
from pathlib import Path
from moto import mock_s3
import boto3
from typing import Generator

os.environ["ENVIRONMENT"] = "development"
os.environ["BUCKET_NAME"] = "test-bucket"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["URL_EXPIRY"] = "300"


@pytest.fixture
def sample_markdown() -> str:
    """
    Retorna markdown de ejemplo para tests.
    
    Returns:
        str: Contenido markdown válido
    """
    return """# Título Principal

Este es un párrafo con **texto en negrita** y *cursiva*.


- Item 1
- Item 2
- Item 3


```python
def hello():
    print("Hello World")
```


| Columna 1 | Columna 2 |
|-----------|-----------|
| A         | B         |
| C         | D         |
"""


@pytest.fixture
def sample_html() -> str:
    """
    Retorna HTML de ejemplo para tests.
    
    Returns:
        str: Contenido HTML válido
    """
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
</head>
<body>
    <h1>Título Principal</h1>
    <p>Este es un párrafo con <strong>texto en negrita</strong> y <em>cursiva</em>.</p>
    <h2>Subtítulo</h2>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
</body>
</html>
"""


@pytest.fixture
def mock_s3_bucket():
    """
    Crea un bucket S3 mockeado para tests.
    
    Yields:
        boto3.client: Cliente S3 mockeado
    """
    with mock_s3():
        s3 = boto3.client("s3", region_name="us-east-1")
        
        s3.create_bucket(Bucket="test-bucket")
        
        yield s3


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """
    Crea directorio temporal para tests.
    
    Args:
        tmp_path: Fixture de pytest que provee path temporal
    
    Returns:
        Path: Directorio temporal
    """
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    return test_dir


@pytest.fixture
def mock_lambda_event() -> dict:
    """
    Retorna evento Lambda mock para tests del handler.
    
    Returns:
        dict: Evento simulado de API Gateway
    """
    return {
        "httpMethod": "POST",
        "path": "/convert",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": '{"markdown": "# Test", "output_format": "docx"}',
        "requestContext": {
            "requestId": "test-request-id",
            "identity": {
                "sourceIp": "127.0.0.1"
            }
        }
    }


@pytest.fixture
def mock_lambda_context():
    """
    Retorna contexto Lambda mock.
    
    Returns:
        object: Contexto simulado
    """
    class MockContext:
        function_name = "test-function"
        memory_limit_in_mb = 128
        invoked_function_arn = "arn:aws:lambda:us-east-1:123456789:function:test"
        aws_request_id = "test-request-id"
        
        def get_remaining_time_in_millis(self):
            return 30000
    
    return MockContext()


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """
    Limpia archivos temporales después de cada test.
    
    Esta fixture se ejecuta automáticamente después de cada test.
    """
    yield  # El test se ejecuta aquí
    
    temp_dir = Path("/tmp/s3-mock")
    if temp_dir.exists():
        for file in temp_dir.glob("*"):
            try:
                file.unlink()
            except Exception:
                pass


@pytest.fixture
def invalid_markdown_samples() -> list:
    """
    Retorna casos de markdown inválidos para tests negativos.
    
    Returns:
        list: Lista de strings inválidos
    """
    return [
        "",  # Vacío
        None,  # None
        123,  # No es string
        [],  # Lista
        {},  # Dict
    ]


@pytest.fixture
def complex_markdown() -> str:
    """
    Retorna markdown complejo para tests avanzados.
    
    Returns:
        str: Markdown con múltiples elementos
    """
    return """# Documento Complejo


Este documento contiene **múltiples** elementos de *Markdown*.


1. Primer nivel
   - Segundo nivel
   - Otro item
     - Tercer nivel
2. Continuación


```javascript
function calculate(x, y) {
    return x + y;
}
```


| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Info     | Content  |


[Link a Google](https://google.com)


> Esta es una cita
> en múltiples líneas

---


Este párrafo tiene **negrita**, *cursiva*, `código inline`, y ~~tachado~~.
"""