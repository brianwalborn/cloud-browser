import cloud_browser.globals as globals
import cloud_browser.services.aws.elb as elb
from concurrent.futures import ThreadPoolExecutor

class Check:
    def __init__(self):
        self.load_balancers = []

    def get_load_balancer_instance_health(self):
        def get_instance_health(load_balancer, service):
            load_balancer.instance_states = service.get_instance_health(load_balancer.name)

        for region in globals.regions:
            service = elb.ElasticLoadBalancingService(region)
            load_balancers = service.get_load_balancers()

            with ThreadPoolExecutor(max_workers = 20) as executor:
                for load_balancer in load_balancers:
                    executor.submit(get_instance_health, load_balancer, service)

            self.load_balancers += load_balancers

        return self.load_balancers
