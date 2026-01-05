
resource "aws_lambda_function" "rsrc-lambda-function" {
  filename         = "../backend/function.zip"
  function_name    = "${var.project_name}-converter"
  role             = aws_iam_role.rsrc-lambda-perm.arn
  handler          = "handler.lambda_handler"
  source_code_hash = filebase64sha256("../backend/function.zip")
  memory_size      = var.lambda_memory_mb
  timeout          = var.lambda_timeout_seconds
  runtime          = "python3.13"

  environment {
    variables = {
      ENVIRONMENT      = var.environment
      BUCKET_NAME      = aws_s3_bucket.rsrc-docx-bucket.bucket
      URL_EXPIRY       = var.url_expiry_seconds
      MAX_FILE_SIZE_MB = 10
      LOG_LEVEL        = "INFO"
    }
  }

  tags = {
    Name        = "${var.project_name}-lambda-function"
    Environment = var.environment
  }
}