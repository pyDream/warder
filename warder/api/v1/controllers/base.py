import logging

from oslo_config import cfg
from pecan import rest

from warder.common import data_models
from warder.common import exceptions
from warder.db import repositories

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class BaseController(rest.RestController):

    def __init__(self):
        super(BaseController, self).__init__()
        self.repositories = repositories.Repositories()

    @staticmethod
    def _convert_db_to_type(db_entity, to_type, children=False):
        """Converts a data model into an Octavia WSME type

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

    @staticmethod
    def _get_db_obj(session, repo, data_model, id):
        """Gets an object from the database and returns it."""
        db_obj = repo.get(session, id=id)
        if not db_obj:
            LOG.exception('%(name)s %(id)s not found',
                          {'name': data_model._name(), 'id': id})
            raise exceptions.NotFound(
                resource=data_model._name(), id=id)
        return db_obj

    def _get_db_lb(self, session, id):
        """Get a load balancer from the database."""
        return self._get_db_obj(session, self.repositories.load_balancer,
                                data_models.LoadBalancer, id)
