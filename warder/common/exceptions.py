from webob import exc

from warder.i18n import _


class APIException(exc.HTTPClientError):
      msg = "Something unknown went wrong"
      code = 500

      def __init__(self, **kwargs):
          self.msg = self.msg %kwargs
          super(APIException, self).__init__(detail=self.msg)


class NotFound(APIException):
    msg = _('%(resource)s %(id)s not found.')
    code = 404


class DeleteError(APIException):
    msg = _('%(resource)s %(id)s delete Error.')
    code = 500
