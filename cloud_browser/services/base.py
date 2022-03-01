import boto3
import cloud_browser.globals as globals
from cloud_browser.models.aws.generic.tag import Tag

class BaseAwsService:
    def __init__(self, aws_service, region) -> None:
        self.client = self.__get_client(aws_service, region)
        self.filters = self.__generate_filters()
        self.tags = self.__get_tags()
        self.tags_to_ignore = self.__get_tags_to_ignore()

    def __generate_filters(self) -> list[object]:
        filters = []

        for tag in globals.tags:
            filters.append({ 'Name': f'tag:{tag}', 'Values': globals.tags[tag] })

        return filters

    def __get_client(self, aws_service, region) -> boto3.Session.client:
        return boto3.client(aws_service, region_name = region)

    def __get_tags(self):
        tags = []

        for tag_key in globals.tags:
            for tag_value in globals.tags[tag_key]:
                tags.append(Tag(tag_key, tag_value))

        return tags

    def __get_tags_to_ignore(self):
        ignore_tags = []

        for tag_key in globals.tags_to_ignore:
            for tag_value in globals.tags_to_ignore[tag_key]:
                ignore_tags.append(Tag(tag_key, tag_value))

        return ignore_tags
