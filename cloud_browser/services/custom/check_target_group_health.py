import cloud_browser.services.aws.elbv2 as elbv2
from cloud_browser.database.database import get_database
from cloud_browser.models.aws.elbv2.target_group import TargetGroup
from cloud_browser.models.aws.elbv2.target_health_description import TargetHealthDescription
from concurrent.futures import ThreadPoolExecutor

def check_target_group_health() -> dict[str, list[TargetHealthDescription]]:
    def get_target_health(service: elbv2.ElasticLoadBalancingV2Service, target_group: TargetGroup, target_health: dict[str, list[TargetHealthDescription]]) -> None:
        response = service.get_target_health(target_group.arn)

        target_health[target_group.name] = response

    try:
        database = get_database()
        regions = database.execute('SELECT * FROM settings_query_regions').fetchall()
        target_health: dict[str, list[TargetHealthDescription]] = {}

        for region in regions:
            service = elbv2.ElasticLoadBalancingV2Service(region['region'])
            target_groups = service.get_target_groups()

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for target_group in target_groups:
                    executor.submit(get_target_health, service, target_group, target_health)

        return dict(sorted(target_health.items()))
    except Exception as e:
        raise Exception(e)
