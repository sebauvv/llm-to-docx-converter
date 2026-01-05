"""
Módulo para convertir Markdown a HTML.

Este módulo NO tiene dependencias de AWS, es lógica pura.
Puede ser testeado sin infraestructura.
"""

import markdown
from typing import Optional


def convert(markdown_text: str, extensions: Optional[list] = None) -> str:
    """
    Convierte texto Markdown a HTML.

    Args:
        markdown_text: String con contenido Markdown
        extensions: Lista de extensiones de markdown (opcional)

    Returns:
        String con HTML generado

    Raises:
        ValueError: Si el input es None o vacío
        Exception: Si hay error en la conversión

    Examples:
        >>> convert("# Hello")
        '<h1>Hello</h1>'

        >>> convert("**bold**")
        '<p><strong>bold</strong></p>'
    """
    if markdown_text is None:
        raise ValueError("El contenido Markdown no puede estar vacío")

    if not isinstance(markdown_text, str):
        raise TypeError("El contenido debe ser un string")

    if not markdown_text:
        raise ValueError("El contenido Markdown no puede estar vacío")

    # Extensiones por defecto si no se especifican
    if extensions is None:
        extensions = [
            "fenced_code",      # Para ```code blocks```
            "tables",           # Para tablas
            "nl2br",            # Convierte \n en <br> (me salvó)
            "sane_lists",       # Listas más consistentes
        ]

    try:
        html = markdown.markdown(
            markdown_text,
            extensions=extensions,
            output_format="html5"
        )
        return html
    except Exception as e:
        raise Exception(f"Error al convertir Markdown: {str(e)}")


def convert_with_metadata(markdown_text: str) -> dict:
    """
    Convierte Markdown a HTML y extrae metadata si existe.

    Útil para documentos con YAML front matter.

    Args:
        markdown_text: String con contenido Markdown

    Returns:
        Dict con 'html' y 'metadata'
    """
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",
            "sane_lists",
            "meta"  
        ]
    )

    html = md.convert(markdown_text)

    return {
        "html": html,
        "metadata": getattr(md, "Meta", {})
    }