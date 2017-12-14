import logging

from oslo_config import cfg
from pecan import rest
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1 import controllers as v1_controller


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class RootController(rest.RestController):
    """The controller with which the pecan wsgi app should be created."""
    _versions = None

    def __init__(self):
        super(RootController, self).__init__()
        self._versions = []
        v1_enabled = CONF.api_settings.api_v1_enabled
        if v1_enabled:
            self.v1 = v1_controller.V1Controller()
            self._versions.append(
                {
                    'status': 'SUPPORTED',
                    'updated': '2014-12-11T00:00:00Z',
                    'id': 'v1'
                })
        if not (v1_enabled):
            LOG.warning("Both v1 and v2.0 API endpoints are disabled -- is "
                        "this intentional?")
        elif v1_enabled:
            LOG.warning("Both v1 and v2.0 API endpoints are enabled -- it is "
                        "a security risk to expose the v1 endpoint publicly,"
                        "so please make sure access to it is secured.")

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        return {'versions': self._versions}
