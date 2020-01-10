variable "encryption_enabled" {
  description = "Whether or not to enable AWS EMR encryption for jobs (in transit and at rest)"
  type        = bool
  default     = false
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
