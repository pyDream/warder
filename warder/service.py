from oslo_config import cfg
from oslo_log import log

from warder.common import config


def prepare_service(argv=None):
    """Sets global config from config file and sets up logging."""
    argv = argv or []
    config.init(argv[1:])
    log.set_defaults()
    config.setup_logging(cfg.CONF)