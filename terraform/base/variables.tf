variable "environment" {
  description = "The environment identifier"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "The AWS region that will host the resources"
  type        = string
  default     = "us-east-1"
}

variable "azs" {
  description = "The AWS availability zones that could receive subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}
