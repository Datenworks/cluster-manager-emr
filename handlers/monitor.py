from lib.aws.emr.client import AwsEmrClient

emr_client = AwsEmrClient()


def is_step_running(step):
    return step['Status']['State'] == 'PENDING' or \
        step['Status']['State'] == 'RUNNING'


def is_step_completed(step):
    return step['Status']['State'] == 'COMPLETED'


def execute(event, context):
    cluster_id = event.get("JobFlowId")
    step_name = event.get("step_name")

    step = emr_client.\
        get_step_by_name(cluster_id=cluster_id, step_name=step_name)

    steps_running = emr_client.list_steps_running(cluster_id=cluster_id)
    if len(steps_running['Steps']) == 0:
        emr_client.destroy_cluster(cluster_id)

    if is_step_running(step):
        event.update({"State": "RUNNING"})
    elif is_step_completed(step):
        event.update({"State": "COMPLETED"})
    else:
        event.update({"State": "FAILED"})
        event.update(step['Status']['FailureDetails'])
    return event
