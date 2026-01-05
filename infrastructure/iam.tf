# IAM role for Lambda
data "aws_iam_policy_document" "lambda-assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "rsrc-lambda-perm" {
  name               = "llm_md-lambda-execution-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume_role.json
}

# IAM policy for CloudWatch Logs
resource "aws_iam_role_policy_attachment" "rsrc-lambda_logs" {
  role       = aws_iam_role.rsrc-lambda-perm.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM policy for S3 access
data "aws_iam_policy_document" "s3-access-policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${aws_s3_bucket.rsrc-docx-bucket.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "rsrc-s3-access" {
  name = "llm_md-s3-access-policy"
  role = aws_iam_role.rsrc-lambda-perm.id

  policy = data.aws_iam_policy_document.s3-access-policy.json
}

# IAM policy for S3 web server
data "aws_iam_policy_document" "s3-web-server-policy" {
  statement {
    sid    = "PublicReadGetObject"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.rsrc-s3-web-host.arn}/*"
    ]
  }
}

# for Cloudfront access to the web bucket
data "aws_iam_policy_document" "s3-cloudfront-policy" {
  statement {
    sid    = "AllowCloudFrontAccess"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.rsrc-s3-web-host.arn}/*"
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.rsrc-web-distribution.arn]
    }
  }
}