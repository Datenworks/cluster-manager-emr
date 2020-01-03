import boto3


def execute(event, context):
    cluster_id = event.get("JobFlowId")
    emr_client = boto3.client('emr')
    steps = emr_client.list_steps(ClusterId=cluster_id)
    step = steps.get("Steps")[0]
    status = step.get("Status")

    if status.get("State") == "COMPLETED":
        delete_cluster(emr_client, cluster_id)
        return {"State": "COMPLETED"}

    elif status.get("State") == "RUNNING" or \
            status.get("State") == "PENDING":
        event.update({"State": "RUNNING"})
        return event

    else:
        delete_cluster(emr_client, cluster_id)
        return failed_step(status)


def failed_step(status):
    response = {
        "State": "FAILED",
        "Cause": status.get("FailureDetails").get("Reason", "Unknown"),
        "Error": status.get("FailureDetails").get("Message", "Unknown")
    }
    return response


def delete_cluster(emr_client, cluster_id):
    emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
