import copy

import six
from wsme import types as wtypes

if six.PY3:
    unicode = str

class BaseType(wtypes.Base):
    @classmethod
    def _full_response(cls):
        return False

    @classmethod
    def from_data_model(cls, data_model, children=False):
        """Converts data_model to Octavia WSME type.

        :param data_model: data model to convert from
        :param children: convert child data models
        """
        if not hasattr(cls, '_type_to_model_map'):
            return cls(**data_model.to_dict())

        dm_to_type_map = {value: key
                          for key, value in cls._type_to_model_map.items()}
        type_dict = data_model.to_dict()
        new_dict = copy.deepcopy(type_dict)
        for key, value in type_dict.items():
            if isinstance(value, dict):
                for child_key, child_value in value.items():
                    if '.'.join([key, child_key]) in dm_to_type_map:
                        new_dict['_'.join([key, child_key])] = child_value
            elif key in ['name', 'description'] and value is None:
                new_dict[key] = ''
            else:
                if key in dm_to_type_map:
                    new_dict[dm_to_type_map[key]] = value
                    del new_dict[key]
        return cls(**new_dict)

    def to_dict(self, render_unsets=False):
        """Converts Octavia WSME type to dictionary.

        :param render_unsets: If True, will convert items that are WSME Unset
                              types to None. If False, does not add the item
        """
        # Set project_id equal tenant_id if project_id is unset and tenant_id
        # is
        if hasattr(self, 'project_id') and hasattr(self, 'tenant_id'):
            if (isinstance(self.project_id, wtypes.UnsetType) and
                    not isinstance(self.tenant_id, wtypes.UnsetType)):
                self.project_id = self.tenant_id
        ret_dict = {}
        for attr in dir(self):
            if attr.startswith('_'):
                continue
            value = getattr(self, attr, None)
            # TODO(blogan): Investigate wsme types handling the duality of
            # tenant_id and project_id in a clean way.  One way could be
            # wsme.rest.json.fromjson and using the @fromjson.when_object
            # decorator.
            if attr == 'tenant_id':
                continue
            if value and callable(value):
                    continue
            if value and isinstance(value, BaseType):
                value = value.to_dict(render_unsets=render_unsets)
            if value and isinstance(value, list):
                value = [val.to_dict(render_unsets=render_unsets)
                         if isinstance(val, BaseType) else val
                         for val in value]
            if isinstance(value, wtypes.UnsetType):
                if render_unsets:
                    value = None
                else:
                    continue
            attr_name = attr
            if (hasattr(self, '_type_to_model_map') and
                    attr in self._type_to_model_map):
                renamed = self._type_to_model_map[attr]
                if '.' in renamed:
                    parent, child = renamed.split('.')
                    if parent not in ret_dict:
                        ret_dict[parent] = {}
                    ret_dict[parent][child] = value
                    continue
                attr_name = renamed
            ret_dict[attr_name] = value
        return ret_dict