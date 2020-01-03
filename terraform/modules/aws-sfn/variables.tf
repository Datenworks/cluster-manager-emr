variable "role_name" {
  description = "Name for the AWS IAM service role for this State Machine"
  type        = string
  default     = "AllowPermissionsForSfn"
}

variable "path" {
  description = "Desired path for the IAM configurations and roles"
  type        = string
  default     = "/service-role/"
}

variable "aditional_policies_arns" {
  description = "List of ARN for the aditional policies for the AWS Step Functions role"
  type        = list(string)
  default     = []
}

variable "region" {
  description = "The AWS region for the resources"
  type        = string
  default     = "us-east-1"
}

variable "step_functions" {
  description = "List of AWS Step Functions map configurations"
  type        = list(map(string))
}

variable "tags" {
  description = "Tags to be added to resources"
  type        = map(string)
}
