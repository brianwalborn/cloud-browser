import cloud_browser.services.aws.autoscaling as autoscaling
from cloud_browser.models.aws.autoscaling.auto_scaling_group import AutoScalingGroup
from cloud_browser.tasks.base import BaseTask
from concurrent.futures import ThreadPoolExecutor

class GetAutoScalingGroups(BaseTask):
    def __init__(self) -> None:
        super().__init__()

    def get_auto_scaling_groups(self) -> list[AutoScalingGroup]:
        def __append_auto_scaling_groups(service: autoscaling.AutoScalingGroupService, auto_scaling_groups: list[AutoScalingGroup]):
            try: auto_scaling_groups.extend(service.get_auto_scaling_groups())
            except Exception as e: raise Exception(e)
        
        try:
            auto_scaling_groups: list[AutoScalingGroup] = []

            for region in self.regions():
                service = autoscaling.AutoScalingGroupService(region)

                with ThreadPoolExecutor(max_workers = 20) as executor:
                    executor.submit(__append_auto_scaling_groups, service, auto_scaling_groups)

            return auto_scaling_groups
        except Exception as e:
            raise Exception(e)
