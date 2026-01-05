"""
Excepciones personalizadas para el módulo de conversión.

Estas excepciones permiten manejo de errores específico del dominio
y facilitan el debugging y logging.
"""


class ConversionError(Exception):
    """
    Excepción base para errores de conversión
    
    Se usa esta clase como base para todas las excepciones
    relacionadas con conversión de formatos
    """
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class MarkdownConversionError(ConversionError):
    """
    Error al convertir Markdown a HTML
    
    Se lanza cuando hay problemas específicos con el parsing
    o procesamiento de Markdown
    """
    pass


class HTMLConversionError(ConversionError):
    """
    Error al convertir HTML a DOCX
    
    Se lanza cuando hay problemas con la generación del
    documento Word o con el parsing del HTML
    """
    pass


class InvalidInputError(ConversionError):
    """
    Error cuando el input no es válido
    
    Ejemplos:
    - String vacío
    - Formato incorrecto
    - Tipo de dato inesperado
    """
    pass


class StorageError(Exception):
    """
    Error relacionado con almacenamiento (S3, etc)
    
    Separada de ConversionError porque tiene contexto diferente
    """
    def __init__(self, message: str, bucket: str = None, key: str = None):
        self.message = message
        self.bucket = bucket
        self.key = key
        super().__init__(self.message)