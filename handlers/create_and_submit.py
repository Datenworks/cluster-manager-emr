from datetime import datetime
from os import getenv
from lib.aws.emr.cluster import (AwsEmrCluster,
                                 AwsEmrInstance,
                                 AwsEmrInstanceGroup)

from lib.aws.emr.step import AwsEmrStep
from lib.aws.emr.client import AwsEmrClient
from lib.aws.clustermanager.consumer import EmrInputParser
import time
from uuid import uuid4
EMR_MASTER_SG = getenv('EMR_MASTER_SG')
EMR_SLAVE_SG = getenv('EMR_SLAVE_SG')
EMR_SERVICE_ACCESS_SG = getenv('EMR_SERVICE_ACCESS_SG')

SECURITY_CONFIGURATION = getenv("SECURITY_CONFIGURATION")
AUTOSCALING_ROLE = getenv("AUTOSCALING_ROLE")
JOB_FLOW_ROLE = getenv("JOB_FLOW_ROLE")
SERVICE_ROLE = getenv("SERVICE_ROLE")


def execute(event, context):
    input_parse = EmrInputParser(event)
    date = datetime.now().isoformat()
    emr_client = AwsEmrClient()

    arguments = ['spark-submit',
                 '--conf', f'spark.executor.memory={input_parse.mem_executor}',
                 '--conf', f'spark.driver.memory={input_parse.mem_driver}']

    arguments.extend(input_parse.spark_packages)
    arguments.extend(input_parse.arguments)
    arguments.extend(input_parse.jar_files)
    arguments.extend(input_parse.pyfiles)
    arguments.append(input_parse.entrypoint)

    bootstrap_steps = input_parse.bootstrap_steps
    aws_instance_group = \
        AwsEmrInstanceGroup(master_type=input_parse.master_type,
                            core_type=input_parse.core_type,
                            core_instance_count=input_parse.count)
    aws_instance = \
        AwsEmrInstance(subnet_id=input_parse.subnet,
                       master_security_group=EMR_MASTER_SG,
                       core_security_group=EMR_SLAVE_SG,
                       service_access_security_group=EMR_SERVICE_ACCESS_SG,
                       instance_groups=aws_instance_group)
    aws_cluster = \
        AwsEmrCluster(cluster_name=input_parse.name,
                      log_uri=input_parse.log_bucket,
                      release=input_parse.release,
                      applications=[{"Name": "Spark"}],
                      instances=aws_instance,
                      multiple_steps=input_parse.multiple_steps,
                      auto_scaling_role=AUTOSCALING_ROLE,
                      job_flow_role=JOB_FLOW_ROLE,
                      service_role=SERVICE_ROLE)

    for bootstrap_step in bootstrap_steps:
        step = AwsEmrStep(step_name='bootstrap_step',
                          arguments=bootstrap_step)

        emr_client.execute_step(aws_cluster, step.get_step())
        time.sleep(60)

    step_name = f'{input_parse.name}-' \
                f'{input_parse.resource}-' \
                f'{date}-' \
                f'{str(uuid4())}'

    step = AwsEmrStep(step_name=step_name,
                      arguments=arguments)
    print(step.get_step())
    response = emr_client.execute_step(aws_cluster, step.get_step())
    response.update({"step_name": step_name})
    return response
