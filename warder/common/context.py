from oslo_config import cfg
from oslo_context import context as common_context

from warder.db import api as db_api

CONF = cfg.CONF


class Context(common_context.RequestContext):

    _session = None

    def __init__(self, **kwargs):

        super(Context, self).__init__(**kwargs)


    @property
    def session(self):
        if self._session is None:
            self._session = db_api.get_session()
        return self._session
