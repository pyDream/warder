from oslo_db.sqlalchemy import models
from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy.orm import collections


class WarderBase(models.ModelBase):

    __data_model__ = None

    @staticmethod
    def _get_unique_key(obj):
        """Returns a unique key for passed object for data model building."""
        # First handle all objects with their own ID, then handle subordinate
        # objects.
        if obj.__class__.__name__ in ['User']:
            return obj.__class__.__name__ + obj.id
        else:
            raise NotImplementedError

    def to_data_model(self, _graph_nodes=None):
        """Converts to a data model graph.

        In order to make the resulting data model graph usable no matter how
        many internal references are followed, we generate a complete graph of
        WarderBase nodes connected to the object passed to this method.

        :param _graph_nodes: Used only for internal recursion of this
                             method. Should not be called from the outside.
                             Contains a dictionary of all WarderBase type
                             objects in the generated graph
        """
        _graph_nodes = _graph_nodes or {}
        if not self.__data_model__:
            raise NotImplementedError
        dm_kwargs = {}
        for column in self.__table__.columns:
            dm_kwargs[column.name] = getattr(self, column.name)

        attr_names = [attr_name for attr_name in dir(self)
                      if not attr_name.startswith('_')]
        # Appending early, as any unique ID should be defined already and
        # the rest of this object will get filled out more fully later on,
        # and we need to add ourselves to the _graph_nodes before we
        # attempt recursion.
        dm_self = self.__data_model__(**dm_kwargs)
        dm_key = self._get_unique_key(dm_self)
        _graph_nodes.update({dm_key: dm_self})
        for attr_name in attr_names:
            attr = getattr(self, attr_name)
            if isinstance(attr, WarderBase) and attr.__class__:
                # If this attr is already in the graph node list, just
                # reference it there and don't recurse.
                ukey = self._get_unique_key(attr)
                if ukey in _graph_nodes.keys():
                    setattr(dm_self, attr_name, _graph_nodes[ukey])
                else:
                    setattr(dm_self, attr_name, attr.to_data_model(
                        _graph_nodes=_graph_nodes))
            elif isinstance(attr, (collections.InstrumentedList, list)):
                setattr(dm_self, attr_name, [])
                listref = getattr(dm_self, attr_name)
                for item in attr:
                    if isinstance(item, WarderBase) and item.__class__:
                        ukey = self._get_unique_key(item)
                        if ukey in _graph_nodes.keys():
                            listref.append(_graph_nodes[ukey])
                        else:
                            listref.append(
                                item.to_data_model(_graph_nodes=_graph_nodes))
                    elif not isinstance(item, WarderBase):
                        listref.append(item)
        return dm_self


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
