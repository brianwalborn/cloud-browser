import cloud_browser.services.aws.elbv2 as elbv2
from cloud_browser.models.aws.elbv2.target_group import TargetGroup
from cloud_browser.models.aws.elbv2.target_health_description import TargetHealthDescription
from cloud_browser.tasks.base import BaseTask
from concurrent.futures import ThreadPoolExecutor

class TargetGroupHealth(BaseTask):
    def __init__(self):
        super().__init__()

    def get_target_group_health(self) -> dict[str, list[TargetHealthDescription]]:
        def __get_target_health(service: elbv2.ElasticLoadBalancingV2Service, target_group: TargetGroup, target_health: dict[str, list[TargetHealthDescription]]) -> None:
            response = service.get_target_health(target_group.arn)

            target_health[target_group.name] = response

        try:
            target_health: dict[str, list[TargetHealthDescription]] = {}

            for region in self.regions():
                service = elbv2.ElasticLoadBalancingV2Service(region)
                target_groups = service.get_target_groups()

                with ThreadPoolExecutor(max_workers = 20) as executor:
                    for target_group in target_groups:
                        executor.submit(__get_target_health, service, target_group, target_health)

            return dict(sorted(target_health.items()))
        except Exception as e:
            raise Exception(e)
