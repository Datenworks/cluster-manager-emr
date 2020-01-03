resource "aws_kms_key" "default" {
  description             = var.description
  deletion_window_in_days = 10

  policy = var.policy

  tags = var.tags
}

resource "aws_kms_alias" "default" {
  name = "alias/${var.name}"

  target_key_id = aws_kms_key.default.key_id
}
