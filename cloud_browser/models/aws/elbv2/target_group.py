from cloud_browser.models.aws.base import BaseAwsResource
from cloud_browser.models.aws.generic.tag import Tag

class TargetGroup(BaseAwsResource):
    def __init__(self, target_group_json) -> None:
        self.arn: str = self._lookup(target_group_json, 'TargetGroupArn')
        self.health_check_enabled: bool = self._lookup(target_group_json, 'HealthCheckEnabled')
        self.health_check_interval_seconds: int = self._lookup(target_group_json, 'HealthCheckIntervalSeconds')
        self.health_check_path: str = self._lookup(target_group_json, 'HealthCheckPath')
        self.health_check_port: int = self._lookup(target_group_json, 'HealthCheckPort')
        self.health_check_protocol: str = self._lookup(target_group_json, 'HealthCheckProtocol')
        self.health_check_timeout_seconds: int = self._lookup(target_group_json, 'HealthCheckTimeoutSeconds')
        self.healthy_threshold_count: int = self._lookup(target_group_json, 'HealthyThresholdCount')
        self.ip_address_type: str = self._lookup(target_group_json, 'IpAddressType')
        self.load_balancer_arns: list[str] = self._lookup(target_group_json, 'LoadBalancerArns')
        self.name: str = self._lookup(target_group_json, 'TargetGroupName')
        self.port: int = self._lookup(target_group_json, 'Port')
        self.protocol: str = self._lookup(target_group_json, 'Protocol')
        self.protocol_version: str = self._lookup(target_group_json, 'ProtocolVersion')
        self.tags: list[Tag] = None
        self.target_type: str = self._lookup(target_group_json, 'TargetType')
        self.unhealthy_threshold_count: int = self._lookup(target_group_json, 'UnhealthyThresholdCount')
        self.vpc_id: str = self._lookup(target_group_json, 'VpcId')
