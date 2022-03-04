import cloud_browser.services.aws.autoscaling as autoscaling
from cloud_browser.models.aws.autoscaling.auto_scaling_group import AutoScalingGroup
from cloud_browser.database.database import get_database
from concurrent.futures import ThreadPoolExecutor

class Scanner:
    def __init__(self) -> None:
        self.all_auto_scaling_groups = []

    def get_auto_scaling_groups(self) -> list[AutoScalingGroup]:
        try:
            database = get_database()
            regions = database.execute('SELECT * FROM settings_query_regions').fetchall()

            def append_auto_scaling_groups(service: autoscaling.AutoScalingGroupService):
                self.all_auto_scaling_groups += service.get_auto_scaling_groups_by_tag()

            for region in regions:
                service = autoscaling.AutoScalingGroupService(region['region'])

                with ThreadPoolExecutor(max_workers = 20) as executor:
                    executor.submit(append_auto_scaling_groups, service)

            return self.all_auto_scaling_groups
        except Exception as e:
            print(f'Exception {type(e)}: {e}')
