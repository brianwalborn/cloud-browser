from cloud_browser.models.base import BaseAwsResource

class Instance(BaseAwsResource):
    def __init__(self, auto_scaling_group_instance_json):
        self.availability_zone = self._lookup(auto_scaling_group_instance_json, 'AvailabilityZone')
        self.health_status = self._lookup(auto_scaling_group_instance_json, 'HealthStatus')
        self.instance_id = self._lookup(auto_scaling_group_instance_json, 'InstanceId')
        self.instance_type = self._lookup(auto_scaling_group_instance_json, 'InstanceType')
        self.launch_configuration_name = self._lookup(auto_scaling_group_instance_json, 'LaunchConfigurationName')
        self.lifecycle_state = self._lookup(auto_scaling_group_instance_json, 'LifecycleState')
