output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint
}

output "convert_url" {
  description = "Full URL for conversion endpoint"
  value       = "${aws_apigatewayv2_api.rsrc-api-md-converter.api_endpoint}/convert"
}

output "s3_bucket_name" {
  description = "S3 bucket for converted files"
  value       = aws_s3_bucket.rsrc-docx-bucket.bucket
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.rsrc-lambda-function.function_name
}

# output "s3_web_server_url" {
#   description = "S3 Website URL"
#   value       = aws_s3_bucket_website_configuration.rsrc-s3-website-config.website_endpoint
# }

output "cloudfront_url" {
  description = "CloudFront HTTPS URL"
  value       = "https://${aws_cloudfront_distribution.rsrc-web-distribution.domain_name}"
}