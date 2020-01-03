resource "aws_emr_security_configuration" "default" {
  count = var.encryption_enabled ? 1 : 0

  name = var.security_configuration_name

  configuration = jsonencode({
    EncryptionConfiguration = {
      AtRestEncryptionConfiguration = {
        S3EncryptionConfiguration = {
          EncryptionMode = (var.kms_encrypt_key_for_s3 != "") ? "SSE-KMS" : "SSE-S3"
          AwsKmsKey      = var.kms_encrypt_key_for_s3
        }
        LocalDiskEncryptionConfiguration = {
          EnableEbsEncryption       = true
          EncryptionKeyProviderType = "AwsKms"
          AwsKmsKey                 = var.kms_encrypt_key_for_ebs
        }
      }
      EnableInTransitEncryption = false
      EnableAtRestEncryption    = true
    }
  })
}

# EMR EC2 Configurations
data "aws_iam_policy_document" "emr_ec2_default_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "emr_ec2" {
  name        = var.emr_ec2_role_name
  description = var.emr_ec2_description

  assume_role_policy = data.aws_iam_policy_document.emr_ec2_default_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "emr_ec2" {
  role       = aws_iam_role.emr_ec2.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "emr_ec2_custom" {
  count = length(var.aditional_policies_arns)

  role       = aws_iam_role.emr_ec2.name
  policy_arn = element(var.aditional_policies_arns, count.index)
}

resource "aws_iam_instance_profile" "emr_ec2_instance_profile" {
  name = aws_iam_role.emr_ec2.name
  role = aws_iam_role.emr_ec2.name
}

# EMR
data "aws_iam_policy_document" "emr_default_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["elasticmapreduce.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "emr" {
  name        = var.emr_role_name
  description = var.emr_description

  assume_role_policy = data.aws_iam_policy_document.emr_default_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "emr" {
  count = length(var.aditional_policies_arns)

  role       = aws_iam_role.emr.name
  policy_arn = element(var.aditional_policies_arns, count.index)
}

resource "aws_iam_role_policy_attachment" "emr_custom" {
  role       = aws_iam_role.emr.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}
