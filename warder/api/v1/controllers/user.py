import uuid

from oslo_config import cfg
from oslo_log import log as logging
import pecan
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from warder.api.v1.controllers import base
from warder.api.v1.types import user as hw_types
from warder.common import exceptions

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class UserController(base.BaseController):

    def __init__(self, user_id):
        super(UserController, self).__init__()
        self.user_id = user_id
        # self.handler = self.handler.load_balancer

#    _custom_actions = {
#        'detail': ['GET'],
#    }

    @wsme_pecan.wsexpose(hw_types.UserDetailRespone, wtypes.text)
    def get(self):
        phones = []
        context = pecan.request.context.get('warder_context')
        user_inf = self.repositories.user.get_user(context.session, self.user_id)
        user_dict = user_inf.to_dict()
        for phone in user_inf.telephone:
            phones.append(phone.telnumber)
        user_dict["telephone"] = phones
        return hw_types.UserDetailRespone(**user_dict)

    def detail(self):
        pass

    @wsme_pecan.wsexpose(hw_types.UserResponse, wtypes.text,
                         status_code=200,body=hw_types.UserPost)
    def put(self, user_inf):
        user_dict = user_inf.to_dict()
        context = pecan.request.context.get('warder_context')
        self.repositories.user.update_user(context.session, self.user_id, **user_dict)

    @wsme_pecan.wsexpose(None, wtypes.text, wtypes.text, status_code=204)
    def delete(self):
        context  = pecan.request.context.get('warder_context')
        try:
            LOG.info('Dele te user of %s', self.user_id)
            self.repositories.user.delete(context.session, user_id=self.user_id)
        except Exception:
            LOG.exception('Delete User %(user_id)s fail',{'user_id':self.user_id})
            raise exceptions.DeleteError(resource="User", id=self.user_id)

class UsersController(base.BaseController):

    @wsme_pecan.wsexpose(hw_types.UserListResponse, status_code=200)
    def get_all(self):
        context = pecan.request.context.get('warder_context')
        users_inf, links = self.repositories.user.get_all(context.session)
        result = self._convert_db_to_type(users_inf,
                                          [hw_types.UserResponse])
        return hw_types.UserListResponse(users=result)

    @wsme_pecan.wsexpose(hw_types.UserResponse, body=hw_types.
                         UserRootPost, status_code=201)
    def post(self, user_inf):
        user = user_inf.user
        user_dict = user.to_dict()
        context = pecan.request.context.get('warder_context')
        user_dict["user_id"] = str(uuid.uuid4())

        add_user_rel = self.repositories.user.add_user(
            context.session, user_dict)
        return self._convert_db_to_type(add_user_rel, [hw_types.UserResponse])

    @pecan.expose()
    def _lookup(self, user_id, *remainder):
        return UserController(user_id), remainder
