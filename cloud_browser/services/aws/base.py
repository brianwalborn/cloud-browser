import boto3
import botocore.exceptions
from cloud_browser.database.database import get_database
from cloud_browser.models.aws.generic.tag import Tag

class BaseAwsService:
    __session: boto3.Session = None

    def __init__(self, aws_service, region) -> None:
        self.client = self.__get_client(aws_service, region)
        self.__test_connection()
        self.tags = self.__get_tags()
        self.filters = self.__generate_filters()
        self.tags_to_ignore = self.__get_tags_to_ignore()

    @staticmethod
    def __create_session() -> boto3.Session:
        try:
            profile = get_database().execute('SELECT * FROM settings_selected_aws_profile').fetchone()

            return boto3.Session(profile_name = profile['aws_profile'])
        except Exception as e:
            raise(e)

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
            if BaseAwsService.__session_null_or_updated() or BaseAwsService.__session_expired(): BaseAwsService.__session = BaseAwsService.__create_session()
            credentials = BaseAwsService.__session.get_credentials()

            return BaseAwsService.__session.client(
                aws_service, 
                region_name = region, 
                aws_access_key_id = credentials.access_key,
                aws_secret_access_key = credentials.secret_key,
                aws_session_token = credentials.token
            )
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

    @staticmethod
    def __session_expired() -> bool:
        try:
            BaseAwsService.__session.client('s3').list_buckets()

            return False
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken': return True
            raise Exception(f'{e.response["Error"]["Message"]} ({e.response["Error"]["Code"]})')
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def __session_null_or_updated() -> bool:
        try:
            if not BaseAwsService.__session: return True

            current_profile = BaseAwsService.__session.profile_name
            selected_profile = get_database().execute('SELECT * FROM settings_selected_aws_profile').fetchone()

            return not current_profile == selected_profile['aws_profile']
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def __test_connection() -> bool:
        try:
            BaseAwsService.__session.client('s3').list_buckets()
        except botocore.exceptions.ClientError as e:
            raise Exception(f'{e.response["Error"]["Message"]} ({e.response["Error"]["Code"]})')
        except Exception as e:
            raise Exception(e)
