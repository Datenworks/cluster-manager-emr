{
  "Comment": "${comment}",
  "StartAt": "CreateAndSubmit",
  "States": {
    "CreateAndSubmit": {
      "Type": "Task",
      "Resource": "${function_prefix}-create_and_submit",
      "InputPath": "$.data",
      "Next": "WatchAndDestroy"
    },
    "WatchAndDestroy": {
      "Type": "Task",
      "Resource": "${function_prefix}-monitor_cluster_step",
      "Next": "ChoiceState"
    },
    "ChoiceState": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.State",
          "StringEquals": "FAILED",
          "Next": "FailStateMachine"
        },
        {
          "Variable": "$.State",
          "StringEquals": "COMPLETED",
          "Next": "SuccessStateMachine"
        },
        {
          "Variable": "$.State",
          "StringEquals": "RUNNING",
          "Next": "RetryWatchAndDestroy"
        }
      ]
    },
    "FailStateMachine": {
      "Type": "Fail"
    },
    "SuccessStateMachine": {
      "Type": "Succeed"
    },
    "RetryWatchAndDestroy":{ 
      "Type": "Wait",
      "Seconds": 120,
      "Next": "WatchAndDestroy"
    }
  }
}
