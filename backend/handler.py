"""
AWS Lambda handler para el servicio de conversión MD -> DOCX.

Este es el punto de entrada cuando se ejecuta en Lambda.
"""

import json
import logging
from typing import Dict, Any

from app.converter.markdown_to_html import convert as md_to_html
from app.converter.html_to_docx import convert as html_to_docx
from app.storage.s3_client import S3Client
from app.utils.response import success, error, validation_error, internal_error
from app.config import config
from app.converter.exceptions import ConversionError

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler principal de Lambda.
    
    Args:
        event: Evento de API Gateway con formato:
            {
                "body": "{\"content\": \"# Title\", \"output_format\": \"docx\"}",
                "httpMethod": "POST",
                ...
            }
        context: Contexto de Lambda
    
    Returns:
        Dict con respuesta HTTP para API Gateway
        
    Supported conversions:
        - Markdown -> DOCX (output_format: "docx")
        - Markdown -> HTML (output_format: "html")
    """
    logger.info(f"Request ID: {context.aws_request_id}")
    
    http_method = event.get("httpMethod")  # REST API
    if not http_method and "requestContext" in event:
        # HTTP API v2
        http_method = event.get("requestContext", {}).get("http", {}).get("method")
    
    logger.info(f"HTTP Method: {http_method}")
    
    try:
        # 1. Para validar si es método HTTP
        if http_method != "POST":
            return error("Método no permitido. Use POST", status_code=405)
        
        # 2. Se parsea el body
        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError:
            return error("JSON inválido en el body", status_code=400)
        
        # 3. Validacion del input
        markdown_content = body.get("content")
        output_format = body.get("output_format", "docx").lower()
        
        # que se provea contenido
        if not markdown_content:
            return validation_error("content", "Campo requerido")
        
        # formato de salida
        if output_format not in ["docx", "html"]:
            return validation_error(
                "output_format",
                "Formato de salida inválido. Use: 'docx' o 'html'"
            )
        
        # 4. Tamaño permitido
        content_size = len(markdown_content.encode('utf-8'))
        if content_size > config.MAX_FILE_SIZE_BYTES:
            return error(
                f"Contenido demasiado grande. Máximo: {config.MAX_FILE_SIZE_MB}MB",
                status_code=413
            )
        
        logger.info(f"Processing {content_size} bytes, output: {output_format}")
        
				# En front: https://www.freeformatter.com/json-escape.html#before-output
				# Se debe formatear correctamente para que sea valido el json

        # 5. Markdown -> HTML
        try:
            html_content = md_to_html(markdown_content)
            logger.info("Markdown converted to HTML successfully")
        except Exception as e:
            logger.error(f"Markdown conversion failed: {str(e)}")
            return error(
                "Error al convertir Markdown",
                status_code=422,
                details={"error": str(e)}
            )
        
        # 6. Si el output es HTML, se retorna directamente
        if output_format == "html":
            logger.info("Returning HTML content directly")
            return success(
                data={
                    "html": html_content,
                    "output_format": output_format,
                    "size_bytes": len(html_content.encode('utf-8'))
                },
                message="Conversión completada exitosamente"
            )
        
        # 7. HTML -> DOCX
        try:
            docx_bytes = html_to_docx(html_content)
            logger.info(f"HTML converted to DOCX: {len(docx_bytes)} bytes")
        except Exception as e:
            logger.error(f"DOCX conversion failed: {str(e)}")
            return error(
                "Error al generar documento DOCX",
                status_code=500,
                details={"error": str(e)}
            )
        
        # 8. Subida a S3 y su URL
        try:
            s3_client = S3Client(use_mock=False)
            file_url = s3_client.upload_and_get_url(docx_bytes, output_format)
            logger.info(f"File uploaded to S3: {file_url}")
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            return error(
                "Error al subir archivo a S3",
                status_code=500,
                details={"error": str(e)}
            )
        
        # 9. Respuesta exitosa
        return success(
            data={
                "download_url": file_url,
                "output_format": output_format,
                "size_bytes": len(docx_bytes),
                "expires_in": config.PRESIGNED_URL_EXPIRY
            },
            message="Conversión completada exitosamente"
        )
        
    except Exception as e:
        logger.exception("Unhandled exception in lambda_handler")
        return internal_error(e)


def health_check(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Endpoint de health check.
    
    Returns:
        Respuesta simple indicando que el servicio está funcionando
    """
    return success(
        data={
            "status": "healthy",
            "version": "0.1.0",
            "environment": config.ENVIRONMENT
        },
        message="Service is running"
    )