class AwsEmrInstanceGroup:
    def __init__(self, master_type, core_type,
                 core_instance_count):
        self.master_type = master_type
        self.core_type = core_type
        self.core_instance_count = core_instance_count

    def get_instance_group(self):
        instances_group = [{
            "InstanceCount": 1,
            "Market": "ON_DEMAND",
            "Name": "MasterInstanceGroup",
            "InstanceRole": "MASTER",
            "InstanceType": self.master_type
        }, {
            "InstanceCount": self.core_instance_count,
            "Market": "SPOT",
            "Name": "CoreInstanceGroup",
            "InstanceRole": "CORE",
            "InstanceType": self.core_type,
            "AutoScalingPolicy": {
                "Constraints": {
                    "MinCapacity": (self.core_instance_count // 2),
                    "MaxCapacity": (self.core_instance_count * 3)
                },
                "Rules": [
                    {
                        "Name": "Default-scale-out",
                        "Description": "Replicates the default scale-out rule"
                                       "in the console for YARN memory.",
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
        return instances_group


class AwsEmrInstance:
    def __init__(self, subnet_id: str,
                 master_security_group: str, core_security_group: str,
                 service_access_security_group: str,
                 instance_groups: AwsEmrInstanceGroup):
        self.subnet_id = subnet_id
        self.master_sg = master_security_group
        self.core_sg = core_security_group
        self.service_access_sg = service_access_security_group
        self.instance_groups = instance_groups

    def get_instance(self):
        instances = {
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'InstanceGroups': self.instance_groups.get_instance_group(),
            'Ec2SubnetId': self.subnet_id,
            'EmrManagedMasterSecurityGroup': self.master_sg,
            'EmrManagedSlaveSecurityGroup': self.master_sg,
            'ServiceAccessSecurityGroup': self.service_access_sg
        }
        return instances


class AwsEmrCluster:
    def __init__(self, cluster_name: str, log_uri: str,
                 release: str, applications: list, instances: AwsEmrInstance,
                 multiple_steps: str, auto_scaling_role: str,
                 job_flow_role: str, service_role: str):
        self.cluster_name = cluster_name
        self.log_uri = log_uri
        self.release = release
        self.applications = applications
        self.instances = instances.get_instance()
        self.multiple_steps = multiple_steps
        self.auto_scaling_role = auto_scaling_role
        self.job_flow_role = job_flow_role
        self.service_role = service_role
