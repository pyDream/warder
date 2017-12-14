import contextlib

from oslo_config import cfg
from oslo_db.sqlalchemy import session as db_session
from oslo_utils import excutils

_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = db_session.EngineFacade.from_config(cfg.CONF, sqlite_fk=True)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(expire_on_commit=True, autocommit=True):
    """Helper method to grab session."""
    facade = _create_facade_lazily()
    return facade.get_session(expire_on_commit=expire_on_commit,
                              autocommit=autocommit)


@contextlib.contextmanager
def get_lock_session():
    """Context manager for using a locking (not auto-commit) session."""
    lock_session = get_session(autocommit=False)
    try:
        yield lock_session
        lock_session.commit()
    except Exception:
        with excutils.save_and_reraise_exception():
            lock_session.rollback()