import itertools

import warder.common.config


def list_opts():
    return [
        ('DEFAULT',
         itertools.chain(warder.common.config.core_opts)),
        ('api_settings', warder.common.config.api_opts),
    ]

