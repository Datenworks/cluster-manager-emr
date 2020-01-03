variable "kms_encrypt_key_for_s3" {
  description = "AWS KMS Key to encrypt data at rest in AWS S3"
  type        = string
  default     = ""
}

variable "kms_encrypt_key_for_ebs" {
  description = "AWS KMS Key to encrypt local EBS volumes in AWS EMR"
  type        = string
  default     = ""
}

variable "encryption_enabled" {
  description = "Whether or not to enable AWS EMR encryption for jobs (in transit and at rest)"
  type        = bool
  default     = false
}

variable "security_configuration_name" {
  description = "Name for the Security Configuration in AWS EMR"
  type        = string
  default     = "default-emr-encryption"
}

variable "aditional_policies_arns" {
  description = "List of ARN for the aditional policies for the AWS Step Functions role"
  type        = list(string)
  default     = []
}

variable "emr_description" {
  description = "Role to create EMR Clusters"
  default     = "Allows users to create EMR Cluster and run Job Flows"
}

variable "emr_role_name" {
  description = "What is the name for the EMR Default role?"
  type        = string
  default     = "EMR_DefaultRole"
}

variable "emr_policy_name" {
  description = "What is the name for the EMR Default Policy?"
  type        = string
  default     = "EMR_Policy"
}

variable "emr_ec2_description" {
  description = "Role to create EMR Clusters"
  default     = "Allows users to create EMR Cluster and run Job Flows"
}

variable "emr_ec2_role_name" {
  description = "What is the name for the EMR EC2 Default role?"
  type        = string
  default     = "EMR_EC2_DefaultRole"
}

variable "emr_ec2_path" {
  description = "Desired path for the IAM users and role"
  type        = string
  default     = "/"
}
