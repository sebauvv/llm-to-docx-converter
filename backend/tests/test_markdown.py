"""
Tests para el módulo de conversión Markdown -> HTML.

Cubre casos normales, edge cases y errores.
"""

import pytest
from app.converter.markdown_to_html import convert, convert_with_metadata
from app.converter.exceptions import InvalidInputError


class TestMarkdownToHTML:
    """Tests para conversión básica de Markdown a HTML."""
    
    def test_simple_header(self):
        """Test conversión de header simple."""
        markdown = "# Hello World"
        html = convert(markdown)
        
        assert "<h1>Hello World</h1>" in html
        assert isinstance(html, str)
    
    def test_bold_text(self):
        """Test conversión de texto en negrita."""
        markdown = "**bold text**"
        html = convert(markdown)
        
        assert "<strong>bold text</strong>" in html
    
    def test_italic_text(self):
        """Test conversión de texto en cursiva."""
        markdown = "*italic text*"
        html = convert(markdown)
        
        assert "<em>italic text</em>" in html
    
    def test_unordered_list(self):
        """Test conversión de lista no ordenada."""
        markdown = """
- Item 1
- Item 2
- Item 3
"""
        html = convert(markdown)
        
        assert "<ul>" in html
        assert "<li>Item 1</li>" in html
        assert "<li>Item 2</li>" in html
        assert "<li>Item 3</li>" in html
        assert "</ul>" in html
    
    def test_ordered_list(self):
        """Test conversión de lista ordenada."""
        markdown = """
1. First
2. Second
3. Third
"""
        html = convert(markdown)
        
        assert "<ol>" in html
        assert "<li>First</li>" in html
        assert "</ol>" in html
    
    def test_code_block(self):
        """Test conversión de bloque de código."""
        markdown = """
```python
def hello():
    print("world")
```
"""
        html = convert(markdown)
        
        assert "<code>" in html or "<pre>" in html
        assert "def hello():" in html
    
    def test_inline_code(self):
        """Test conversión de código inline."""
        markdown = "Use `print()` function"
        html = convert(markdown)
        
        assert "<code>print()</code>" in html
    
    def test_table(self):
        """Test conversión de tabla."""
        markdown = """
| Col 1 | Col 2 |
|-------|-------|
| A     | B     |
| C     | D     |
"""
        html = convert(markdown)
        
        assert "<table>" in html
        assert "<th>Col 1</th>" in html
        assert "<td>A</td>" in html
    
    def test_links(self):
        """Test conversión de links."""
        markdown = "[Google](https://google.com)"
        html = convert(markdown)
        
        assert '<a href="https://google.com">Google</a>' in html
    
    def test_multiple_headers(self):
        """Test múltiples niveles de headers."""
        markdown = """
"""
        html = convert(markdown)
        
        assert "<h1>H1</h1>" in html
        assert "<h2>H2</h2>" in html
        assert "<h3>H3</h3>" in html


class TestMarkdownEdgeCases:
    """Tests para casos especiales y edge cases."""
    
    def test_empty_string_raises_error(self):
        """Test que string vacío lanza error."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            convert("")
    
    def test_none_raises_error(self):
        """Test que None lanza error."""
        with pytest.raises(ValueError):
            convert(None)
    
    def test_non_string_raises_error(self):
        """Test que tipos incorrectos lanzan error."""
        with pytest.raises(TypeError, match="debe ser un string"):
            convert(123)
        
        with pytest.raises(TypeError):
            convert([])
        
        with pytest.raises(TypeError):
            convert({})
    
    def test_whitespace_only(self):
        """Test markdown con solo espacios."""
        markdown = "   \n\n   "
        html = convert(markdown)
        
        assert isinstance(html, str)
    
    def test_special_characters(self):
        """Test caracteres especiales HTML."""
        markdown = "< > & \" '"
        html = convert(markdown)
        
        assert isinstance(html, str)
        assert len(html) > 0
    
    def test_very_long_document(self):
        """Test documento muy largo."""
        markdown = "# Header\n\n" + ("Paragraph text. " * 1000)
        html = convert(markdown)
        
        assert "<h1>Header</h1>" in html
        assert len(html) > len(markdown)
    
    def test_mixed_content(self, sample_markdown):
        """Test documento con contenido mixto."""
        html = convert(sample_markdown)
        
        assert "<h1>" in html
        assert "<h2>" in html
        assert "<ul>" in html
        assert "<strong>" in html
        assert "<em>" in html


class TestMarkdownWithMetadata:
    """Tests para conversión con metadata."""
    
    def test_convert_with_metadata_basic(self):
        """Test conversión con metadata básica."""
        markdown = "# Test"
        result = convert_with_metadata(markdown)
        
        assert "html" in result
        assert "metadata" in result
        assert isinstance(result["html"], str)
        assert isinstance(result["metadata"], dict)
    
    def test_metadata_extraction(self):
        """Test extracción de metadata YAML."""
        markdown = """---
title: Test Document
author: John Doe
---

"""
        result = convert_with_metadata(markdown)
        
        assert "html" in result
        assert "metadata" in result


class TestCustomExtensions:
    """Tests para extensiones personalizadas de Markdown."""
    
    def test_custom_extensions(self):
        """Test con extensiones personalizadas."""
        markdown = "# Test"
        html = convert(markdown, extensions=["extra"])
        
        assert "<h1>Test</h1>" in html
    
    def test_no_extensions(self):
        """Test sin extensiones."""
        markdown = "# Test"
        html = convert(markdown, extensions=[])
        
        assert "<h1>Test</h1>" in html


class TestComplexMarkdown:
    """Tests para documentos Markdown complejos."""
    
    def test_nested_lists(self):
        """Test listas anidadas."""
        markdown = """
- Level 1
  - Level 2
    - Level 3
"""
        html = convert(markdown)
        
        assert "<ul>" in html
        assert "<li>Level 1" in html
    
    def test_mixed_formatting(self):
        """Test formato mixto en mismo párrafo."""
        markdown = "**Bold** and *italic* and `code`"
        html = convert(markdown)
        
        assert "<strong>Bold</strong>" in html
        assert "<em>italic</em>" in html
        assert "<code>code</code>" in html
    
    def test_blockquotes(self):
        """Test bloques de cita."""
        markdown = "> This is a quote"
        html = convert(markdown)
        
        assert "<blockquote>" in html
        assert "This is a quote" in html
    
    def test_horizontal_rule(self):
        """Test línea horizontal."""
        markdown = "---"
        html = convert(markdown)
        
        assert "<hr" in html


class TestPerformance:
    """Tests de performance."""
    
    def test_conversion_speed(self, sample_markdown):
        """Test que la conversión es rápida."""
        import time
        
        start = time.time()
        convert(sample_markdown)
        duration = time.time() - start
        
        assert duration < 1.0
    
    def test_multiple_conversions(self):
        """Test múltiples conversiones consecutivas."""
        markdown = "# Test"
        
        for _ in range(100):
            html = convert(markdown)
            assert "<h1>Test</h1>" in html