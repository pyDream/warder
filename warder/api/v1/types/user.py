from wsme import types as wtypes
from warder.api.common import types as base


class UserResponse(base.BaseType):
    """Defines the response and acceptable POST request attributes."""
    user_id = wtypes.wsattr(wtypes.UuidType())
    name = wtypes.text

class UserPost(base.BaseType):
    name = wtypes.text
    gender = wtypes.text
    age = int
    email = wtypes.text
    telephone = wtypes.text

class User(base.BaseType):
    id = int
    user_id = wtypes.wsattr(wtypes.UuidType())
    name = wtypes.text
    gender = wtypes.text
    age = int
    email = wtypes.text
    telephone = wtypes.text


class Users(base.BaseType):
    users = [User]