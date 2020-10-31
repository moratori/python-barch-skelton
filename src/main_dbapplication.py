#!/usr/bin/env python3

"""
docstring is here
"""

import common.framework.application.mysqlapplication as appframe
import common.data.dao as dao

global LOGGER


class DBApplication(appframe.MySQLApplication):

    def __init__(self):
        super().__init__(__name__, __file__)

    def validate_config(self):
        pass

    def get_something_record(self):
        ret = self.session.query(dao.SomethingTable)
        return ret

    def setup_resource(self):
        pass

    def setup_application(self):
        pass

    def run_application(self):
        print("hello, world")

    def teardown_application(self):
        pass

    def teardown_resource(self):
        pass


if __name__ == "__main__":
    dbapp = DBApplication()
    LOGGER = dbapp.create_toplevel_logger()
    dbapp.start()
