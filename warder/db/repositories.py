"""
Defines interface for DB access that Controllers may
reference
"""

from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy.orm import joinedload

from warder.common import constants as consts
from warder.db import models
from warder.common import exceptions

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class BaseRepository(object):
    model_class = None

    def count(self, session, **filters):
        """Retrieves a count of entities from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entities should be retrieved.
        :returns: int
        """
        return session.query(self.model_class).filter_by(**filters).count()

    def create(self, session, **model_kwargs):
        """Base create method for a database entity.

        :param session: A Sql Alchemy database session.
        :param model_kwargs: Attributes of the model to insert.
        :returns: warder.db.data_models
        """
        with session.begin(subtransactions=True):
            model = self.model_class(**model_kwargs)
            session.add(model)
        return model.to_data_model()

    def delete(self, session, **filters):
        """Deletes an entity from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entity should be deleted.
        :returns: None
        :raises: sqlalchemy.orm.exc.NoResultFound
        """
        model = session.query(self.model_class).filter_by(**filters).one()
        with session.begin(subtransactions=True):
            session.delete(model)
            session.flush()

    def delete_batch(self, session, ids=None):
        """Batch deletes by entity ids."""
        ids = ids or []
        [self.delete(session, id) for id in ids]

    def update(self, session, id, **model_kwargs):
        """Updates an entity in the database.

        :param session: A Sql Alchemy database session.
        :param model_kwargs: Entity attributes that should be updates.
        :returns: warder.db.data_models
        """
        with session.begin(subtransactions=True):
            session.query(self.model_class).filter_by(
                id=id).update(model_kwargs)

    def get(self, session, **filters):
        """Retrieves an entity from the database.

        :param session: A Sql Alchemy database session.
        :param filters: Filters to decide which entity should be retrieved.
        :returns: warder.db.data_models
        """
        model = session.query(self.model_class).filter_by(**filters).first()
        if not model:
            return
        return model.to_data_model()

    def get_all(self, session, pagination_helper=None, **filters):

        """Retrieves a list of entities from the database.

        :param session: A Sql Alchemy database session.
        :param pagination_helper: Helper to apply pagination and sorting.
        :param filters: Filters to decide which entities should be retrieved.
        :returns: [warder.db.data_models]
        """
        deleted = filters.pop('show_deleted', True)
        query = session.query(self.model_class).filter_by(**filters)
        # Only make one trip to the database
        query = query.options(joinedload('*'))

        if not deleted:
            query = query.filter(
                self.model_class.provisioning_status != consts.DELETED)

        if pagination_helper:
            model_list, links = pagination_helper.apply(
                query, self.model_class)
        else:
            links = None
            model_list = query.all()

        data_model_list = [model.to_data_model() for model in model_list]
        return data_model_list, links

    def exists(self, session, id):
        """Determines whether an entity exists in the database by its id.

        :param session: A Sql Alchemy database session.
        :param id: id of entity to check for existence.
        :returns: warder.db.data_models
        """
        return bool(session.query(self.model_class).filter_by(id=id).first())


class Repositories(object):
    def __init__(self):
        self.user = UserRepository()


class UserRepository(BaseRepository):
    model_class = models.User

    def add_user(self, session, user_dict):
        phones = []
        for tel_numb in user_dict["telephone"]:
            db_phone = models.Telephone(telnumber=tel_numb)
            phones.append(db_phone)
        user_dict["telephone"] = phones
        return self.create(session, **user_dict)

    def get_user(self, session, user_id):
        db_obj = self.get(session, user_id = user_id)
        if not db_obj:
            LOG.exception('User %(user_id)s not found',
                          {"user_id":user_id})
            raise exceptions.NotFound(resource="User", id=user_id)
        return  db_obj

    def update_user(self, session, user_id, **user_dict):
        if user_dict.has_key('telephone'):
            phones = []
            for phone in user_dict['telephone']:
                db_phone = models.Telephone(telnumber=phone)
                phones.append(db_phone)
            user_dict['telephone'] = phones
        self.update(session, user_id, **user_dict)
