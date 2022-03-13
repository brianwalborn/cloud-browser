from cloud_browser.models.aws.ssm.command_invocation import CommandInvocation
from cloud_browser.services.aws.base import BaseAwsService

class SimpleSystemsManagerService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('ssm', region)

    def get_command_invocation(self, command_id, instance_id):
        try:
            response = self.client.get_command_invocation(CommandId = command_id, InstanceId = instance_id)

            return CommandInvocation(response)
        except Exception as e:
            raise Exception(f'Command ID {command_id}: {e}')

    def send_command(self, command):
        try:
            response = self.client.send_command(InstanceIds = command.instance_ids, DocumentName = command.document_name, Parameters = command.parameters)

            command.command_id = response['Command']['CommandId']

            return command
        except Exception as e:
            raise Exception(e)
