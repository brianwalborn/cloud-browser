import cloud_browser.services.aws.elb as elb
from cloud_browser.database.database import get_database
from cloud_browser.models.aws.elb.load_balancer import LoadBalancer
from concurrent.futures import ThreadPoolExecutor

class Check:
    def __init__(self):
        self.load_balancers = []

    def get_load_balancer_instance_health(self):
        try:
            database = get_database()
            regions = database.execute('SELECT * FROM settings_query_regions').fetchall()

            def set_instance_health(load_balancer: LoadBalancer, service: elb.ElasticLoadBalancingService):
                load_balancer.instance_states = service.get_instance_health(load_balancer.name)

            for region in regions:
                service = elb.ElasticLoadBalancingService(region['region'])
                load_balancers = service.get_load_balancers()

                with ThreadPoolExecutor(max_workers = 20) as executor:
                    for load_balancer in load_balancers:
                        executor.submit(set_instance_health, load_balancer, service)

                self.load_balancers += load_balancers

            return sorted(self.load_balancers, key=lambda x: x.name)
        except Exception as e:
            raise Exception(e)
