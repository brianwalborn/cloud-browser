from cloud_browser.models.aws.base import BaseAwsResource

class SuspendedProcess(BaseAwsResource):
    def __init__(self, suspended_process_json):
        self.process_name = self._lookup(suspended_process_json, 'ProcessName')
        self.suspension_reason = self._lookup(suspended_process_json, 'SuspensionReason')
