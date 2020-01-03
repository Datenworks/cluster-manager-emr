variable "alarm_name" {
  type        = string
  description = "What will be the name of the alarm?"
}

variable "alarm_description" {
  type        = string
  description = "Descript here what you alarm will do"
}

variable "comparison_operation" {
  type        = string
  description = "What will be the comparison of your alarm?"
}

variable "evaluation_periods" {
  type        = number
  description = "Period that cloudwatch alarm will be check for errors"
}

variable "threshold" {
  type        = number
  description = "Limit that cloudwatch will be tolerate for trigger an alarm"
}

variable "namespace" {
  type = string
  description = "The type of resource for the cloudwatch alarm will be watching, example AWS/Lambda"
}

variable "metric_name" {
  type = string
  description = "The name of the metric, such ExecutionFailed, the metric to be watched in cloudwatch alarm"
}

variable "metric_period" {
  type = number
  description = "The period in seconds for cloudwatch alarm trigger the alarm"
}

variable "metric_stat" {
  type = string
  description = "What will be the stat for consider in alarm? A SampleCount? a Sum?"
}

variable "metric_dimensions" {
  type = string
  description = "Put de ARN of resource to be watched"
}

variable "alarm_actions" {
  type = list(string)
  description = "What will be de action when the alarm is triggered? Put a message in a sns queue? Send the arn of the resource"
}

variable "treat_missing_data" {
  type = string
  description = "How will be treated the state of missing data by the alarm"
}
