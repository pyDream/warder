from oslo_db.sqlalchemy import models
from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext import declarative


class WarderBase(models.ModelBase):

    __data_model__ = None


class LookupTableMixin(object):
    """Mixin to add to classes that are lookup tables."""
    name = sa.Column(sa.String(255), primary_key=True, nullable=False)
    description = sa.Column(sa.String(255), nullable=True)


class IdMixin(object):
    """Id mixin, add to subclasses that have an id."""
    id = sa.Column(sa.String(36), primary_key=True,
                   default=uuidutils.generate_uuid)

class NameMixin(object):
    """Name mixin to add to classes which need a name."""
    name = sa.Column(sa.String(255), nullable=True)


BASE = declarative.declarative_base(cls=WarderBase)
