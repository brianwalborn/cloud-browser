from cloud_browser.models.aws.elbv2.target import Target
from cloud_browser.models.aws.elbv2.target_health import TargetHealth
from cloud_browser.models.base import BaseAwsResource

class TargetHealthDescription(BaseAwsResource):
    def __init__(self, target_group_arn, target_health_description_json):
        self.health_check_port: int = self._lookup(target_health_description_json, 'HealthCheckPort')
        self.target: Target = Target(self._lookup(target_health_description_json, 'Target'))
        self.target_group_arn: str = target_group_arn
        self.target_health: TargetHealth = TargetHealth(self._lookup(target_health_description_json, 'TargetHealth'))
        