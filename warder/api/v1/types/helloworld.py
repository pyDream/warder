from wsme import types as wtypes
from warder.api.common import types as base


class HelloWorldResponse(base.BaseType):
    """Defines the response and acceptable POST request attributes."""
    port_id = wtypes.wsattr(wtypes.UuidType())