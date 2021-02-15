#!/usr/bin/env python

import common.framework.application.baseapplication as appframe
import common.db.table as table

from logging import getLogger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

LOGGER = getLogger(__name__)


class PostgreSQLApplication(appframe.BaseApplication):

    def __init__(self, module_name, script_name):
        super().__init__(module_name, script_name)

    def validate_config(self):
        self.conf.common.postgresql.user
        self.conf.common.postgresql.passwd
        self.conf.common.postgresql.host
        self.conf.common.postgresql.dbname

    def setup_resource(self):
        database_specifier = \
            "postgresql+psycopg2://%s:%s@%s/%s" % (
                self.conf.common.postgresql.user,
                self.conf.common.postgresql.passwd,
                self.conf.common.postgresql.host,
                self.conf.common.postgresql.dbname)
        self.dbengine = create_engine(database_specifier,
                                      encoding="utf-8",
                                      echo=False)

        LOGGER.debug("create db engine completed")

        table.Base.metadata.create_all(bind=self.dbengine)

        # pass this object to child thread in order to make
        # theread local session
        self.thread_local_session_maker = \
            scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=self.dbengine))

        LOGGER.debug("create scoped session completed")

        self.session = self.thread_local_session_maker()

        LOGGER.debug("session created for current thread: %s" %
                     self.session)

    def setup_application(self):
        pass

    def teardown_application(self):
        pass

    def teardown_resource(self):
        self.session.close()
        self.dbengine.dispose()
