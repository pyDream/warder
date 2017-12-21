from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1.controllers import base
from warder.api.v1.controllers import user


class V1Controller(base.BaseController):

    user = None

    def __init__(self):
        super(V1Controller, self).__init__()
        self.user = user.UserController()

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        # TODO(blogan): decide what exactly should be here, if anything
        return "v1"
