# LLM MD Converter API

## Overview

Designed to be used via AWS Lambda and API Gateway.

---

## Endpoint

`POST /convert`

---

## Request

**Content-Type:** `application/json`

### Body Parameters

| Field          | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| `content`      | string | Yes      | Markdown text to convert                 |
| `output_format`| string | No       | Output format: `"docx"` or `"html"`      |

**Example:**

```json
{
  "content": "# Title\n\nThis is a test.",
  "output_format": "docx"
}
```

---

## Response

### Success

- **Status Code:** `200 OK`
- **Body:**

For `output_format: "docx"`:

```json
{
  "success": true,
  "data": {
    "download_url": "https://.../file.docx?X-Amz-...",
    "output_format": "docx",
    "size_bytes": 12345,
    "expires_in": 300
  },
  "timestamp": "2024-06-01T12:00:00.000Z",
  "message": "Conversión completada exitosamente"
}
```

For `output_format: "html"`:

```json
{
  "success": true,
  "data": {
    "html": "<h1>Title</h1><p>This is a test.</p>",
    "output_format": "html",
    "size_bytes": 56
  },
  "timestamp": "2024-06-01T12:00:00.000Z",
  "message": "Conversión completada exitosamente"
}
```

---

### Error

- **Status Code:** `4xx` or `5xx`
- **Body:**

```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2024-06-01T12:00:00.000Z",
  "error_code": "ERROR_TYPE",
  "details": { ... }
}
```

---


## Notes

- Maximum file size: 10 MB
- Supported output formats: `docx`, `html`
- Download URLs expire after 300 seconds (default)