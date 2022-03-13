from cloud_browser.models.aws.elb.instance_state import InstanceState
from cloud_browser.models.aws.elb.load_balancer import LoadBalancer
from cloud_browser.models.aws.elb.tag_description import TagDescription
from cloud_browser.services.aws.base import BaseAwsService
from concurrent.futures import ThreadPoolExecutor

class ElasticLoadBalancingService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('elb', region)

    def __get_tag_descriptions(self, load_balancers: list[LoadBalancer]) -> list[TagDescription]:
        def __call(group: list[str], tag_descriptions: list[TagDescription]) -> None:
            response = self.client.describe_tags(LoadBalancerNames = group)
                    
            for tag_description in response['TagDescriptions']:
                tag_description = TagDescription(tag_description)

                for tag in tag_description.tags:
                    if tag in self.tags and tag not in self.tags_to_ignore: tag_descriptions.append(tag_description)

        try:
            names = [load_balancer.name for load_balancer in load_balancers]
            names_grouped_in_twenties = [names[n:n+20] for n in range(0, len(names), 20)] # the describe_tags call can only handle 20 load balancers at a time
            tag_descriptions: list[TagDescription] = []
            
            with ThreadPoolExecutor(max_workers = 20) as executor:
                for group in names_grouped_in_twenties: executor.submit(__call, group, tag_descriptions)

            return tag_descriptions
        except Exception as e:
            raise Exception(e)

    def get_instance_health(self, load_balancer_name):
        try:
            instance_states: list[InstanceState] = []
            response = self.client.describe_instance_health(LoadBalancerName = load_balancer_name)
            
            if 'InstanceStates' in response:
                for instance_state in response['InstanceStates']:
                    instance_states.append(InstanceState(instance_state))

            return instance_states
        except Exception as e:
            raise Exception(e)

    def get_load_balancers(self) -> list[LoadBalancer]:
        def __append_load_balancer(load_balancer_json, load_balancers: list[LoadBalancer]) -> None: load_balancers.append(LoadBalancer(load_balancer_json))

        try:
            load_balancers: list[LoadBalancer] = []
            response: dict = self.client.describe_load_balancers()

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for load_balancer in response['LoadBalancerDescriptions']:
                    executor.submit(__append_load_balancer, load_balancer, load_balancers)

            tag_descriptions = self.__get_tag_descriptions(load_balancers)

            for load_balancer in load_balancers:
                index = -1

                try: index = [ tag_description.load_balancer_name for tag_description in tag_descriptions ].index(load_balancer.name)
                except ValueError: pass # a value error exception indicates the value isn't in the list, that's ok in this case

                if not index == -1: load_balancer.tags = tag_descriptions[index].tags

            return sorted([load_balancer for load_balancer in load_balancers if load_balancer.tags is not None], key = lambda x: x.name)
        except Exception as e:
            raise Exception(e)
