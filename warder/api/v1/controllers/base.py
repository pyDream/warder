import logging

from oslo_config import cfg
from pecan import rest
# from stevedore import driver as stevedore_driver
from warder.db import repositories

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class BaseController(rest.RestController):

    def __init__(self):
        super(BaseController, self).__init__()
        self.repositories = repositories.Repositories()
        # self.handler = stevedore_driver.DriverManager(
        #     namespace='warder.api.handlers',
        #     name=CONF.api_settings.api_handler,
        #     invoke_on_load=True
        # ).driver

    @staticmethod
    def _convert_db_to_type(db_entity, to_type, children=False):
        """Converts a data model into an Warder WSME type

        :param db_entity: data model to convert
        :param to_type: converts db_entity to this time
        """
        if isinstance(to_type, list):
            to_type = to_type[0]

        def _convert(db_obj):
            return to_type.from_data_model(db_obj, children=children)
        if isinstance(db_entity, list):
            converted = [_convert(db_obj) for db_obj in db_entity]
        else:
            converted = _convert(db_entity)
        return converted

