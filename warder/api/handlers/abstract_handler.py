import abc

import six


@six.add_metaclass(abc.ABCMeta)
class BaseObjectHandler(object):
    """Base class for any object handler."""
    @abc.abstractmethod
    def create(self, model_id):
        """Begins process of actually creating data_model."""
        pass

    @abc.abstractmethod
    def update(self, model_id, updated_dict):
        """Begins process of actually updating data_model."""
        pass

    @abc.abstractmethod
    def delete(self, model_id):
        """Begins process of actually deleting data_model."""
        pass


class NotImplementedObjectHandler(BaseObjectHandler):
    """Default Object Handler to force implementation of subclasses.

    Helper class to make any subclass of AbstractHandler explode if it
    is missing any of the required object managers.
    """
    @staticmethod
    def update(model_id, updated_dict):
        raise NotImplementedError()

    @staticmethod
    def delete(model_id):
        raise NotImplementedError()

    @staticmethod
    def create(model_id):
        raise NotImplementedError()


@six.add_metaclass(abc.ABCMeta)
class BaseHandler(object):
    """Base class for all handlers."""
    hello_world = NotImplementedObjectHandler()
