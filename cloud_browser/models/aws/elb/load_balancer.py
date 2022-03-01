from cloud_browser.models.aws.elb.health_check import HealthCheck
from cloud_browser.models.aws.elb.listener import Listener
from cloud_browser.models.base import BaseAwsResource

class LoadBalancer(BaseAwsResource):
    def __init__(self, describe_load_balancer_json):
        self.availability_zones = self._lookup(describe_load_balancer_json, 'AvailabilityZones')
        self.canonical_hosted_zone_name_id = self._lookup(describe_load_balancer_json, 'CanonicalHostedZoneNameID')
        self.dns_name = self._lookup(describe_load_balancer_json, 'DNSName')
        self.health_check = HealthCheck(self._lookup(describe_load_balancer_json, 'HealthCheck'))
        self.instance_states = None
        self.name = self._lookup(describe_load_balancer_json, 'LoadBalancerName')
        self.listeners = self.__get_listeners(describe_load_balancer_json)
        self.security_groups = self._lookup(describe_load_balancer_json, 'SecurityGroups')
        self.scheme = self._lookup(describe_load_balancer_json, 'Scheme')
        self.subnets = self._lookup(describe_load_balancer_json, 'Subnets')
        self.tags = None
        self.vpc_id = self._lookup(describe_load_balancer_json, 'VPCId')

    def __get_listeners(self, describe_load_balancer_json):
        listeners = []

        for listener in self._lookup(describe_load_balancer_json, 'ListenerDescriptions'):
            listeners.append(Listener(listener['Listener']))

        return listeners
        