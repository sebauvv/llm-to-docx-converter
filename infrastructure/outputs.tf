output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint
}

output "convert_url" {
  description = "Full URL for conversion endpoint"
  value       = "${aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint}/convert"
}

output "s3_bucket_name" {
	description = "S3 bucket name for DOCX storage"
	value       = aws_s3_bucket.rsrc-docx-bucket.bucket
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.rsrc-lambda-function.function_name
}

output "cloudfront_url" {
  description = "CloudFront HTTPS URL"
  value       = "https://${aws_cloudfront_distribution.rsrc-web-distribution.domain_name}"
}


# Outputs for GitHub Actions Secrets
output "github_actions_aws_access_key_id" {
  description = "AWS Access Key ID for GitHub Actions"
  value       = aws_iam_access_key.github_actions.id
  sensitive   = false
}

output "github_actions_aws_secret_access_key" {
  description = "AWS Secret Access Key for GitHub Actions"
  value       = aws_iam_access_key.github_actions.secret
  sensitive   = true
}

output "s3_web_bucket_name" {
  description = "S3 bucket name for frontend hosting"
  value       = aws_s3_bucket.rsrc-s3-web-host.bucket
}

output "cloudfront_distribution_id" {
  description = "CloudFront Distribution ID for cache invalidation"
  value       = aws_cloudfront_distribution.rsrc-web-distribution.id
}

output "vite_api_url" {
  description = "API URL for frontend environment variable"
  value       = "${aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint}/convert"
}

output "github_secrets_setup" {
  description = "Instructions for setting up GitHub Secrets"
  value       = <<-EOT
  
    Required Secrets:
    -----------------
    AWS_ACCESS_KEY_ID: ${aws_iam_access_key.github_actions.id}
    AWS_SECRET_ACCESS_KEY: ${nonsensitive(aws_iam_access_key.github_actions.secret)}
    S3_BUCKET_NAME: ${aws_s3_bucket.rsrc-s3-web-host.bucket}
    S3_STORAGE_BUCKET: ${aws_s3_bucket.rsrc-docx-bucket.bucket}
    CLOUDFRONT_DISTRIBUTION_ID: ${aws_cloudfront_distribution.rsrc-web-distribution.id}
    LAMBDA_FUNCTION_NAME: ${aws_lambda_function.rsrc-lambda-function.function_name}
    VITE_API_URL: ${aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint}/convert
    
    NOTE: Store AWS_SECRET_ACCESS_KEY securely. This value won't be shown again.
  EOT
}