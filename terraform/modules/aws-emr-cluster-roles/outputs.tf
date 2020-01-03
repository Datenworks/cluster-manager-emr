output "role_arn" {
  description = "ARN of the AWS IAM Role created for AWS EMR"
  value       = aws_iam_role.emr.arn
}

output "role_name" {
  description = "Name of the AWS IAM Role created for AWS EMR"
  value       = aws_iam_role.emr.name
}
