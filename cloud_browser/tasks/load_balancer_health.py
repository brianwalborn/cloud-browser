import cloud_browser.services.aws.elb as elb
from cloud_browser.models.aws.elb.load_balancer import LoadBalancer
from cloud_browser.tasks.base import BaseTask
from concurrent.futures import ThreadPoolExecutor

class LoadBalancerHealth(BaseTask):
    def __init__(self):
        super().__init__()

    def get_load_balancer_health(self) -> list[LoadBalancer]:
        def __set_instance_health(service: elb.ElasticLoadBalancingService, load_balancer: LoadBalancer, load_balancers: list[LoadBalancer]):
            load_balancer.instance_states = service.get_instance_health(load_balancer.name)

            load_balancers.append(load_balancer)
        
        try:
            load_balancers: list[LoadBalancer] = []

            for region in self.regions():
                service = elb.ElasticLoadBalancingService(region)
                response = service.get_load_balancers()

                with ThreadPoolExecutor(max_workers = 20) as executor:
                    for load_balancer in response:
                        executor.submit(__set_instance_health, service, load_balancer, load_balancers)

            return sorted(load_balancers, key = lambda x: x.name)
        except Exception as e:
            raise Exception(e)
