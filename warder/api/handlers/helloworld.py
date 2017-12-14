from oslo_config import cfg

from warder.api.handlers import abstract_handler


cfg.CONF.import_group('oslo_messaging', 'warder.common.config')


class HelloWorldHandler(abstract_handler.BaseHandler):
    pass