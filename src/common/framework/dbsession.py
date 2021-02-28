#!/usr/bin/env python3

import contextlib
from typing import Generator, Any
from logging import getLogger
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session

LOGGER = getLogger(__name__)


@contextlib.contextmanager
def local_session(session_maker: scoped_session,
                  commit_on_exit: bool = False) \
        -> Generator[Session, Any, None]:

    thread_local_session = session_maker()
    LOGGER.debug("session created: %s" %
                 (str(thread_local_session)))

    try:
        yield thread_local_session
        if commit_on_exit:
            thread_local_session.commit()
    except Exception as ex:
        LOGGER.error("an error %s occurred while db session" %
                     (str(ex)))
        LOGGER.info("rollbacking all operations")
        thread_local_session.rollback()
        raise ex
    finally:
        thread_local_session.close()
