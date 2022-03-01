from cloud_browser.models.base import BaseAwsResource

class HealthCheck(BaseAwsResource):
    def __init__(self, health_check_json):
        self.healthy_threshold = self._lookup(health_check_json, 'HealthyThreshold')
        self.interval = self._lookup(health_check_json, 'Interval')
        self.target = self._lookup(health_check_json, 'Target')
        self.timeout = self._lookup(health_check_json, 'Timeout')
        self.unhealthy_threshold = self._lookup(health_check_json, 'UnhealthyThreshold')
