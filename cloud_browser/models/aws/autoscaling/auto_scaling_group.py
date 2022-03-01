import cloud_browser.services.aws.autoscaling as autoscaling
from cloud_browser.models.aws.autoscaling.instance import Instance
from cloud_browser.models.aws.autoscaling.suspended_process import SuspendedProcess
from cloud_browser.models.base import BaseAwsResource

class AutoScalingGroup(BaseAwsResource):
    def __init__(self, auto_scaling_group_json) -> None:
        self.auto_scaling_group_arn = self._lookup(auto_scaling_group_json, 'AutoScalingGroupARN')
        self.auto_scaling_group_name = self._lookup(auto_scaling_group_json, 'AutoScalingGroupName')
        self.availability_zones = self._lookup(auto_scaling_group_json, 'AvailabilityZones')
        self.region = self.availability_zones[0][:-1]
        self.desired_capacity = self._lookup(auto_scaling_group_json, 'DesiredCapacity')
        self.health_check_grace_period = self._lookup(auto_scaling_group_json, 'HealthCheckGracePeriod')
        self.health_check_type = self._lookup(auto_scaling_group_json, 'HealthCheckType')
        self.instances = self.__get_auto_scaling_group_instances(auto_scaling_group_json)
        self.launch_configuration_name = self._lookup(auto_scaling_group_json, 'LaunchConfigurationName')
        self.lifecycle_hooks = autoscaling.AutoScalingGroupService(self.region).get_lifecycle_hooks(self.auto_scaling_group_name)
        self.load_balancers = self._lookup(auto_scaling_group_json, 'LoadBalancerNames')
        self.max_size = self._lookup(auto_scaling_group_json, 'MaxSize')
        self.min_size = self._lookup(auto_scaling_group_json, 'MinSize')
        self.suspended_processes = self.__get_suspended_processes(auto_scaling_group_json)
        self.tags = self._get_tags(self._lookup(auto_scaling_group_json, 'Tags'))
        self.target_group_arns = self._lookup(auto_scaling_group_json, 'TargetGroupARNs')

    def __get_auto_scaling_group_instances(self, auto_scaling_group_json):
        instances = []

        for instance_json in self._lookup(auto_scaling_group_json, 'Instances'): instances.append(Instance(instance_json))

        return instances

    def __get_suspended_processes(self, auto_scaling_group_json):
        suspended_processes = []

        for suspended_process in self._lookup(auto_scaling_group_json, 'SuspendedProcesses'): suspended_processes.append(SuspendedProcess(suspended_process))

        return suspended_processes
