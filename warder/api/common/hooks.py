from pecan import hooks

from warder.api.common import pagination
from warder.common import constants
from warder.common import context


class ContextHook(hooks.PecanHook):
    """Configures a request context and attaches it to the request."""

    def on_route(self, state):
        context_obj = context.Context.from_environ(state.request.environ)
        state.request.context['warder_context'] = context_obj


class QueryParametersHook(hooks.PecanHook):

    def before(self, state):
        if state.request.method != 'GET':
            return

        state.request.context[
            constants.PAGINATION_HELPER] = pagination.PaginationHelper(
            state.request.params.mixed())
