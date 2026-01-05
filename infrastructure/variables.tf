variable "project_name" {
  description = "Project name"
  type        = string
  default     = "llm_md-to-docx"
}

variable "environment" {
  description = "Environment (DEVELOPMENT, PROD)"
  type        = string
  default     = "PROD"
}

variable "bucket_name" {
  description = "S3 bucket name for converted files"
  type        = string
  default     = "llmmd-to-docx-storage"
}

variable "bucket_web_server_name" {
  type    = string
  default = "llmmd-to-docx"
}

variable "lambda_memory_mb" {
  description = "Lambda memory in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout_seconds" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "url_expiry_seconds" {
  description = "Presigned URL expiry time"
  type        = number
  default     = 300
}

variable "aws_profile" {
	description = "AWS CLI profile to use"
	type        = string
	default     = "Ecomm-Seba"
}