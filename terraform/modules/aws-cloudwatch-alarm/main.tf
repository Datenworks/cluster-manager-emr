resource "aws_cloudwatch_metric_alarm" "default" {
  alarm_name          = var.alarm_name
  alarm_description   = var.alarm_description
  comparison_operator = var.comparison_operation
  evaluation_periods  = var.evaluation_periods
  threshold           = var.threshold
  namespace           = var.namespace
  metric_name         = var.metric_name
  period              = var.metric_period
  statistic           = var.metric_stat
  dimensions = {
    StateMachineArn = var.metric_dimensions
  }
  alarm_actions      = var.alarm_actions
  treat_missing_data = var.treat_missing_data
}
