resource "aws_s3_bucket" "rsrc-s3-web-host" {
  bucket = var.bucket_web_server_name
}

resource "aws_s3_bucket_ownership_controls" "rsrc-s3-web-host-ownership" {
  bucket = aws_s3_bucket.rsrc-s3-web-host.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }

}

resource "aws_s3_bucket_policy" "rsrc-s3-web-host-policy" {
  bucket = aws_s3_bucket.rsrc-s3-web-host.id
  policy = data.aws_iam_policy_document.s3-web-server-policy.json
}

resource "aws_s3_bucket_public_access_block" "rsrc-s3-public-access-block" {
  bucket = aws_s3_bucket.rsrc-s3-web-host.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "rsrc-s3-web-host-acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.rsrc-s3-web-host-ownership,
    aws_s3_bucket_public_access_block.rsrc-s3-public-access-block
  ]

  bucket = aws_s3_bucket.rsrc-s3-web-host.id
  acl    = "public-read"
}

# resource "aws_s3_bucket_website_configuration" "rsrc-s3-website-config" {
#   bucket = aws_s3_bucket.rsrc-s3-web-host.id

#   index_document {
#     suffix = "index.html"
#   }

# }

resource "aws_s3_object" "rsrc-s3-website-files" {
  for_each = fileset("../frontend/dist", "**")

  bucket = aws_s3_bucket.rsrc-s3-web-host.id
  key    = each.value
  source = "../frontend/dist/${each.value}"
  content_type = lookup({
    "html" = "text/html"
    "css"  = "text/css"
    "js"   = "application/javascript"
    "json" = "application/json"
    "png"  = "image/png"
    "jpg"  = "image/jpeg"
    "svg"  = "image/svg+xml"
    "ico"  = "image/x-icon"
    "webp" = "image/webp"
  }, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream")

  etag = filemd5("../frontend/dist/${each.value}")
}

resource "aws_s3_bucket_policy" "rsrc-s3-cloudfront-host-policy" {
  bucket = aws_s3_bucket.rsrc-s3-web-host.id
  policy = data.aws_iam_policy_document.s3-cloudfront-policy.json
}
