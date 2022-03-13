from cloud_browser.models.aws.base import BaseAwsResource
from cloud_browser.models.aws.generic.tag import Tag

class TagDescription(BaseAwsResource):
    def __init__(self, tag_description_json):
        self.load_balancer_name = self._lookup(tag_description_json, 'LoadBalancerName')
        self.tags = self.__get_tags(tag_description_json)

    def __get_tags(self, tag_description_json):
        tags = []

        for tag in tag_description_json['Tags']:
            tags.append(Tag(tag['Key'], tag['Value']))

        return tags
