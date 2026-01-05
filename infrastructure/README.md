# Infrastructure overview

## Services Used:

- **S3**
  - Bucket as storage for uploaded and converted files.
  - Hosting for the frontend as a static website (cheap alternative instead of a EC2 instance).

- **AWS Lambda**
  - Cheap execution of the backend logic for the docx conversion.

- **Amazon API Gateway**
  - Exposes REST API endpoints to trigger Lambda functions.

- **Amazon CloudFront**
  - Distributes the static website globally over HTTPS using the default CloudFront domain (No custom domain added yet).

- **Amazon CloudWatch**
  - Collects logs and metrics for Lambda and API Gateway.

- **AWS IAM**
  - Basic permissions and roles for secure access between services.
