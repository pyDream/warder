from oslo_config import cfg
from oslo_log import log as logging
from oslo_middleware import request_id
import pecan

from warder.api import config as app_config
from warder import service as warder_service

LOG = logging.getLogger(__name__)


def get_pecan_config():
    """Returns the pecan config."""
    filename = app_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(pecan_config=None, debug=False, argv=None):
    """Creates and returns a pecan wsgi app."""
    warder_service.prepare_service(argv)
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
    return app
