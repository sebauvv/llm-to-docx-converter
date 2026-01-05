
# Bucket config
resource "aws_s3_bucket" "rsrc-docx-bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "${var.project_name}-files"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "rsrc-cleanup" {
  bucket = aws_s3_bucket.rsrc-docx-bucket.id

  rule {
    id     = "delete-old-files"
    status = "Enabled"
    filter {}

    expiration {
      days = 3
    }
  }
}

resource "aws_s3_bucket_public_access_block" "rsrc-docx-public-access" {
  bucket = aws_s3_bucket.rsrc-docx-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "rsrc-docx-versioning" {
  bucket = aws_s3_bucket.rsrc-docx-bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "rsrc-docx-cors" {
  bucket = aws_s3_bucket.rsrc-docx-bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}