output "key_id" {
  value = aws_kms_key.default.key_id
}

output "arn" {
  value = aws_kms_key.default.arn
}

output "alias" {
  value = aws_kms_alias.default.arn
}
