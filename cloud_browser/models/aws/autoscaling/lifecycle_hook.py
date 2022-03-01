from cloud_browser.models.base import BaseAwsResource

class LifecycleHook(BaseAwsResource):
    def __init__(self, lifecycle_hook_json):
        self.auto_scaling_group_name = self._lookup(lifecycle_hook_json, 'AutoScalingGroupName')
        self.lifecycle_hook_name = self._lookup(lifecycle_hook_json, 'LifecycleHookName')
