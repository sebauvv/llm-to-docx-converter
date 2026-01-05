resource "aws_apigatewayv2_api" "rsrc-api-md-converter" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["Content-Type"]
  }

  tags = {
    Name        = "${var.project_name}-api"
    Environment = var.environment
  }

}

resource "aws_apigatewayv2_integration" "rsrc-lambda-integration" {
  api_id                 = aws_apigatewayv2_api.rsrc-api-md-converter.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.rsrc-lambda-function.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "rsrc-api-convert-route" {
  api_id    = aws_apigatewayv2_api.rsrc-api-md-converter.id
  route_key = "POST /convert"
  target    = "integrations/${aws_apigatewayv2_integration.rsrc-lambda-integration.id}"
}

resource "aws_apigatewayv2_deployment" "rsrc-api-convert-deployment" {
  api_id = aws_apigatewayv2_api.rsrc-api-md-converter.id

  depends_on = [
    aws_apigatewayv2_route.rsrc-api-convert-route
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_apigatewayv2_stage" "rsrc-api-default-stage" {
  api_id      = aws_apigatewayv2_api.rsrc-api-md-converter.id
  name        = "$default"
  auto_deploy = true

  tags = {
    Name        = "${var.project_name}-stage"
    Environment = var.environment
  }
}

# Perm for API Gateway to invoke Lambda
resource "aws_lambda_permission" "rsrc-apigw-lambda-perm" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rsrc-lambda-function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.rsrc-api-md-converter.execution_arn}/*/*"
}