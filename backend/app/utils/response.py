"""
Utilidades para crear respuestas HTTP estandarizadas.

Centraliza el formato de respuestas para Lambda/API Gateway.
"""

import json
from typing import Any, Dict, Optional
from datetime import datetime


def success(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None
) -> dict:
    """
    Crea respuesta de éxito estandarizada.

    Args:
        data: Datos a retornar en el body
        status_code: Código HTTP (default: 200)
        message: Mensaje opcional de éxito
        headers: Headers HTTP adicionales

    Returns:
        Dict con formato esperado por API Gateway

    Example:
        >>> success({"url": "https://..."}, message="Conversión exitosa")
    """
    body = {
        "success": True,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

    if message:
        body["message"] = message

    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",  # Para CORS
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if headers:
        default_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body)
    }


def error(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[dict] = None,
    headers: Optional[Dict[str, str]] = None
) -> dict:
    """
    Crea respuesta de error estandarizada.

    Args:
        message: Mensaje descriptivo del error
        status_code: Código HTTP (default: 400)
        error_code: Código interno de error (opcional)
        details: Detalles adicionales del error
        headers: Headers HTTP adicionales

    Returns:
        Dict con formato esperado por API Gateway

    Example:
        >>> error("Formato inválido", 400, error_code="INVALID_FORMAT")
    """
    body = {
        "success": False,
        "error": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    if error_code:
        body["error_code"] = error_code

    if details:
        body["details"] = details

    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if headers:
        default_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body)
    }


def validation_error(field: str, reason: str) -> dict:
    """
    Respuesta específica para errores de validación.

    Args:
        field: Campo que falló la validación
        reason: Razón del fallo

    Returns:
        Dict con error 400
    """
    return error(
        message=f"Error de validación en campo '{field}'",
        status_code=400,
        error_code="VALIDATION_ERROR",
        details={"field": field, "reason": reason}
    )


def not_found(resource: str) -> dict:
    """
    Respuesta para recursos no encontrados.

    Args:
        resource: Nombre del recurso no encontrado

    Returns:
        Dict con error 404
    """
    return error(
        message=f"Recurso no encontrado: {resource}",
        status_code=404,
        error_code="NOT_FOUND"
    )


def internal_error(exception: Exception) -> dict:
    """
    Respuesta para errores internos del servidor.

    Args:
        exception: Excepción capturada

    Returns:
        Dict con error 500
    """
    return error(
        message="Error interno del servidor",
        status_code=500,
        error_code="INTERNAL_ERROR",
        details={"exception": str(exception)}
    )