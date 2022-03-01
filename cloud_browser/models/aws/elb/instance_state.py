from cloud_browser.models.base import BaseAwsResource

class InstanceState(BaseAwsResource):
    def __init__(self, instance_state_json):
        self.description = self._lookup(instance_state_json, 'Description')
        self.instance_id = self._lookup(instance_state_json, 'InstanceId')
        self.reason_code = self._lookup(instance_state_json, 'ReasonCode')
        self.state = self._lookup(instance_state_json, 'State')
