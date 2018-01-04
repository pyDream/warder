#    Copyright (c) 2014 Rackspace
#    Copyright (c) 2016 Blue Box, an IBM Company
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re
import six


class BaseDataModel(object):
    def to_dict(self, calling_classes=None, recurse=False, **kwargs):
        """Converts a data model to a dictionary."""
        calling_classes = calling_classes or []
        ret = {}
        for attr in self.__dict__:
            if attr.startswith('_') or not kwargs.get(attr, True):
                continue
            value = self.__dict__[attr]

            if recurse:
                if isinstance(getattr(self, attr), list):
                    ret[attr] = []
                    for item in value:
                        if isinstance(item, BaseDataModel):
                            if type(self) not in calling_classes:
                                ret[attr].append(
                                    item.to_dict(calling_classes=(
                                        calling_classes + [type(self)])))
                            else:
                                ret[attr] = None
                        else:
                            ret[attr] = item
                elif isinstance(getattr(self, attr), BaseDataModel):
                    if type(self) not in calling_classes:
                        ret[attr] = value.to_dict(
                            calling_classes=calling_classes + [type(self)])
                    else:
                        ret[attr] = None
                elif six.PY2 and isinstance(value, six.text_type):
                    ret[attr.encode('utf8')] = value.encode('utf8')
                else:
                    ret[attr] = value
            else:
                if isinstance(getattr(self, attr), (BaseDataModel, list)):
                    ret[attr] = None
                else:
                    ret[attr] = value

        return ret

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.to_dict() == other.to_dict()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    @classmethod
    def _name(cls):
        """Returns class name in a more human readable form."""
        # Split the class name up by capitalized words
        return ' '.join(re.findall('[A-Z][^A-Z]*', cls.__name__))

    def update(self, update_dict):
        """Generic update method which works for simple,
        non-relational attributes.
        """
        for key, value in update_dict.items():
            setattr(self, key, value)


class User(BaseDataModel):

    def __repr__(self):
        return "<User(user_id='%s', name='%s', gender='%s',age='%s',email='%s')>" % (
            self.user_id, self.name, self.gender, self.age, self.email)

    def __init__(self, id, user_id, name, gender, age, email, telephone):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.age = age
        self.email = email
        self.telephone = telephone


class Telephone(BaseDataModel):
    def __repr__(self):
        return "<Telephone(user_id='%s', telnumber='%s')>" % (
            self.user_id, self.telnumber)

    def __init__(self, user_id, telnumber):
        self.user_id = user_id
        self.telnumber = telnumber