#!/usr/bin/env python

import common.framework.application.dbapplication.dbbaseapplication as appframe
from logging import getLogger

LOGGER = getLogger(__name__)


class MySQLApplication(appframe.DBBaseApplication):

    def __init__(self, module_name: str, script_name: str) -> None:
        super().__init__(module_name, script_name)

    def validate_config(self) -> None:
        self.conf.common.mariadb.user
        self.conf.common.mariadb.passwd
        self.conf.common.mariadb.host
        self.conf.common.mariadb.dbname

    def create_db_specifier(self) -> str:
        database_specifier = 'mysql://%s:%s@%s/%s?charset=utf8' % (
            self.conf.common.mariadb.user,
            self.conf.common.mariadb.passwd,
            self.conf.common.mariadb.host,
            self.conf.common.mariadb.dbname
        )

        return database_specifier
