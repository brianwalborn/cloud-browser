from cloud_browser.models.aws.elb.instance_state import InstanceState
from cloud_browser.models.aws.elb.load_balancer import LoadBalancer
from cloud_browser.models.aws.elb.tag_description import TagDescription
from cloud_browser.services.base import BaseAwsService

class ElasticLoadBalancingService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('elb', region)

    def get_instance_health(self, load_balancer_name):
        try:
            instance_states: list[InstanceState] = []
            response = self.client.describe_instance_health(LoadBalancerName = load_balancer_name)
            
            if 'InstanceStates' in response:
                for instance_state in response['InstanceStates']:
                    instance_states.append(InstanceState(instance_state))

            return instance_states
        except Exception as e:
            print(f'\nException {type(e)}: Load balancer name {load_balancer_name}: {e}')

    def get_load_balancers(self) -> list[LoadBalancer]:
        # TODO: Refactor
        try:
            load_balancers: list[LoadBalancer] = []
            response = self.client.describe_load_balancers()
            return_list: list[LoadBalancer] = []

            for load_balancer in response['LoadBalancerDescriptions']:
                load_balancers.append(LoadBalancer(load_balancer))

            tag_descriptions = self.get_load_balancer_tag_descriptions([lb.name for lb in load_balancers])

            for load_balancer in load_balancers:    
                for tag_description in tag_descriptions:
                    if load_balancer.name == tag_description.load_balancer_name:
                        load_balancer.tags = tag_description.tags

            for load_balancer in load_balancers:
                if load_balancer.tags:
                    return_list.append(load_balancer)

            return sorted(return_list, key=lambda x: x.name)
        except Exception as e:
            print(f'\nException {type(e)}: {e}')

    def get_load_balancer_tag_descriptions(self, load_balancer_names) -> list[TagDescription]:
        try:
            if type(load_balancer_names) == str: load_balancer_names = [load_balancer_names]

            load_balancers_grouped_in_twenties = [load_balancer_names[n:n+20] for n in range(0, len(load_balancer_names), 20)] # the describe_tags call can only handle 20 load balancers at a time
            tag_descriptions = []
            
            for group in load_balancers_grouped_in_twenties:
                response = self.client.describe_tags(LoadBalancerNames = group)
                
                for tag_description in response['TagDescriptions']:
                    tag_description = TagDescription(tag_description)

                    for tag in self.tags:
                        if tag in tag_description.tags: tag_descriptions.append(tag_description)

            return tag_descriptions
        except Exception as e:
            print(f'\nException {type(e)}: {e}')
