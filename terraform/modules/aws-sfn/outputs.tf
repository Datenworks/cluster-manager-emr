output "role_arn" {
  value       = aws_iam_role.default.arn
  description = "Default AWS IAM role for Step Functions"
}

output "sfn_state_machine_arns" {
  value       = aws_sfn_state_machine.default.*.id
}
