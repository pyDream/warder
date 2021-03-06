from oslo_config import cfg
from oslo_db import options as db_options
from oslo_log import log as logging

from warder.common import constants
from warder import version

LOG = logging.getLogger(__name__)

def _(s):
    return s

# TODO(rm_work) Remove in or after "R" release
API_SETTINGS_DEPRECATION_MESSAGE = _(
    'This setting has moved to the [api_settings] section.')

core_opts = [
]

api_opts = [
    cfg.IPOpt('bind_host', default='127.0.0.1',
              help=_("The host IP to bind to")),
    cfg.PortOpt('bind_port', default=9876,
                help=_("The port to bind to")),
    cfg.StrOpt('api_handler', default='queue_producer',
               help=_("The handler that the API communicates with")),
    cfg.BoolOpt('allow_pagination', default=True,
                help=_("Allow the usage of pagination")),
    cfg.BoolOpt('allow_sorting', default=True,
                help=_("Allow the usage of sorting")),
    cfg.BoolOpt('allow_filtering', default=True,
                help=_("Allow the usage of filtering")),
    cfg.BoolOpt('allow_field_selection', default=True,
                help=_("Allow the usage of field selection")),
    cfg.StrOpt('pagination_max_limit',
               default=str(constants.DEFAULT_PAGE_SIZE),
               help=_("The maximum number of items returned in a single "
                      "response. The string 'infinite' or a negative "
                      "integer value means 'no limit'")),
    cfg.StrOpt('api_base_uri',
               help=_("Base URI for the API for use in pagination links. "
                      "This will be autodetected from the request if not "
                      "overridden here.")),
    cfg.BoolOpt('api_v1_enabled', default=True,
                help=_("Expose the v1 API?")),
]

# Register the configuration options
cfg.CONF.register_opts(api_opts, group='api_settings')

_SQL_CONNECTION_DEFAULT = 'sqlite://'
# Update the default QueuePool parameters. These can be tweaked by the
# configuration variables - max_pool_size, max_overflow and pool_timeout
db_options.set_defaults(cfg.CONF, connection=_SQL_CONNECTION_DEFAULT,
                        max_pool_size=10, max_overflow=20, pool_timeout=10)

logging.register_options(cfg.CONF)


def init(args, **kwargs):
    cfg.CONF(args=args, project='warder',
             version='%%prog %s' % version.version_info.release_string(),
             **kwargs)


def setup_logging(conf):
    """Sets up the logging options for a log with supplied name.

    :param conf: a cfg.ConfOpts object
    """
    product_name = "warder"
    logging.setup(conf, product_name)
    LOG.info("Logging enabled!")
