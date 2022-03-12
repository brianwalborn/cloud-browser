from cloud_browser.models.aws.elbv2.tag_description import TagDescription
from cloud_browser.models.aws.elbv2.target_group import TargetGroup
from cloud_browser.models.aws.elbv2.target_health_description import TargetHealthDescription
from cloud_browser.services.base import BaseAwsService
from concurrent.futures import ThreadPoolExecutor

class ElasticLoadBalancingV2Service(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('elbv2', region)

    def __get_tag_descriptions(self, target_groups: list[TargetGroup]) -> list[TagDescription]:
        def call(group, tag_descriptions) -> None:
            response = self.client.describe_tags(ResourceArns = group)
                    
            for tag_description in response['TagDescriptions']:
                tag_description = TagDescription(tag_description)

                for tag in tag_description.tags:
                    if tag in self.tags and tag not in self.tags_to_ignore: tag_descriptions.append(tag_description)

        try:
            arns = [target_group.arn for target_group in target_groups]
            arn_groups = [arns[n:n+20] for n in range(0, len(arns), 20)] # the describe_tags call can only handle 20 arns at a time
            tag_descriptions: list[TagDescription] = []
            
            with ThreadPoolExecutor(max_workers = 20) as executor:
                for group in arn_groups: executor.submit(call, group, tag_descriptions)
                    
            return tag_descriptions
        except Exception as e:
            raise Exception(e)

    def get_target_groups(self) -> list[TargetGroup]:
        try:
            response: dict = self.client.describe_target_groups()
            responses: list[dict] = []
            target_groups: list[TargetGroup] = []

            responses.append(response)

            while 'NextMarker' in response:
                response = self.client.describe_target_groups(Marker = response['NextMarker'])

                responses.append(response)

            for response in responses:
                for target_group in response['TargetGroups']:
                    target_groups.append(TargetGroup(target_group))

            tag_descriptions = self.__get_tag_descriptions(target_groups)

            for target_group in target_groups:
                index = -1

                try: index = [ tag_description.resource_arn for tag_description in tag_descriptions ].index(target_group.arn)
                except ValueError: pass # a value error exception indicates the value isn't in the list, that's ok in this case

                if not index == -1: target_group.tags = tag_descriptions[index].tags

            return sorted([target_group for target_group in target_groups if target_group.tags is not None], key = lambda x: x.name)
        except Exception as e:
            raise(e)

    def get_target_health(self, target_group_arn: str) -> list[TargetHealthDescription]:
        target_health_descriptions: list[TargetHealthDescription] = []

        try:
            response = self.client.describe_target_health(TargetGroupArn = target_group_arn)

            for description in response['TargetHealthDescriptions']:
                target_health_descriptions.append(TargetHealthDescription(target_group_arn, description))

            return target_health_descriptions
        except Exception as e:
            raise(e)
