#!/usr/bin/env python3
"""
Script para probar el flujo completo localmente SIN AWS.

1. Convierte Markdown -> HTML
2. Convierte HTML -> DOCX
3. Guarda archivo localmente
4. Usa mock de S3

ex: python local_test.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.converter.markdown_to_html import convert as md_to_html
from app.converter.html_to_docx import convert as html_to_docx
from app.storage.s3_client import S3Client


def test_markdown_conversion():
    """Test conversión de Markdown a HTML."""
    print("=" * 60)
    print("TEST 1: Conversión Markdown -> HTML")
    print("=" * 60)
    
    markdown = """# Documento de Prueba

Este es un documento de **prueba** con *varios* elementos.

## Lista de características

- Convertir Markdown a HTML
- Convertir HTML a DOCX
- Guardar en S3 (o mock local)

## Código de ejemplo

```python
def hello():
    print("Hello World")
```

## Tabla

| Columna 1 | Columna 2 |
|-----------|-----------|
| Dato A    | Dato B    |
| Dato C    | Dato D    |

---

**Fin del documento**
"""
    
    try:
        html = md_to_html(markdown)
        print(" Conversión exitosa")
        print(f" Longitud HTML: {len(html)} caracteres")
        print(f" Primeros 200 caracteres:")
        print(html[:200] + "...")
        return html
    except Exception as e:
        print(f" Error: {e}")
        return None


def test_html_to_docx(html):
    """Test conversión de HTML a DOCX."""
    print("\n" + "=" * 60)
    print("TEST 2: Conversión HTML -> DOCX")
    print("=" * 60)
    
    try:
        docx_bytes = html_to_docx(html)
        print(" Conversión exitosa")
        print(f" Tamaño DOCX: {len(docx_bytes)} bytes ({len(docx_bytes)/1024:.2f} KB)")
        return docx_bytes
    except Exception as e:
        print(f" Error: {e}")
        return None


def test_s3_mock(docx_bytes):
    """Test guardado con S3 mock."""
    print("\n" + "=" * 60)
    print("TEST 3: Guardado con S3 Mock")
    print("=" * 60)
    
    try:
        client = S3Client(use_mock=True)
        url = client.upload_and_get_url(docx_bytes, "docx")
        
        print(" Guardado exitoso")
        print(f" URL: {url}")
        print(f" Ubicación: {url.replace('file://', '')}")
        
        file_path = Path(url.replace("file://", ""))
        if file_path.exists():
            print(f" Archivo verificado: {file_path.stat().st_size} bytes")
        else:
            print(" Archivo no encontrado")
        
        return url
    except Exception as e:
        print(f" Error: {e}")
        return None


def save_output_file(docx_bytes):
    """Guarda archivo DOCX en el directorio actual."""
    print("\n" + "=" * 60)
    print("TEST 4: archivo local")
    print("=" * 60)
    
    try:
        output_file = Path("output_test.docx")
        with open(output_file, "wb") as f:
            f.write(docx_bytes)
        
        print(f" Archivo guardado: {output_file.absolute()}")
        print(f" Tamaño: {output_file.stat().st_size} bytes")
        print("\n Abre el archivo para verificar el contenido")
        return output_file
    except Exception as e:
        print(f" Error: {e}")
        return None


def test_full_pipeline():
    """Test del pipeline completo."""
    print("TEST COMPLETO DEL PIPELINE")
    
    # Test 1: Markdown -> HTML
    html = test_markdown_conversion()
    if not html:
        print("\n Pipeline detenido: Error en conversión Markdown")
        return False
    
    # Test 2: HTML -> DOCX
    docx_bytes = test_html_to_docx(html)
    if not docx_bytes:
        print("\n Pipeline detenido: Error en conversión DOCX")
        return False
    
    # Test 3: S3 Mock
    url = test_s3_mock(docx_bytes)
    if not url:
        print("\n Pipeline detenido: Error en storage")
        return False
    
    # Test 4: Save localmente
    output_file = save_output_file(docx_bytes)
    if not output_file:
        print("\n Pipeline detenido: Error al guardar archivo")
        return False
    
    print("\n" + "=" * 60)
    print(" TODOS LOS TESTS PASARON")
    print("=" * 60)
    print(f"""
  
 Archivos generados:
  - {output_file.absolute()}
  - {url.replace('file://', '')}

""")
    
    return True


def test_edge_cases():
    """Test casos especiales."""
    print("\n" + "=" * 60)
    print("TEST ADICIONAL: Casos Especiales")
    print("=" * 60)
    
    test_cases = [
        ("Markdown simple", "# Hello"),
        ("Solo texto", "Plain text"),
        ("Con emojis", "# Test 💀💀💀💀🚀 "),
        ("Caracteres especiales", "< > & \" '"),
    ]
    
    success_count = 0
    for name, markdown in test_cases:
        try:
            html = md_to_html(markdown)
            docx_bytes = html_to_docx(html)
            success_count += 1
            print(f"{name}: OK")
        except Exception as e:
            print(f"{name}: {e}")
    
    print(f"\n Resultado: {success_count}/{len(test_cases)} casos exitosos")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          MD CONVERTER - TEST LOCAL                         ║
║          Testing sin AWS / sin infraestructura             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")
    
    success = test_full_pipeline()
    
    test_edge_cases()
    
    sys.exit(0 if success else 1)