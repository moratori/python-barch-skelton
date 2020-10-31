#!/usr/bin/env python3


import common.framework.application.mysqlapplication as appframe
import common.data.dao as dao


class InitializeDatabase(appframe.MySQLApplication):

    def __init__(self):
        super().__init__(__name__, __file__)

    def validate_config(self):
        pass

    def setup_resource(self):
        pass

    def setup_application(self):
        pass

    def run_application(self, **args):
        dao.Base.metadata.create_all(bind=self.dbengine)

    def teardown_application(self):
        pass

    def teardown_resource(self):
        pass


if __name__ == "__main__":
    InitializeDatabase().start()
