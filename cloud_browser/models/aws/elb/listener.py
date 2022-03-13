from cloud_browser.models.aws.base import BaseAwsResource

class Listener(BaseAwsResource):
    def __init__(self, listener_json):
        self.instance_port = self._lookup(listener_json, 'InstancePort')
        self.instance_protocol = self._lookup(listener_json, 'InstanceProtocol')
        self.load_balancer_port = self._lookup(listener_json, 'LoadBalancerPort')
        self.protocol = self._lookup(listener_json, 'Protocol')
        self.ssl_certificate_id = self._lookup(listener_json, 'SSLCertificateId')
