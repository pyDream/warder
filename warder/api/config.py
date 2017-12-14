from warder.api.common import hooks

# Pecan Application Configurations
# See https://pecan.readthedocs.org/en/latest/configuration.html#application-configuration # noqa
app = {
    'root': 'warder.api.root_controller.RootController',
    'modules': ['warder.api'],
    'hooks': [
        hooks.ContextHook(),
        hooks.QueryParametersHook()],
    'debug': False
}

# WSME Configurations
# See https://wsme.readthedocs.org/en/latest/integrate.html#configuration
wsme = {
    # Keeping debug True for now so we can easily troubleshoot.
    'debug': True
}