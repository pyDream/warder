# coding=utf-8


from warder.db import base_models
from warder.db import models


def get_metadata():
    return base_models.BASE.metadata