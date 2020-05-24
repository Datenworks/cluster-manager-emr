from lib.aws.emr.cluster import AwsEmrCluster
import boto3


class AwsEmrClient:
    def __init__(self):
        self.emr_client = boto3.client('emr')

    def execute_step(self, cluster: AwsEmrCluster, steps: list):
        print(cluster)
        if cluster.multiple_steps == "ENABLED":
            clusters_available = \
                self.__filter_clusters_by_name(
                    cluster_list=self.__list_available_clusters(),
                    cluster_name=cluster.cluster_name)

            if len(clusters_available) >= 1:
                response = \
                    self.__add_job_flow_step(clusters_available[0]['Id'],
                                             steps)
                response.update({"JobFlowId": clusters_available[0]['Id']})
            else:
                response = self.__run_job_flow(cluster=cluster, steps=steps)
        else:
            response = self.__run_job_flow(cluster=cluster, steps=steps)

        response.update({'multiple_step': cluster.multiple_steps})
        return response

    def __run_job_flow(self, cluster: AwsEmrCluster, steps: list):
        response = self.emr_client.run_job_flow(
            Name=cluster.cluster_name,
            LogUri=cluster.log_uri,
            ReleaseLabel=cluster.release,
            Applications=cluster.applications,
            Instances=cluster.instances,
            SecurityConfiguration="emr-data-encryption",
            AutoScalingRole=cluster.auto_scaling_role,
            VisibleToAllUsers=True,
            Steps=[steps],
            JobFlowRole=cluster.job_flow_role,
            ServiceRole=cluster.service_role
        )
        return response

    def __add_job_flow_step(self, cluster_id, steps):
        return self.emr_client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=[steps]
        )

    def get_step_by_name(self, cluster_id, step_name):
        steps = self.list_steps(cluster_id=cluster_id)
        return [step for step in steps.get("Steps")
                if step['Name'] == step_name][0]

    def describe_step(self, cluster_id, step_id):
        return self.emr_client\
            .describe_step(ClusterId=cluster_id, step_id=step_id)

    def list_steps_running(self, cluster_id):
        states = ['RUNNING', 'PENDING']
        return self.list_steps(cluster_id=cluster_id, states=states)

    def list_steps(self, cluster_id, states=None):
        if states is None:
            return self.emr_client.list_steps(ClusterId=cluster_id)
        return self.emr_client.\
            list_steps(ClusterId=cluster_id, StepStates=states)

    def __list_available_clusters(self):
        available_states = ['STARTING', 'BOOTSTRAPPING', 'RUNNING']
        list_clusters_on = self.emr_client \
            .list_clusters(ClusterStates=available_states) \
            .get("Clusters")
        return list_clusters_on

    def __filter_clusters_by_name(self, cluster_list: [], cluster_name: str):
        return [cluster for cluster in cluster_list
                if cluster['Name'] == cluster_name]

    def destroy_cluster(self, cluster_id):
        self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
