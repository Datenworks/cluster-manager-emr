data "aws_iam_policy_document" "default" {
  statement {
    sid = "AllowToAssumeStatesRole"

    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "states.amazonaws.com",
        "events.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "default" {
  name        = var.role_name
  path        = var.path
  description = "Allow Step Functions to access resources for Sfn"

  assume_role_policy = data.aws_iam_policy_document.default.json

  tags = var.tags
}

data "aws_iam_policy_document" "pass_role" {
  statement {
    sid       = "AllowToPass${var.role_name}"
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.default.arn]
  }
}

resource "aws_iam_policy" "pass_role" {
  name   = "AllowToExecuteECSTasksFor${var.role_name}"
  policy = data.aws_iam_policy_document.pass_role.json
}

resource "aws_iam_role_policy_attachment" "pass_role" {
  role       = aws_iam_role.default.name
  policy_arn = aws_iam_policy.pass_role.arn
}

resource "aws_iam_role_policy_attachment" "custom" {
  count = length(var.aditional_policies_arns)

  role       = aws_iam_role.default.name
  policy_arn = element(var.aditional_policies_arns, count.index)
}

resource "aws_sfn_state_machine" "default" {
  count = length(var.step_functions)

  name     = lookup(element(var.step_functions, count.index), "name")
  role_arn = aws_iam_role.default.arn

  definition = lookup(element(var.step_functions, count.index), "definition")
}
