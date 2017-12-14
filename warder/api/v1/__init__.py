from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1.controllers import base


class V1Controller(base.BaseController):

    loadbalancers = None
    quotas = None

    def __init__(self):
        super(V1Controller, self).__init__()
        self.loadbalancers = load_balancer.LoadBalancersController()
        self.quotas = quotas.QuotasController()

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        # TODO(blogan): decide what exactly should be here, if anything
        return "v1"
