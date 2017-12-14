from oslo_config import cfg
from oslo_log import log as logging
import pecan
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1.controllers import base
from warder.api.v1.types import helloworld as hw_types

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class HelloWorldController(base.BaseController):

    def __init__(self):
        super(HelloWorldController, self).__init__()
        #self.handler = self.handler.load_balancer

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        # TODO(blogan): decide what exactly should be here, if anything
        return "Hello World!"

    # @wsme_pecan.wsexpose(hw_types.HelloWorldResponse, wtypes.text)
    # def get(self, id):
    #     """Hello World!"""
    #     context = pecan.request.context.get('warder_context')
    #     hello_world = self._get_db_lb(context.session, id)
    #     return self._convert_db_to_type(hello_world,
    #                                     hw_types.HelloWorldResponse)
