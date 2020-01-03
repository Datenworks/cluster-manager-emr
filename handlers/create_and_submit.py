import base64
import boto3
import json

from datetime import datetime


def execute(event, context):
    if not isinstance(event, dict):
        event = base64.b64decode(event)
        event = json.loads(event.decode('utf-8'))

    job_name = event.get('name')
    resource = event.get('resource')
    namespace = event.get('namespace')
    mem_executor = event.get('mem_executor', '16G')
    mem_driver = event.get('mem_driver', '8G')
    custom_arguments = [{
        "Key": "--conf", "Value": f"{namespace}."
                                  f"{argument.get('argument')}"
                                  f"={argument.get('value')}"}
                        for argument in event.get("arguments")]

    date = datetime.now().isoformat()

    prefix = "spark.hadoop."

    connection = boto3.client('emr', region_name=event.get('region'))

    spark_packages = ",".join(event.get("spark_packages"))

    core_instance_count = int(event.get('count'))

    instance_groups = [
        {
            "InstanceCount": 1,
            "Market": "ON_DEMAND",
            "Name": "MasterInstanceGroup",
            "InstanceRole": "MASTER",
            "InstanceType": event.get("master_type", "m5.xlarge")
        },
        {
            "InstanceCount": core_instance_count,
            "Market": "SPOT",
            "Name": "CoreInstanceGroup",
            "InstanceRole": "CORE",
            "InstanceType": event.get("slave_type", "m5.2xlarge"),
            "AutoScalingPolicy": {
                "Constraints": {
                    "MinCapacity": (core_instance_count // 2),
                    "MaxCapacity": int(core_instance_count * 3)
                },
                "Rules": [
                    {
                        "Name": "Default-scale-out",
                        "Description": "Replicates the default "
                                       "scale-out rule in the console "
                                       "for YARN memory.",
                        "Action": {
                            "SimpleScalingPolicyConfiguration": {
                                "AdjustmentType": "CHANGE_IN_CAPACITY",
                                "ScalingAdjustment": 1,
                                "CoolDown": 300
                            }
                        },
                        "Trigger": {
                            "CloudWatchAlarmDefinition": {
                                "ComparisonOperator": "LESS_THAN",
                                "EvaluationPeriods": 1,
                                "MetricName": "YARNMemoryAvailablePercentage",
                                "Namespace": "AWS/ElasticMapReduce",
                                "Period": 300,
                                "Threshold": 15,
                                "Statistic": "AVERAGE",
                                "Unit": "PERCENT",
                                "Dimensions": [
                                    {
                                        "Key": "JobFlowId",
                                        "Value": "${emr.clusterId}"
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        }
    ]

    # Not being used at the moment
    instance_fleets = [
                {
                    'Name': 'CoreInstanceFleet',
                    'InstanceFleetType': 'CORE',
                    'TargetOnDemandCapacity': int(core_instance_count * .2),
                    'TargetSpotCapacity': int(core_instance_count * .8),
                    'InstanceTypeConfigs': [{
                        'InstanceType': event.get("slave_type")
                    }],
                    'LaunchSpecifications': {
                        'SpotSpecification': {
                            'TimeoutDurationMinutes': 3,
                            'TimeoutAction': 'SWITCH_TO_ON_DEMAND'
                        }
                    }
                }
            ]

    arguments = ['spark-submit', '--packages', spark_packages,
                 '--conf', f'spark.executor.memory={mem_executor}',
                 '--conf', f'spark.driver.memory={mem_driver}']

    for custom_argument in custom_arguments:
        arguments.append(custom_argument['Key'])
        arguments.append(f"{prefix}{custom_argument['Value']}")

    if event.get('pyfiles') is not None:
        arguments.append('--py-files')
        arguments.append(event.get('pyfiles'))

    arguments.append(event.get('entrypoint'))

    response = connection.run_job_flow(
        Name=f'{job_name}-{resource}-spark-job',
        LogUri=event.get('log_bucket'),
        ReleaseLabel=event.get('release'),
        Applications=[{'Name': 'Spark'}],
        Instances={
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'InstanceGroups': instance_groups,
            'Ec2SubnetId': event.get('subnet')
        },
        SecurityConfiguration="emr-data-encryption",
        AutoScalingRole="EMR_AutoScaling_DefaultRole",
        VisibleToAllUsers=True,
        Steps=[{
            'Name': f'{job_name}-{resource}-{date}',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': arguments
            }
        }],
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole'
    )

    return response
