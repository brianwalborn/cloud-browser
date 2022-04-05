import cloud_browser.services.aws.ec2 as ec2
import cloud_browser.services.aws.ssm as ssm
import time
from cloud_browser.models.aws.autoscaling.instance import Instance
from cloud_browser.models.aws.ssm.command import Command
from cloud_browser.models.aws.ssm.command_invocation import CommandInvocation
from cloud_browser.tasks.base import BaseTask
from concurrent.futures import ThreadPoolExecutor
from itertools import groupby

class SendSsmCommand(BaseTask):
    def __init__(self) -> None:
        super().__init__()

        self.linux_command = None
        self.windows_command = None

    def __get_distinct_operating_systems(self, instances: list) -> list[str]:
        os_list = []
        operating_system_list = set({instance.operating_system for instance in instances})

        for os in operating_system_list: os_list.append(os.lower())

        return os_list

    def __group_instances_by_operating_system(self, instances_grouped_by_region: list[list]) -> list[list[Instance]]:
        output = []

        for group in instances_grouped_by_region:
            operating_system_list = self.__get_distinct_operating_systems(group)
            operating_system_groups = [[] for _ in range(len(operating_system_list))]

            for instance in group: operating_system_groups[operating_system_list.index(instance.operating_system.lower())].append(instance)

            output.append(operating_system_groups)
        
        return output

    def __group_instances_by_region(self, instances: list[Instance]) -> list[list[Instance]]:
        region_groups = [list(result) for key, result in groupby(instances, key = lambda x: x.region)]

        return region_groups

    def __initialize_commands(self, groups:list[list[list[Instance]]]) -> list[Command]:
        commands = []

        for region_group in groups:
            if len(region_group):
                for os_group in region_group:
                    instance_group = [os_group]
                    
                    if len(os_group) >= 50: instance_group = [os_group[n:n+50] for n in range(0, len(os_group), 50)] # the send_command call can only handle 50 instances at a time

                    for group in instance_group:
                        command = Command(group)
                        os = group[0].operating_system

                        if os.lower() == 'linux/unix': command.linux_command = self.linux_command
                        elif os.lower() == 'windows': command.windows_command = self.windows_command
                        else:
                            raise Exception(f'Unrecognized operating system: \'{os}\'.')

                        command.set_document_name()
                        command.set_parameter()
                        command.region = group[0].region

                        commands.append(command)

        return commands

    def __send_commands(self, commands: list[Command]) -> list[Command]:
        sent_commands = []

        for command in commands:
            client = ssm.SimpleSystemsManagerService(command.region)

            client.send_command(command)

            sent_commands.append(command)

        return sent_commands

    def get_command_results(self, sent_commands: list[Command]) -> list[CommandInvocation]:
        completed_invocations = []

        for command in sent_commands:
            client = ssm.SimpleSystemsManagerService(command.region)

            for instance_id in command.instance_ids:
                invocation = client.get_command_invocation(command.command_id, instance_id)

                while invocation.status == 'InProgress':
                    invocation = client.get_command_invocation(command.command_id, instance_id)

                    time.sleep(2)

                completed_invocations.append(invocation)

        return completed_invocations

    def get_instances(self) -> list[Instance]:
        def __get_instances(service: ec2.ElasticComputeCloudService, instances: list[Instance]):
            response = service.get_instances()

            for instance in response:
                if instance.state.lower() == 'running': instances.append(instance)

        try:
            instances: list[Instance] = []

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for region in self.regions():
                    service = ec2.ElasticComputeCloudService(region)
                    
                    executor.submit(__get_instances, service, instances)

            return sorted(instances, key = lambda x: x.name)
        except Exception as e:
            raise Exception(e)

    def send_commands(self, selected_instances) -> list[Command]:
        instances_grouped_by_region_and_os = self.__group_instances_by_operating_system(self.__group_instances_by_region(selected_instances))
        commands_to_send = self.__initialize_commands(instances_grouped_by_region_and_os)

        sent_commands = self.__send_commands(commands_to_send)

        time.sleep(5) # short timeout to allow commands to send

        return sent_commands
