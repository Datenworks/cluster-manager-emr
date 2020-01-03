
output "environment" {
  description = "Current environment configuration for this base"
  value       = var.environment
}

output "aws_account_id" {
  description = "The AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "Region containing the base resources"
  value       = var.region
}