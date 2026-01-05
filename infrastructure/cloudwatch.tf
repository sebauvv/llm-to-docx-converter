# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "custom-lambda-log-group"
  retention_in_days = 7

  tags = {
    Name = "llm_md-to-docx-converter-logs"
  }
}