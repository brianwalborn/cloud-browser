import boto3
import botocore.exceptions
from cloud_browser.database.database import get_database
from cloud_browser.models.aws.generic.tag import Tag

class BaseAwsService:
    def __init__(self, aws_service, region) -> None:
        self.__test_connection()
        self.client = self.__get_client(aws_service, region)
        self.tags = self.__get_tags()
        self.filters = self.__generate_filters()
        self.tags_to_ignore = self.__get_tags_to_ignore()

    def __generate_filters(self) -> list[object]:
        try:
            filters: dict[str, list[str]] = {}
            ret = []
            tags = self.tags

            for tag in tags:
                if tag.key in filters: filters[tag.key].append(tag.value)
                else: filters.update({tag.key: [tag.value]})
                
            for filter in filters:    
                ret.append({ 'Name': f'tag:{filter}', 'Values': filters[filter] })

            return ret
        except Exception as e:
            raise Exception(e)

    def __get_client(self, aws_service, region) -> boto3.Session.client:
        try:
            return boto3.client(aws_service, region_name = region)
        except Exception as e:
            raise Exception(e)

    def __get_tags(self) -> list[Tag]:
        try:
            database = get_database()
            tags = database.execute('SELECT * FROM settings_query_tags').fetchall()
            ret = []

            for tag in tags:
                ret.append(Tag(tag['tag_key'], tag['tag_value']))

            return ret
        except Exception as e:
            raise Exception(e)

    def __get_tags_to_ignore(self) -> list[Tag]:
        try:
            database = get_database()
            ignore_tags = database.execute('SELECT * FROM settings_exclude_tags').fetchall()
            ret = []

            for tag in ignore_tags:
                ret.append(Tag(tag['tag_key'], tag['tag_value']))

            return ret
        except Exception as e:
            raise Exception(e)

    def __test_connection(self):
        try:
            boto3.client('s3').list_buckets()
        except botocore.exceptions.ClientError as e:
            raise Exception(f'{e.response["Error"]["Message"]} ({e.response["Error"]["Code"]})')
        except Exception as e:
            raise Exception(e)
