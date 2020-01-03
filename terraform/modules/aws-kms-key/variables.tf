variable "description" {
  description = "Application or solution name (e.g. `app`)"
  type        = string
}

variable "name" {
  description = "The key name (alias) to be attributed"
  type        = string
}

variable "policy" {
  description = "AWS IAM policy to control access for this KMS Key"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Map of tags to be added in KMS key"
  type        = map(string)
  default     = {}
}
