#!/usr/bin/env python3

"""
docstring is here
"""

import common.framework.application.mysqlapplication as appframe
from common.db.table import SomethingTable

global LOGGER


class DBApplication(appframe.MySQLApplication):

    def __init__(self):
        super().__init__(__name__, __file__)

    def validate_config(self):
        super().validate_config()

    def setup_resource(self):
        super().setup_resource()

    def get_something_record(self):
        ret = self.session.query(SomethingTable).all()
        return ret

    def setup_application(self):
        pass

    def run_application(self):
        print("hello, world")
        print(self.get_something_record())

    def teardown_application(self):
        pass

    def teardown_resource(self):
        pass


if __name__ == "__main__":
    dbapp = DBApplication()
    LOGGER = dbapp.create_toplevel_logger()
    dbapp.start()
