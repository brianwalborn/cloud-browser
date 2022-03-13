from cloud_browser.models.aws.base import BaseAwsResource

class TargetHealth(BaseAwsResource):
    def __init__(self, target_health_json):
        self.description: str = self._lookup(target_health_json, 'Description')
        self.reason: str = self._lookup(target_health_json, 'Reason')
        self.state: str = self._lookup(target_health_json, 'State')
        