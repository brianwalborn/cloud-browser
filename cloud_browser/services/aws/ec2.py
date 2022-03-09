from cloud_browser.models.aws.ec2.image import Image
from cloud_browser.models.aws.ec2.instance import Instance
from cloud_browser.services.base import BaseAwsService
from concurrent.futures import ThreadPoolExecutor

class ElasticComputeCloudService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('ec2', region)

    def describe_image(self, image_id: str):
        try:
            response = self.client.describe_images(ImageIds = [image_id])
            
            return Image(response)
        except Exception as e:
            raise Exception(e)

    def get_instances_by_tags(self) -> list[Instance]:
        try:
            def add_instance(instance, instances) -> None:
                ignore = False
                instance_object = Instance(instance)

                for tag in self.tags_to_ignore:
                    if tag in instance_object.tags: ignore = True

                if not ignore:
                    instance_object.image = self.describe_image(instance_object.image_id)
                    instances.append(instance_object)

            instances = []
            responses = []

            response = self.client.describe_instances(Filters = self.filters)

            responses.append(response)

            while 'NextToken' in response:
                response = self.client.describe_instances(Filters = self.filters, NextToken = response['NextToken'])

                responses.append(response)

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for response in responses:
                    for reservation in response['Reservations']:
                        for instance in reservation['Instances']:
                            executor.submit(add_instance, instance, instances)
    
            return instances
        except Exception as e:
            raise Exception(e)
