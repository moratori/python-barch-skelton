#!/usr/bin/env python

import common.framework.application.dbapplication.dbbaseapplication as appframe
from logging import getLogger

LOGGER = getLogger(__name__)


class PostgreSQLApplication(appframe.DBBaseApplication):

    def __init__(self, module_name: str, script_name: str) -> None:
        super().__init__(module_name, script_name)

    def validate_config(self) -> None:
        self.conf.common.postgresql.user
        self.conf.common.postgresql.passwd
        self.conf.common.postgresql.host
        self.conf.common.postgresql.dbname

    def create_db_specifier(self) -> str:

        database_specifier = \
            "postgresql+psycopg2://%s:%s@%s/%s" % (
                self.conf.common.postgresql.user,
                self.conf.common.postgresql.passwd,
                self.conf.common.postgresql.host,
                self.conf.common.postgresql.dbname)

        return database_specifier
