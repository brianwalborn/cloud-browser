import cloud_browser.globals as globals
import cloud_browser.services.aws.autoscaling as autoscaling
from concurrent.futures import ThreadPoolExecutor

class Helpers:
    def should_remove(self) -> bool:
        indicator = input('\nWould you like to remove the lifecycle hooks and suspended processes found above? (y/n) > ')

        if indicator.lower() in ['y', 'yes']: 
            return True
        else:
            return False

class Scanner:
    def __init__(self) -> None:
        self.all_auto_scaling_groups = []
        self.auto_scaling_groups_containing_leftovers = []
        self.helpers = Helpers()

    def __remove(self) -> None:
        for auto_scaling_group in self.auto_scaling_groups_containing_leftovers:
            for lifecycle_hook in auto_scaling_group.lifecycle_hooks_to_remove:
                print(f'Removing {lifecycle_hook.lifecycle_hook_name} from {auto_scaling_group.auto_scaling_group_name}')
                autoscaling.AutoScalingGroupService(auto_scaling_group.region).delete_lifecycle_hook(auto_scaling_group.auto_scaling_group_name, lifecycle_hook.lifecycle_hook_name)

            if auto_scaling_group.suspended_processes:
                processes = [p.process_name for p in auto_scaling_group.suspended_processes]
                print(f'Resuming {processes} on {auto_scaling_group.auto_scaling_group_name}')
                autoscaling.AutoScalingGroupService(auto_scaling_group.region).resume_processes(auto_scaling_group.auto_scaling_group_name, processes)

    def run(self) -> None:
        try:
            with ThreadPoolExecutor(max_workers = 20) as executor:
                def append_auto_scaling_groups(region, tag_key):
                    self.all_auto_scaling_groups += autoscaling.AutoScalingGroupService(region).get_auto_scaling_groups_by_tag(tag_key, globals.tags[tag_key])

                for region in globals.regions:
                    for tag_key in globals.tags:
                        executor.submit(append_auto_scaling_groups, region, tag_key)
        except Exception as e:
            print(f'Exception {type(e)}: {e}')
            exit()
