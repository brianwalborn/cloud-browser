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
            raise Exception(e)

    def get_auto_scaling_groups_by_tag(self) -> list[AutoScalingGroup]:
        try:
            def add_groups(auto_scaling_group, auto_scaling_groups) -> None:
                ignore = False
                auto_scaling_group_object = AutoScalingGroup(auto_scaling_group)

                for dict in self.tags_to_ignore:
                    if dict in auto_scaling_group_object.tags: ignore = True

                if not ignore:
                    auto_scaling_group_object.lifecycle_hooks = sorted(self.get_lifecycle_hooks(auto_scaling_group_object.auto_scaling_group_name), key = lambda x: x.lifecycle_hook_name)
                    
                    auto_scaling_groups.append(auto_scaling_group_object)
            
            auto_scaling_groups = []
            response = self.client.describe_auto_scaling_groups(Filters = self.filters)
            responses = []

            responses.append(response)
            
            while 'NextToken' in response:
                response = self.client.describe_auto_scaling_groups(Filters = self.filters, NextToken = response['NextToken'])
                
                responses.append(response)

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for response in responses:
                    for auto_scaling_group in response['AutoScalingGroups']:
                        executor.submit(add_groups, auto_scaling_group, auto_scaling_groups)

            return sorted(auto_scaling_groups, key = lambda x: x.auto_scaling_group_name)
        except Exception as e:
            raise Exception(e)

    def get_lifecycle_hooks(self, auto_scaling_group_name) -> list[LifecycleHook]:
        try:
            lifecycle_hooks = []
            response = self.client.describe_lifecycle_hooks(AutoScalingGroupName = auto_scaling_group_name)

            for lifecycle_hook in response['LifecycleHooks']: lifecycle_hooks.append(LifecycleHook(lifecycle_hook))

            return lifecycle_hooks
        except Exception as e:
            raise Exception(e)

    def resume_processes(self, auto_scaling_group_name, suspended_processes):
        try:
            response = self.client.resume_processes(AutoScalingGroupName = auto_scaling_group_name, ScalingProcesses = suspended_processes)

            return response
        except Exception as e:
            raise Exception(e)
