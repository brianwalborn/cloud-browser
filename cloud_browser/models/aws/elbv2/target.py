from cloud_browser.models.aws.base import BaseAwsResource

class Target(BaseAwsResource):
    def __init__(self, target_json):
        self.availability_zone: str = self._lookup(target_json, 'AvailabilityZone')
        self.id: str = self._lookup(target_json, 'Id')
        self.port: int = self._lookup(target_json, 'Port')
