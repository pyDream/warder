import sys
from wsgiref import simple_server

from oslo_config import cfg
from oslo_log import log as logging
from oslo_reports import guru_meditation_report as gmr

from warder.api import app as api_app
from warder import version


LOG = logging.getLogger(__name__)


def main():
    gmr.TextGuruMeditation.setup_autorun(version)

    app = api_app.setup_app(argv=sys.argv)

    host = cfg.CONF.api_settings.bind_host
    port = cfg.CONF.api_settings.bind_port
    LOG.info("Starting API server on %(host)s:%(port)s",
             {"host": host, "port": port})
    srv = simple_server.make_server(host, port, app)

    srv.serve_forever()
