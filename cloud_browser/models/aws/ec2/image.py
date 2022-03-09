from cloud_browser.models.base import BaseAwsResource

class Image(BaseAwsResource):
    def __init__(self, describe_image_json):
        self.platform = self._lookup(describe_image_json['Images'][0], 'PlatformDetails')
        self.name = self._lookup(describe_image_json['Images'][0], 'Name')
