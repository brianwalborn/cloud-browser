from cloud_browser.models.aws.autoscaling.instance import Instance

class Command:
    def __init__(self, instances: list[Instance] = None) -> None:
        self.command_id = None
        self.document_name = None
        self.instance_ids = self.__get_instance_ids(instances) if instances else None
        self.linux_command = None
        self.parameters = None
        self.region = None
        self.windows_command = None

    def __get_document_name(self) -> None:
        if not self.windows_command and self.linux_command: return 'AWS-RunShellScript'
        elif not self.linux_command and self.windows_command: return 'AWS-RunPowerShellScript'
        else: raise Exception('Could not determine a document name from the commands provided')

    def __get_instance_ids(self, instances) -> list[str]:
        instance_ids = []
        instance_id_list = {instance.instance_id for instance in instances}

        for id in instance_id_list:
            instance_ids.append(id)

        return instance_ids

    def set_document_name(self) -> None:
        self.document_name = self.__get_document_name()

    def set_instance_ids(self, instances) -> None:
        self.instance_ids = self.__get_instance_ids(instances)

    def set_parameter(self) -> None:
        if not self.document_name:
            raise Exception('A document name needs to be set on the command before setting the parameter')

        if self.document_name == 'AWS-RunShellScript': self.parameters = { 'commands': [ self.linux_command ] }
        elif self.document_name == 'AWS-RunPowerShellScript': self.parameters = { 'commands': [ self.windows_command ] }
        else:
            raise Exception(f'Unrecognized document name ({self.document_name})')
