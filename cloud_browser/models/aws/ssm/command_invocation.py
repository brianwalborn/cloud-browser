from cloud_browser.models.aws.base import BaseAwsResource

class CommandInvocation(BaseAwsResource):
    def __init__(self, command_invocation_json):
        self.command_id = self._lookup(command_invocation_json, 'CommandId')
        self.comment = self._lookup(command_invocation_json, 'Comment')
        self.document_name = self._lookup(command_invocation_json, 'DocumentName')
        self.error = self._lookup(command_invocation_json, 'StandardErrorContent').replace("\n", "\n\t")
        self.execution_end_date_time = self._lookup(command_invocation_json, 'ExecutionEndDateTime')
        self.execution_start_date_time = self._lookup(command_invocation_json, 'ExecutionStartDateTime')
        self.instance_id = self._lookup(command_invocation_json, 'InstanceId')
        self.output = self._lookup(command_invocation_json, 'StandardOutputContent').replace("\n", "\n\t")
        self.status = self._lookup(command_invocation_json, 'Status')
        self.status_details = self._lookup(command_invocation_json, 'StatusDetails').replace("\n", "\n\t")
