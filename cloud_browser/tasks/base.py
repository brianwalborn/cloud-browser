from cloud_browser.database.database import get_database
from cloud_browser.models.aws.generic.tag import Tag

class BaseTask:
    def __init__(self) -> None:
        self.__database = get_database()

    def get_putty_session_name(self, region) -> str:
        try:
            response = self.__database.execute('SELECT session_name FROM settings_putty_session_names WHERE region = (?)', (region,)).fetchone()

            if not response: raise Exception('No PuTTy sessions specified. Please review settings.')

            return response['session_name']
        except Exception as e:
            raise(e)

    def regions(self) -> list[str]:
        try: 
            regions: list[str] = []
            response = self.__database.execute('SELECT * FROM settings_query_regions').fetchall()

            if not response: raise Exception('No regions specified. Please review settings.')

            for region in response: regions.append(region['region'])

            return regions
        except Exception as e:
            raise(e)

    def tags(self) -> list[Tag]:
        try:
            response = self.__database.execute('SELECT * FROM settings_query_tags').fetchall()
            tags: list[Tag] = []

            if not response: raise Exception('No tags specified. Please review settings.')

            for tag in response: tags.append(Tag(tag['tag_key'], tag['tag_value']))

            return tags
        except Exception as e:
            raise(e)