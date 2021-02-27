#!/usr/bin/env python

import common.framework.application.batchbaseapplication as appframe
import common.data.table as table

from abc import abstractmethod
from logging import getLogger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

LOGGER = getLogger(__name__)


class DBBaseApplication(appframe.BatchBaseApplication):

    def __init__(self, module_name: str, script_name: str) -> None:
        super().__init__(module_name, script_name)

    @abstractmethod
    def create_db_specifier(self) -> str:
        pass

    def setup_resource(self) -> None:
        self.dbengine = create_engine(self.create_db_specifier(),
                                      encoding="utf-8",
                                      echo=False)

        LOGGER.debug("db engine %s created" % str(self.dbengine))

        table.Base.metadata.create_all(bind=self.dbengine)

        # pass this object to child thread in order to make
        # thread local session
        self.thread_local_session_maker = \
            scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=self.dbengine))

        LOGGER.debug("session maker %s created" %
                     str(self.thread_local_session_maker))

    def teardown_resource(self) -> None:
        self.thread_local_session_maker.remove()
        self.dbengine.dispose()
