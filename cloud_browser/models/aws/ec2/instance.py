from cloud_browser.models.aws.base import BaseAwsResource

class Instance(BaseAwsResource):
    def __init__(self, describe_instance_json):
        self.availability_zone = self._lookup(describe_instance_json['Placement'], 'AvailabilityZone')
        self.image = None
        self.image_id = self._lookup(describe_instance_json, 'ImageId')
        self.instance_id = self._lookup(describe_instance_json, 'InstanceId')
        self.operating_system = self._lookup(describe_instance_json, 'PlatformDetails')
        self.private_ip_address = self._lookup(describe_instance_json, 'PrivateIpAddress')
        self.region = self.availability_zone[:-1]
        self.state = self._lookup(describe_instance_json['State'], 'Name')
        self.tags = self._get_tags(self._lookup(describe_instance_json, 'Tags'))
        self.name = [tag for tag in self.tags if tag.key == "Name"][0].value
