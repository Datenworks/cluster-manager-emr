data "aws_caller_identity" "current" {}

module "aws_emr_cluster_roles" {
  source = "../modules/aws-emr-cluster-roles"
}

module "aws_alarms_sns_topic" {
  source  = "terraform-aws-modules/sns/aws"
  version = "~> 2.0"

  name = "monitoring-alarms"
}

locals {
  cluster_manager_sfn_definitions = [
    {
      comment = "Step Functions State Machine responsible control the flow of a job in EMR CLuster, Create, Submit, Watch and Destroy"
      name    = "cluster-manager-sfn"
    }
  ]
}

data "template_file" "cluster_manager_sfn_definitions" {
  count    = length(local.cluster_manager_sfn_definitions)
  template = file("../templates/clusterManager.json.tpl")

  vars = {
    function_prefix = format(
      "arn:aws:lambda:%s:%s:function:cluster-job-manager-%s",
      var.region,
      data.aws_caller_identity.current.account_id,
      var.environment
    )

    comment = lookup(element(local.cluster_manager_sfn_definitions, count.index), "comment")
  }
}

module "aws_cluster_manager_step_functions" {
  source = "../modules/aws-sfn"

  role_name = "ClusterManagerSfnRole"

  aditional_policies_arns = [
    "arn:aws:iam::aws:policy/IAMFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchEventsFullAccess",
    "arn:aws:iam::aws:policy/AWSLambdaFullAccess",
    "arn:aws:iam::aws:policy/AdministratorAccess" # DELETE ME if you can!
  ]

  step_functions = [
    for sfn_definition in local.cluster_manager_sfn_definitions :
    {
      name = lookup(sfn_definition, "name"),
      definition = data.template_file.cluster_manager_sfn_definitions[
        index(local.cluster_manager_sfn_definitions, sfn_definition)
      ].rendered
    }
  ]

  tags = {
    Provisioned = "Terraform"
  }
}

module "aws_cloudwatch_alarm_cluster_manager" {
  source               = "../modules/aws-cloudwatch-alarm"
  alarm_name           = "cluster-manager-alarm-step-function"
  alarm_description    = "Check if the Cluster Manager - JobFlowId return an error"
  comparison_operation = "GreaterThanOrEqualToThreshold"
  evaluation_periods   = 1
  threshold            = 1

  namespace         = "AWS/States"
  metric_name       = "ExecutionsFailed"
  metric_period     = 60
  metric_stat       = "Maximum"
  metric_dimensions = module.aws_cluster_manager_step_functions.sfn_state_machine_arns[0]

  alarm_actions = [
    module.aws_alarms_sns_topic.this_sns_topic_arn
  ]

  treat_missing_data = "notBreaching"   
}
