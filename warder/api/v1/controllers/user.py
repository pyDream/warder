from oslo_config import cfg
from oslo_log import log as logging
import pecan
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1.controllers import base
from warder.api.v1.types import user as hw_types

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class UserController(base.BaseController):

    def __init__(self, user_id):
        super(UserController, self).__init__()
        self.user_id = user_id
        #self.handler = self.handler.load_balancer

    _custom_actions = {
        'detail': ['GET'],
    }

    @wsme_pecan.wsexpose(wtypes.text)
    def get_one(self):
        # TODO(blogan): decide what exactly should be here, if anything
        return "Hello World!"

    def detail(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class UsersController(base.BaseController):

    def get_all(self):
         pass

    @wsme_pecan.wsexpose(hw_types.UserResponse, body=hw_types.
                         UserPost, status_code=202)
    def post(self, user):
        print user

    @pecan.expose()
    def _lookup(self, user_id, *remainder):
        return UserController(user_id), remainder
