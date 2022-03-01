from cloud_browser.models.aws.autoscaling.auto_scaling_group import AutoScalingGroup
from cloud_browser.models.aws.autoscaling.lifecycle_hook import LifecycleHook
from cloud_browser.services.base import BaseAwsService
from concurrent.futures import ThreadPoolExecutor

class AutoScalingGroupService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('autoscaling', region)

    def delete_lifecycle_hook(self, auto_scaling_group_name, lifecycle_hook_name):
        try:
            response = self.client.delete_lifecycle_hook(AutoScalingGroupName = auto_scaling_group_name, LifecycleHookName = lifecycle_hook_name)
            
            return response
        except Exception as e:
            print(f'\nException {type(e)}: {e}')

    def get_auto_scaling_groups_by_tag(self, tag_key: str, tag_values: list[str]) -> list[AutoScalingGroup]:
        try:
            def add_groups(auto_scaling_group, auto_scaling_groups) -> None:
                ignore = False
                auto_scaling_group_object = AutoScalingGroup(auto_scaling_group)

                for dict in self.tags_to_ignore:
                    if dict in auto_scaling_group_object.tags: ignore = True

                if not ignore: auto_scaling_groups.append(auto_scaling_group_object)
            
            auto_scaling_groups = []
            responses = []
            tag_values_grouped_in_fives = [tag_values[n:n+5] for n in range(0, len(tag_values), 5)] # the describe_auto_scaling_groups call can only handle five tags at a time

            for group in tag_values_grouped_in_fives:
                response = self.client.describe_auto_scaling_groups(Filters = [{'Name': f'tag:{tag_key}', 'Values': group}])

                responses.append(response)
                
                while 'NextToken' in response:
                    response = self.client.describe_auto_scaling_groups(Filters = [{'Name': f'tag:{tag_key}', 'Values': group}], NextToken = response['NextToken'])
                    
                    responses.append(response)

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for response in responses:
                    for auto_scaling_group in response['AutoScalingGroups']:
                        executor.submit(add_groups, auto_scaling_group, auto_scaling_groups)

            return sorted(auto_scaling_groups, key=lambda x: x.auto_scaling_group_name)
        except Exception as e:
            print(f'\nException {type(e)}: {e}')

    def get_lifecycle_hooks(self, auto_scaling_group_name) -> list[LifecycleHook]:
        try:
            lifecycle_hooks = []
            response = self.client.describe_lifecycle_hooks(AutoScalingGroupName = auto_scaling_group_name)

            for lifecycle_hook in response['LifecycleHooks']: lifecycle_hooks.append(LifecycleHook(lifecycle_hook))

            return lifecycle_hooks
        except Exception as e:
            print(f'\nException {type(e)}: {e}')

    def resume_processes(self, auto_scaling_group_name, suspended_processes):
        try:
            response = self.client.resume_processes(AutoScalingGroupName = auto_scaling_group_name, ScalingProcesses = suspended_processes)

            return response
        except Exception as e:
            print(f'\nException {type(e)}: {e}')
