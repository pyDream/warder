from wsme import types as wtypes
from warder.api.common import types as base


class HelloWorldResponse(base.BaseType):
    """Defines the response and acceptable POST request attributes."""
    ip_address = wtypes.wsattr(base.IPAddressType())
    port_id = wtypes.wsattr(wtypes.UuidType())
    subnet_id = wtypes.wsattr(wtypes.UuidType())
    network_id = wtypes.wsattr(wtypes.UuidType())