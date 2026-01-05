"""
Módulo de conversión de formatos.

Provee funciones para convertir entre Markdown, HTML y DOCX.
"""

from .markdown_to_html import convert as md_to_html
from .html_to_docx import convert as html_to_docx
from .exceptions import (
    ConversionError,
    MarkdownConversionError,
    HTMLConversionError,
    InvalidInputError
)

__all__ = [
    "md_to_html",
    "html_to_docx",
    "ConversionError",
    "MarkdownConversionError",
    "HTMLConversionError",
    "InvalidInputError"
]