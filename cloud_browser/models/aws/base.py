from cloud_browser.models.aws.generic.tag import Tag

class BaseAwsResource:
    def _get_tags(self, tag_json) -> list[Tag]:
        tags = []

        for tag in tag_json: tags.append(Tag(tag['Key'], tag['Value']))

        return tags

    def _lookup(self, json, property_name):
        if property_name in json: return json[property_name]
        else: return None
