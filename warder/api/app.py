
from oslo_config import cfg
from oslo_log import log as logging
from oslo_middleware import cors
from oslo_middleware import request_id
import pecan

from octavia.api import config as app_config
from octavia.common import constants
from octavia.common import keystone
from octavia.common import service as octavia_service

LOG = logging.getLogger(__name__)


def get_pecan_config():
    """Returns the pecan config."""
    filename = app_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(pecan_config=None, debug=False, argv=None):
    """Creates and returns a pecan wsgi app."""
    octavia_service.prepare_service(argv)
    cfg.CONF.log_opt_values(LOG, logging.DEBUG)

    if not pecan_config:
        pecan_config = get_pecan_config()
    pecan.configuration.set_config(dict(pecan_config), overwrite=True)

    return pecan.make_app(
        pecan_config.app.root,
        wrap_app=_wrap_app,
        debug=debug,
        hooks=pecan_config.app.hooks,
        wsme=pecan_config.wsme
    )


def _wrap_app(app):
    """Wraps wsgi app with additional middlewares."""
    app = request_id.RequestId(app)
    if cfg.CONF.api_settings.auth_strategy == constants.KEYSTONE:
        app = keystone.SkippingAuthProtocol(app, {})

    # This should be the last middleware in the list (which results in
    # it being the first in the middleware chain). This is to ensure
    # that any errors thrown by other middleware, such as an auth
    # middleware - are annotated with CORS headers, and thus accessible
    # by the browser.
    app = cors.CORS(app, cfg.CONF)
    cors.set_defaults(
        allow_headers=['X-Auth-Token', 'X-Openstack-Request-Id'],
        allow_methods=['GET', 'PUT', 'POST', 'DELETE'],
        expose_headers=['X-Auth-Token', 'X-Openstack-Request-Id']
    )

    return app
